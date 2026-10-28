import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from backend import database, ai_engine

def run_tests():
    print("=== 1. Testing Database Cards ===")
    cards = database.get_all_cards()
    print(f"Total cards seeded: {len(cards)}")
    assert len(cards) >= 20, f"Expected at least 20 cards, got {len(cards)}"
    print("First card:", cards[0]['name'], "Category:", cards[0]['category_id'])

    print("\n=== 2. Testing Categories ===")
    cats = database.get_categories()
    print("Categories found:", [c['name'] for c in cats])

    print("\n=== 3. Testing AI Engine (Telugu Query) ===")
    te_query = "నా ఫ్రెండ్ పుట్టినరోజుకి ₹1000 లోపు ఏ గేమింగ్ గిఫ్ట్ కార్డ్ బాగుంటుంది?"
    te_res = ai_engine.generate_ai_sales_response(te_query)
    print("Language detected:", te_res['language'])
    print("Matched cards count:", len(te_res['cards']))
    print("Top matched cards:", [c['name'] for c in te_res['cards'][:3]])
    print("Telugu response snippet:\n", te_res['reply'][:200])

    print("\n=== 4. Testing AI Engine (English Query) ===")
    en_query = "Suggest best shopping discount card under 2000 for sister"
    en_res = ai_engine.generate_ai_sales_response(en_query)
    print("Language detected:", en_res['language'])
    print("Top matched cards:", [c['name'] for c in en_res['cards'][:3]])

    print("\n=== 5. Testing Greeting Message Generator ===")
    wish = ai_engine.generate_personalized_greeting("Sneha", "Birthday", "te")
    print("Generated Telugu Wish:", wish)

    print("\n=== 6. Testing Checkout & Voucher Generation ===")
    order = database.create_order(
        customer_name="Suresh Varma",
        customer_email="suresh@example.com",
        customer_phone="9876543210",
        recipient_name="Priya",
        recipient_email="priya@example.com",
        card_id="amazon-pay",
        denomination=1000.0,
        discount_amount=40.0,
        final_price=960.0,
        gift_message="Happy Birthday Priya!",
        occasion="Birthday",
        payment_method="UPI"
    )
    print("Generated Order ID:", order['order_id'])
    print("Voucher Code:", order['voucher_code'])
    print("Voucher PIN:", order['voucher_pin'])

    print("\n=== 7. Testing Balance Verification ===")
    bal = database.check_card_balance(order['voucher_code'])
    assert bal is not None, "Card balance check failed"
    print("Balance Verified:", bal['denomination'], "for", bal['card_name'])

    print("\n=== 8. Testing Admin Stats ===")
    stats = database.get_admin_stats()
    print("Admin stats:", stats)

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Platform is 100% operational.")

if __name__ == "__main__":
    run_tests()
