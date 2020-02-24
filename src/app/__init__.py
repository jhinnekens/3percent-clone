from flask import Flask
import os
app = Flask(__name__)
print(app.root_path)

from app import routes
