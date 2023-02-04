from flask import Flask, jsonify, make_response
import requests
import os


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    ''' Greet the user '''

    return "Hey! The service is up, how about doing something useful"


if __name__ == '__main__':
    app.run(port=5000, debug=True)