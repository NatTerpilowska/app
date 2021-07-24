from flask import url_for
from flask_testing import LiveServerTestCase

from selenium import webdriver
from urllib.request import urlopen

from application import app, db
from application.models import Story

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            DEBUG=True,
            LIVESERVER_PORT=self.TEST_PORT
        )
        return app

    def setUp(self):
        db.create_all()

        db.session.add(Story(description="Run integration tests"))
        db.session.add(Story(description="Do something else", completed=True))

        db.session.commit()

        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/')

    def tearDown(self):
        db.drop_all()
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/')
        assert response.code == 200

class TestCreate(TestBase):
    def test_create(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()

        self.driver.find_element_by_xpath('//*[@id="description"]').send_keys("Create")

        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        element = self.driver.find_element_by_xpath("/html/body/div[4]")
        assert "Create" in element.text