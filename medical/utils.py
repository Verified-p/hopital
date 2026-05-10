import requests
import base64
from datetime import datetime
from django.conf import settings


def get_access_token():
    """Generate M-Pesa access token"""
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    response.raise_for_status()
    access_token = response.json().get("access_token")

    if not access_token:
        raise ValueError("Failed to obtain M-Pesa access token")

    return access_token


def initiate_stk_push(phone_number, amount):
    """Initiate M-Pesa STK Push"""
    access_token = get_access_token()
    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    business_short_code = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate password
    data_to_encode = business_short_code + passkey + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode("utf-8")

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "MEDICAL_STORE",
        "TransactionDesc": "Payment for Medicine",
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    response_data = response.json()

    # Print response in terminal for debugging
    print("==== Safaricom STK Response ====")
    print(response_data)

    if response.status_code == 200 and response_data.get("ResponseCode") == "0":
        return {"success": True, "message": "✅ STK Push sent successfully!", "data": response_data}
    else:
        return {
            "success": False,
            "message": f"❌ Payment initiation failed: {response_data.get('errorMessage', 'Unknown error')}",
            "data": response_data,
        }
