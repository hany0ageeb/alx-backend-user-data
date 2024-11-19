#!/usr/bin/env python3
"""Route module for basic flask app API
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """return a JSON payload of the form:
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
