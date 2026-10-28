import sys
import os
import time
import threading
import requests
import uvicorn

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.server import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

def test_http():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1.5)

    base = "http://127.0.0.1:8000"
    print("Testing GET / (index.html)...")
    r = requests.get(f"{base}/")
    assert r.status_code == 200
    assert "GiftCraft AI" in r.text
    print("-> GET / SUCCESS (HTML rendered)")

    print("Testing GET /api/cards...")
    r = requests.get(f"{base}/api/cards")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 20
    print(f"-> GET /api/cards SUCCESS ({data['count']} cards returned)")

    print("Testing POST /api/chat (Telugu)...")
    r = requests.post(f"{base}/api/chat", json={"message": "నాకు నెట్‌ఫ్లిక్స్ లేదా స్పాటిఫై కార్డ్ కావాలి"})
    assert r.status_code == 200
    chat_res = r.json()
    assert len(chat_res["cards"]) > 0
    print("-> POST /api/chat SUCCESS. Matched:", [c["name"] for c in chat_res["cards"][:2]])

    print("Testing POST /api/coupon/validate...")
    r = requests.post(f"{base}/api/coupon/validate", json={"coupon_code": "WELCOME10", "subtotal": 1000})
    assert r.status_code == 200
    c_res = r.json()
    assert c_res["valid"] is True
    print(f"-> Coupon VALID. Saved: Rs.{c_res['discount_amount']}")

    print("Testing POST /api/checkout...")
    r = requests.post(f"{base}/api/checkout", json={
        "card_id": "steam-wallet",
        "denomination": 500,
        "customer_name": "Kiran",
        "customer_email": "kiran@example.com",
        "coupon_code": "WELCOME10"
    })
    assert r.status_code == 200
    chk_res = r.json()
    assert chk_res["success"] is True
    order = chk_res["order"]
    print(f"-> Order SUCCESS: {order['order_id']} | Voucher: {order['voucher_code']} | PIN: {order['voucher_pin']}")

    print("\n✅ ALL HTTP & REST API ENDPOINTS ARE FULLY OPERATIONAL!")

if __name__ == "__main__":
    test_http()
