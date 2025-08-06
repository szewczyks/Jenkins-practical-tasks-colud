import numpy as np
from flask import jsonify

def register_routes(app):
    @app.route("/")
    def index():
        return jsonify({"message": "Hello from Flask"})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/random")
    def random_number():
        random_value = np.random.randint(1, 100)
        return jsonify({"random_number": int(random_value)})