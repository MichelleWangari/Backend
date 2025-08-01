# mpesa.py
import requests
import base64
import datetime
import os
from .daraja import get_access_token
from .models import PaymentTransaction

def lipa_na_mpesa(phone, amount):
    access_token = get_access_token()
    if not access_token:
        return {"success": False, "message": "Failed to get access token"}

    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")
    callback_url = os.getenv("CALLBACK_URL")
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Generate password
    data_to_encode = shortcode + passkey + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": encoded_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "TujengeChama",
        "TransactionDesc": "Chama contribution"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        res = response.json()
        transaction = PaymentTransaction.objects.create(
            phone=phone,
            amount=amount,
            transaction_id=res.get("MerchantRequestID", ""),  # Placeholder for now
            checkout_request_id=res.get("CheckoutRequestID", ""),
            result_code=-1,  # Unknown until callback
            result_description="Pending"
        )
        return {"success": True, "checkout_request_id": transaction.checkout_request_id}
    else:
        return {"success": False, "message": response.text}
