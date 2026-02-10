import requests
from django.conf import settings

BASE_URL = "https://accept.paymob.com/api"

def get_auth_token():
    r = requests.post(f"{BASE_URL}/auth/tokens", json={
        "api_key": settings.PAYMOB_API_KEY
    })
    return r.json()["token"]


def create_order(token, amount_cents):
    r = requests.post(f"{BASE_URL}/ecommerce/orders", json={
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": amount_cents,
        "currency": "EGP",
        "items": [],
    })
    return r.json()["id"]

def get_payment_key(token, order_id, amount_cents, user):
    r = requests.post(f"{BASE_URL}/acceptance/payment_keys", json={
        "auth_token": token,
        "amount_cents": amount_cents,
        "expiration": 3600,
        "order_id": order_id,
        "currency": "EGP",
        "integration_id": int(settings.PAYMOB_CARD_INTEGRATION_ID),
        "billing_data": {
            "first_name": user.username or "User",
            "last_name": "Test",
            "email": user.email or "test@test.com",
            "phone_number": "01000000000",
            "country": "EG",
            "city": "Cairo",
            "street": "NA",
            "building": "NA",
            "floor": "NA",
            "apartment": "NA",
            "postal_code": "NA",
        }
    })

    data = r.json()

    # 🔥 Debug ذكي
    if not isinstance(data, dict):
        raise Exception(f"Paymob Error (not dict): {data}")

    if "token" not in data:
        raise Exception(f"Paymob Error (no token): {data}")

    return data["token"]
