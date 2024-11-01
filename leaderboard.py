# leaderboard.py

from flask import Flask, jsonify
from config import db
from guess import Guess
from user import User  # Assuming there’s a User model for user data

app = Flask(__name__)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    """
    Retrieves the leaderboard for the Zoom-n-Guess game.
    Shows correct guesses first, then incorrect ones, ordered by timestamp.
    """
    guesses = Guess.query.order_by(Guess.is_correct.desc(), Guess.timestamp.desc()).all()
    leaderboard_data = []

    for guess in guesses:
        user = User.query.get(guess.user_id)
        leaderboard_data.append({
            "username": user.username if user else "Unknown",
            "image_id": guess.image_id,
            "guess": guess.guess_text,
            "reasoning": guess.reasoning,
            "is_correct": guess.is_correct,
            "timestamp": guess.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(leaderboard_data)

if __name__ == "__main__":
    app.run(debug=True)
