from flask_testing import TestCase
from flask import url_for

from application import app, db
from application.models import Story

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            WTF_CSRF_ENABLED=False
        )

        return app

    def setUp(self):
        db.create_all()
        
        db.session.add(Story(description="run unit tests"))
        db.session.add(Story(description="do something else", completed=True))
    
        db.session.commit()

    def tearDown(self):
        db.drop_all()

class TestViews(TestBase):

    def test_create(self):
        response = self.client.get(url_for("create"))
        self.assert200(response)    

    def test_create_card(self):
        response = self.client.get(url_for("create_card"))
        self.assert200(response)   

    def test_update(self):
        response = self.client.get(url_for("update", id=1))
        self.assert200(response)        

class TestRead(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"),
        follow_redirects=True)

        assert "Run unit tests" not in response.data.decode()
        assert "Do something else" not in response.data.decode()

class TestCreate(TestBase):
    def test_create(self):
        response = self.client.post(
            url_for("create"),
            data={"description": "Check create is working"},
            follow_redirects=True
        )

        assert "Check create is working" in response.data.decode()

    def test_create_card(self):
        response = self.client.post(
            url_for("create_card", id=1),
            data={"description": "Check create is working2"},
            follow_redirects=True
        )

        assert "Check create is working" not in response.data.decode()    

class TestUpdate(TestBase):
    def test_update(self):
        response = self.client.post(
            url_for("update", id=1),
            data={"description": "Check update is working"},
            follow_redirects=True
        )
        
        assert "do something" in response.data.decode()
        assert "Run unit tests"          not in response.data.decode()

    def test_complete(self):
        response = self.client.get(
            url_for("complete", id=1),
            follow_redirects=True
        )
        assert "Run unit tests -👾" not in response.data.decode()
        assert "Do something else -👾"not in response.data.decode()

    def test_incomplete(self):
        response = self.client.get(
            url_for("incomplete", id=1),
            follow_redirects=True
        )
        assert "Run unit tests -👾" not in response.data.decode()
        assert "Do something else -" not in response.data.decode()    
        


class TestDelete(TestBase):
    def test_delete(self):
        response = self.client.get(
            url_for("delete", id=1),
            follow_redirects=True
        )

        assert "Run unit tests" not in response.data.decode()