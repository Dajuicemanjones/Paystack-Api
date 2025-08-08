from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Your Paystack Secret Key
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_live_xxxxxxxxxxxxxxxxx")

@app.route('/')
def home():
    return 'Paystack payment API is running!'

@app.route('/create-payment', methods=['POST'])
def create_payment():
    data = request.get_json()

    amount = data.get('amount')  # Amount in USD (from Shopify frontend)
    email = data.get('email')

    # Convert USD to kobo (Paystack uses NGN kobo internally — multiply by 100)
    # But since your store is USD, we tell Paystack currency is USD
    amount_in_cents = int(float(amount) * 100)

    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        "email": email,
        "amount": amount_in_cents,
        "currency": "USD",
        "callback_url": "https://ninshuorbs.com/thank_you"
    }

    r = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
    response_data = r.json()

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


