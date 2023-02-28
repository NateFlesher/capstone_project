import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# give access to the project in any operation system we find outselves in
# alllows outside filers and folders to be added to the project from the based directory

load_dotenv(os.path.join(basedir, '.env'))


class Config():
    """
    set Config variables for the flask app.
    Using Environment Variables where available otherwise
    create the config variable if not done already
    """
    FLASK_APP=os.environ.get('FLASK_APP')
    FLASK_APP=os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ERROR'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlitre:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turn off update messages