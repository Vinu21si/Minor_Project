# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    game = db.Column(db.String(50))  # 'tictactoe' or 'chess'
    result = db.Column(db.String(20)) # 'win','loss','draw','move'
    value = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
