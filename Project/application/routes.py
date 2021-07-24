from . import app, db
from .models import Card, Story
from .forms import StoryForm, CardForm
from flask import redirect, url_for, request, render_template

@app.route("/")
def home():
    stories = Story.query.all()

    return render_template("home.html", stories=stories)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = StoryForm()

    if request.method == "POST":
        new_story = Story(
            description=form.description.data,
            card_id=form.card.data
            )
        db.session.add(new_story)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        cards = Card.query.all()
        form.card.choices = [(card.id, card.name) for card in cards]

        return render_template("create_story.html", form=form)

@app.route("/create_card", methods=["GET", "POST"])
def create_card():
    form = CardForm()

    if request.method == "POST":
        new_card = Card(name=form.name.data)
        db.session.add(new_card)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("create_card.html", form=form)

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    story = Story.query.get(id)
    form = StoryForm()

    if request.method == "POST":
        story.description = form.description.data
        story.card_id = form.card.data
        db.session.add(story)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        cards = Card.query.all()
        form.card.choices = [(card.id, card.name) for card in cards]

        form.description.data = story.description

        return render_template("create_story.html", form=form)

@app.route("/delete/<int:id>")
def delete(id):
    story = Story.query.get(id)
    db.session.delete(story)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/complete/<int:id>")
def complete(id):
    story = Story.query.get(id)
    story.completed = True
    db.session.add(story)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/incomplete/<int:id>")
def incomplete(id):
    story = Story.query.get(id)
    story.completed = False
    db.session.add(story)
    db.session.commit()

    return redirect(url_for("home"))