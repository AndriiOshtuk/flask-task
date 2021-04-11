import os

DEBUG = True
HOST = os.getenv("APPLICATION_HOST", "0.0.0.0")
PORT = int(os.getenv("APPLICATION_PORT", "5000"))
SQLALCHEMY_TRACK_MODIFICATIONS = False

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
DB_URI = os.getenv("DB_URI", "sqlite:///{}".format(DB_PATH))
