import os
from decouple import config as ENV

DEBUG = True

SECRET_KEY = ENV("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}