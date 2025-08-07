from flask import Flask
import numpy as np
from app.routes import register_routes

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)
    register_routes(app)
    return app