from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class StoryForm(FlaskForm):
    description = StringField("What is the story?")
    card = SelectField("Choose a card", choices=[])
    submit = SubmitField("Submit")

class CardForm(FlaskForm):
    name = StringField("What is the card?")
    submit = SubmitField("Submit")