
import flask_sqlalchemy
from flask import Flask
from app import db
from enum import Enum

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    message = db.Column(db.String(120))
    
    def __init__(self, name, message):
        
        self.name = name
    
        self.message = message
        
    def __repr__(self):
        return "<User name: {}\nmessage: {}".format(self.name, self.message)

class AuthUserType(Enum):
    LINKEDIN = "linkedin"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    GITHUB = "github"
    PASSWORD = "password"