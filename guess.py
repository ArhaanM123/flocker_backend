# guess.py

from datetime import datetime
from config import db  # Import the configured db instance (SQLAlchemy)

class Guess(db.Model):
    """
    Guess Model
    
    Stores each guess made in the Zoom-n-Guess game.
    
    Attributes:
        id (int): Primary key for the guess.
        image_id (int): ID of the image being guessed.
        guess_text (str): The guess provided by the user.
        reasoning (str): User's reasoning for the guess.
        user_id (int): ID of the user who made the guess.
        is_correct (bool): Whether the guess was correct or not.
        timestamp (datetime): When the guess was made.
    """
    __tablename__ = 'guesses'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, nullable=False)
    guess_text = db.Column(db.String(255), nullable=False)
    reasoning = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, image_id, guess_text, reasoning, user_id, is_correct):
        self.image_id = image_id
        self.guess_text = guess_text
        self.reasoning = reasoning
        self.user_id = user_id
        self.is_correct = is_correct

    def __repr__(self):
        return f"<Guess(id={self.id}, guess_text='{self.guess_text}', is_correct={self.is_correct})>"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
