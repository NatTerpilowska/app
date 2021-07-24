from . import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    stories = db.relationship('Story', backref="card")