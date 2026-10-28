"""
GiftCard Platform - Main FastAPI Application Server
Provides REST APIs for Catalog, AI Sales Concierge, Digital Checkout, and Scratch-to-Reveal Voucher Delivery.
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from . import database
from . import ai_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(
    title="GiftCraft AI - Universal Gift Card Marketplace",
    description="All-in-One AI-Powered Gift Card Marketplace selling gaming, shopping, entertainment, food, and travel gift cards.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Request Models -----------------

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = "guest"

class CheckoutRequest(BaseModel):
    card_id: str
    denomination: float
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = ""
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None
    gift_message: Optional[str] = ""
    occasion: Optional[str] = "General"
    payment_method: Optional[str] = "UPI"
    coupon_code: Optional[str] = None
    upi_utr_ref: Optional[str] = None

class CouponValidationRequest(BaseModel):
    coupon_code: str
    subtotal: float

class BalanceCheckRequest(BaseModel):
    voucher_code: str

class GreetingRequest(BaseModel):
    recipient: str
    occasion: str
    lang: Optional[str] = "te"


class MerchantSettingsUpdate(BaseModel):
    merchant_name: Optional[str] = "GiftCraft Store Owner"
    bank_name: Optional[str] = "HDFC Bank"
    account_number: Optional[str] = "50100492817291"
    ifsc_code: Optional[str] = "HDFC0001234"
    merchant_upi_id: Optional[str] = "giftcraft@okhdfcbank"
    active_gateway: Optional[str] = "Razorpay"
    razorpay_key_id: Optional[str] = "rzp_test_YOUR_KEY_HERE"
    phonepe_merchant_id: Optional[str] = "MERCHANTUAT"

# ----------------- API Endpoints -----------------

@app.get("/api/categories")
def get_categories():
    """Retrieve all available gift card categories with counts"""
    return database.get_categories()

@app.get("/api/merchant-info")
def get_merchant_public_info():
    """Retrieve active merchant UPI ID for customer QR code payment"""
    settings = database.get_merchant_settings()
    return {
        "merchant_name": settings.get("merchant_name", "GiftCraft Store"),
        "merchant_upi_id": settings.get("merchant_upi_id", "9059382131-2@ybl")
    }

@app.get("/api/cards")
def get_cards(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "popular"
):
    """Filter, search and retrieve gift cards"""
    cards = database.get_all_cards(category=category, search=search, sort_by=sort_by)
    return {"count": len(cards), "cards": cards}

@app.get("/api/cards/{card_id}")
def get_card_detail(card_id: str):
    """Retrieve full details of a specific gift card"""
    card = database.get_card_by_id(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Gift card not found")
    return card

@app.post("/api/chat")
def chat_with_ai(payload: ChatMessageRequest):
    """
    Intelligent AI Sales Concierge.
    Understands customer needs in Telugu/English, recommends matching cards,
    computes best discounts, and guides to instant checkout.
    """
    response_data = ai_engine.generate_ai_sales_response(
        user_message=payload.message,
        session_id=payload.session_id or "guest"
    )
    return response_data

@app.post("/api/generate-message")
def generate_greeting(payload: GreetingRequest):
    """Generate heartwarming custom greeting message for gift cards"""
    wish = ai_engine.generate_personalized_greeting(
        recipient=payload.recipient,
        occasion=payload.occasion,
        lang=payload.lang or "te"
    )
    return {"message": wish}

@app.post("/api/coupon/validate")
def validate_coupon(payload: CouponValidationRequest):
    """Validate promo coupon codes (e.g. WELCOME10, AIDEAL5, FESTIVE15)"""
    code = payload.coupon_code.strip().upper()
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE code = ?", (code,))
    coupon = cursor.fetchone()
    conn.close()

    if not coupon:
        return {"valid": False, "message": "Invalid or expired promo code"}

    min_order = coupon["min_order"]
    if payload.subtotal < min_order:
        return {
            "valid": False,
            "message": f"Minimum order amount of ₹{min_order} required for {code}"
        }

    pct = coupon["discount_pct"]
    max_disc = coupon["max_discount"]
    discount_val = min((payload.subtotal * (pct / 100.0)), max_disc)

    return {
        "valid": True,
        "code": code,
        "discount_pct": pct,
        "discount_amount": round(discount_val, 2),
        "message": f"Promo applied! You saved ₹{round(discount_val, 2)}"
    }

@app.post("/api/checkout")
def process_checkout(payload: CheckoutRequest):
    """
    Execute order, apply brand discount and optional coupon,
    generate secure 16-digit voucher code & PIN with instant digital delivery.
    """
    card = database.get_card_by_id(payload.card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Selected gift card does not exist")

    denom = float(payload.denomination)
    if denom <= 0:
        raise HTTPException(status_code=400, detail="Invalid denomination")

    # Calculate brand discount
    brand_disc_pct = card.get("discount_pct", 0.0)
    brand_discount = denom * (brand_disc_pct / 100.0)

    # Optional Coupon discount
    coupon_discount = 0.0
    if payload.coupon_code:
        c_code = payload.coupon_code.strip().upper()
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coupons WHERE code = ?", (c_code,))
        coupon = cursor.fetchone()
        conn.close()
        if coupon and denom >= coupon["min_order"]:
            coupon_val = min((denom * (coupon["discount_pct"] / 100.0)), coupon["max_discount"])
            coupon_discount = coupon_val

    total_discount = round(brand_discount + coupon_discount, 2)
    final_price = max(1.0, round(denom - total_discount, 2))

    order = database.create_order(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        customer_phone=payload.customer_phone or "",
        recipient_name=payload.recipient_name or payload.customer_name,
        recipient_email=payload.recipient_email or payload.customer_email,
        card_id=payload.card_id,
        denomination=denom,
        discount_amount=total_discount,
        final_price=final_price,
        gift_message=payload.gift_message or "",
        occasion=payload.occasion or "General",
        payment_method=payload.payment_method or "UPI"
    )

    # Merge card details for immediate display
    order["card_name"] = card["name"]
    order["brand"] = card["brand"]
    order["logo_icon"] = card["logo_icon"]
    order["card_gradient"] = card["card_gradient"]
    order["redemption_guide"] = card["redemption_guide"]
    order["terms"] = card["terms"]

    return {
        "success": True,
        "message": "Payment verified and voucher generated successfully!",
        "order": order
    }

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    """Retrieve full order details with scratchable voucher code and PIN"""
    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/check-balance")
def check_balance(payload: BalanceCheckRequest):
    """Simulate checking remaining balance and expiry of gift card voucher"""
    order = database.check_card_balance(payload.voucher_code)
    if not order:
        return {
            "found": False,
            "message": "Card code not found or invalid format. Please check the 16-digit voucher code."
        }
    return {
        "found": True,
        "card_name": order["card_name"],
        "brand": order["brand"],
        "denomination": order["denomination"],
        "balance": order["denomination"] if not order["is_redeemed"] else 0.0,
        "status": "Active & Valid" if not order["is_redeemed"] else "Already Redeemed",
        "created_at": order["created_at"],
        "expiry": "Valid for 12 months from issuance"
    }

@app.get("/api/recent-orders")
def get_recent_orders():
    """Live orders feed ticker for social proof and activity"""
    return database.get_recent_orders(limit=8)

@app.get("/api/admin/stats")
def get_admin_dashboard_stats():
    """Retrieve admin summary statistics"""
    return database.get_admin_stats()

@app.get("/api/admin/payout-settings")
def get_payout_settings():
    """Retrieve merchant settlement bank details and gateway configurations"""
    return {
        "settings": database.get_merchant_settings(),
        "settlements": database.get_settlements_history()
    }

@app.post("/api/admin/payout-settings")
def update_payout_settings(payload: MerchantSettingsUpdate):
    """Update bank account and payment gateway keys"""
    updated = database.update_merchant_settings(payload.model_dump())
    return {
        "success": True,
        "message": "Merchant bank account & payment gateway configuration saved successfully!",
        "settings": updated
    }


# ----------------- Serve Frontend Static Files -----------------

# Mount assets directory if exists
assets_dir = os.path.join(FRONTEND_DIR, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Serve frontend root
@app.get("/")
def serve_home():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "GiftCard Platform API running. Frontend index.html not yet placed."})

# Catch-all for other frontend static files like style.css, app.js
@app.get("/{file_name:path}")
def serve_static(file_name: str):
    target = os.path.join(FRONTEND_DIR, file_name)
    if os.path.exists(target) and os.path.isfile(target):
        return FileResponse(target)
    # Default fallback to index.html
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="File not found")
