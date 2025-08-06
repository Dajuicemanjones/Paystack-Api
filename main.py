from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Securely load your Paystack Secret Key from environment variable
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

@app.route('/')
def home():
    return 'Paystack payment API is running!'

@app.route('/create-payment', methods=['POST'])
def create_payment():
    data = request.get_json()

    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        'email': data['email'],
        'amount': int(data['amount']) * 100,  # Convert to kobo
        'currency': 'NGN',  # You can change this to 'USD' if you're using USD on Paystack
        'callback_url': data['callback_url']
    }

    response = requests.post('https://api.paystack.co/transaction/initialize', json=payload, headers=headers)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
