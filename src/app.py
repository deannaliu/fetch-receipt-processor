from flask import Flask, request, jsonify

import uuid # a python library which helps in generating random objects of 128 bits as ids.

from utils import validate_receipt

# command: python app.py
app = Flask(__name__)

# Key: receipt_id 
# Value: points
receipts = {} # dictionary to hold the receipts 

# Route decorator in Flask
# Route: /receipts/process
# HTTP method: POST endpoint to process a receipt
@app.route('/receipts/process', methods=['POST']) 
def process_receipt():
    data = request.json

    # check if recipt is valid
    is_receipt_valid = validate_receipt(data)
    # calculate the points


# Route decorator in Flask
# Route: /receipts/process
# HTTP method: GET endpoint to get points for a given receipt
@app.route('/receipts/process', methods=['GET'])
def get_points(receipt_id):
    if receipt_id not in receipts:
        return jsonify({"error": "invalid receipt/receipt not found"}), 404
    return jsonify({"points": receipts[receipt_id]}), 200

if __name__ == '__main__':
    app.run(debug=True)