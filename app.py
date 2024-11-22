from flask import Flask, request, jsonify

import uuid # a python library which helps in generating random objects of 128 bits as ids.

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)