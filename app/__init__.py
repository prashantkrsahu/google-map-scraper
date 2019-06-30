from flask import Flask

app = Flask(__name__)

#Load Config File
app.config.from_object('config')

from app import views
