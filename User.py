from flask import request, jsonify, g
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from config import db

class User(db.Model):
    """
    User Model
    
    Represents a registered user in the system.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the user.
        username (db.Column): A unique string representing the username.
        email (db.Column): A unique string representing the user's email.
        password_hash (db.Column): A string representing the hashed password.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists.")

    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class UserAPI:
    """
    API Endpoints for User model.
    
    Provides methods for creating new users and retrieving user information.
    """
    class CreateUser(Resource):
        def post(self):
            data = request.get_json()
            try:
                user = User(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                user.create()
                return jsonify({"message": "User created", "user": user.read()})
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

    class GetUser(Resource):
        @token_required
        def get(self):
            user = g.current_user
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify(user.read())

    class DeleteUser(Resource):
        @token_required
        def delete(self):
            user = g.current_user
            if user:
                user.delete()
                return jsonify({"message": "User deleted"})
            return jsonify({"error": "User not found"}), 404

# Add endpoints to the API
from config import app
from flask_restful import Api

api = Api(app)
api.add_resource(UserAPI.CreateUser, '/user')
api.add_resource(UserAPI.GetUser, '/user/<int:id>')
api.add_resource(UserAPI.DeleteUser, '/user/<int:id>')
