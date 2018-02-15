import sqlite3
import os

from flask import Flask
app = Flask(__name__)

import storeapp.views

#load config
app.config.from_object('config')

