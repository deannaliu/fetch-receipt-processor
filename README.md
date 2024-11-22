python app.py

curl -X POST http://127.0.0.1:5000/receipts/process -H "Content-Type: application/json" --data "@../examples/morning-receipt.json" 
