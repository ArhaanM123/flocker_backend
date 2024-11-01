# db_init.py

from config import app, db
from guess import Guess

def init_guesses():
    with app.app_context():
        db.create_all()
        
        # Sample data for testing
        guess1 = Guess(image_id=1, guess_text="Eiffel Tower", reasoning="It looks like iron lattice work.", user_id=1, is_correct=True)
        guess2 = Guess(image_id=2, guess_text="Great Wall", reasoning="Stony structure across hills.", user_id=2, is_correct=False)
        
        for guess in [guess1, guess2]:
            try:
                guess.save()
                print(f"Record created: {repr(guess)}")
            except Exception as e:
                print(f"Failed to add record: {e}")

if __name__ == "__main__":
    init_guesses()
