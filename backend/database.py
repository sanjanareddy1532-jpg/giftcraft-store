"""
GiftCard Platform - Database Initialization & ORM/Helper Layer
SQLite Database with rich catalog and order processing
"""

import sqlite3
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "giftcards.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        name_te TEXT NOT NULL,
        icon TEXT NOT NULL,
        description TEXT,
        badge TEXT
    )
    """)

    # Gift Cards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gift_cards (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        brand TEXT NOT NULL,
        category_id TEXT NOT NULL,
        description TEXT NOT NULL,
        description_te TEXT NOT NULL,
        discount_pct REAL DEFAULT 0.0,
        denominations TEXT NOT NULL, -- JSON list of numbers
        card_gradient TEXT NOT NULL,
        brand_color TEXT NOT NULL,
        logo_icon TEXT NOT NULL,
        rating REAL DEFAULT 4.8,
        total_reviews INTEGER DEFAULT 120,
        terms TEXT NOT NULL,
        redemption_guide TEXT NOT NULL,
        featured INTEGER DEFAULT 0,
        instant_delivery INTEGER DEFAULT 1,
        in_stock INTEGER DEFAULT 1,
        sales_count INTEGER DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    """)

    # Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        customer_name TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        customer_phone TEXT,
        recipient_name TEXT,
        recipient_email TEXT,
        card_id TEXT NOT NULL,
        denomination REAL NOT NULL,
        discount_amount REAL NOT NULL,
        final_price REAL NOT NULL,
        voucher_code TEXT NOT NULL,
        voucher_pin TEXT NOT NULL,
        gift_message TEXT,
        occasion TEXT,
        payment_method TEXT DEFAULT 'UPI',
        payment_status TEXT DEFAULT 'COMPLETED',
        is_redeemed INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (card_id) REFERENCES gift_cards (id)
    )
    """)

    # Coupons Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        code TEXT PRIMARY KEY,
        discount_pct REAL NOT NULL,
        max_discount REAL NOT NULL,
        min_order REAL NOT NULL,
        description TEXT
    )
    """)

    # Merchant Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchant_settings (
        id INTEGER PRIMARY KEY DEFAULT 1,
        merchant_name TEXT DEFAULT 'GiftCraft Store Owner',
        bank_name TEXT DEFAULT 'HDFC Bank',
        account_number TEXT DEFAULT '50100492817291',
        ifsc_code TEXT DEFAULT 'HDFC0001234',
        merchant_upi_id TEXT DEFAULT 'giftcraft@okhdfcbank',
        active_gateway TEXT DEFAULT 'Razorpay',
        settlement_cycle TEXT DEFAULT 'T+1 (Daily Auto-Credit at 8:00 AM)',
        razorpay_key_id TEXT DEFAULT 'rzp_test_YOUR_KEY_HERE',
        phonepe_merchant_id TEXT DEFAULT 'MERCHANTUAT',
        auto_settlement_enabled INTEGER DEFAULT 1
    )
    """)

    # Seed initial merchant row if empty
    cursor.execute("SELECT COUNT(*) FROM merchant_settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO merchant_settings (id) VALUES (1)")

    # Payout Settlements Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settlements (
        id TEXT PRIMARY KEY,
        amount REAL NOT NULL,
        bank_account TEXT NOT NULL,
        utr_ref TEXT NOT NULL,
        status TEXT DEFAULT 'SETTLED',
        settled_at TEXT NOT NULL
    )
    """)

    conn.commit()
    seed_data(conn)
    conn.close()

def seed_data(conn):
    cursor = conn.cursor()
    
    # Check if categories already exist
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] > 0:
        return

    # Seed Categories
    categories = [
        ("coupons", "Hot Promo Vouchers", "లక్ష్య డిస్కౌంట్ వోచర్లు (₹19 - ₹49)", "fa-tags", "Domino's, boAt, Flight, Audible, CCD, Derma Co", "FLASH SALE"),
        ("gaming", "Gaming & Esports", "గేమింగ్ & ఇ-స్పోర్ట్స్", "fa-gamepad", "Steam, PlayStation, Xbox, Roblox, BGMI", "HOT"),
        ("shopping", "Shopping & Retail", "షాపింగ్ & ఇ-కామర్స్", "fa-bag-shopping", "Amazon, Flipkart, Myntra, Nykaa, Ajio", "POPULAR"),
        ("entertainment", "Entertainment & OTT", "సినిమాలు & వినోదం", "fa-film", "Netflix, Spotify, BookMyShow, Hotstar", "TRENDING"),
        ("food", "Food & Dining", "ఆహారం & రెస్టారెంట్లు", "fa-utensils", "Zomato, Swiggy, Starbucks, Domino's", "BEST OFFERS"),
        ("travel", "Travel & Stay", "ట్రావెల్ & హోటల్స్", "fa-plane-departure", "MakeMyTrip, Uber, Airbnb, Cleartrip", "DEALS"),
        ("software", "Software & Utilities", "సాఫ్ట్‌వేర్ & సబ్‌స్క్రిప్షన్స్", "fa-laptop-code", "Google Play, Apple, Canva, Microsoft", "NEW")
    ]
    cursor.executemany("INSERT OR IGNORE INTO categories VALUES (?, ?, ?, ?, ?, ?)", categories)

    # Seed Coupons
    coupons = [
        ("WELCOME10", 10.0, 200.0, 500.0, "10% Flat OFF for New Users (Up to ₹200)"),
        ("AIDEAL5", 5.0, 300.0, 1000.0, "AI Recommended Special 5% Discount"),
        ("FESTIVE15", 15.0, 500.0, 1500.0, "Mega Festive Celebration 15% OFF")
    ]
    cursor.executemany("INSERT OR IGNORE INTO coupons VALUES (?, ?, ?, ?, ?)", coupons)

    # Seed 22+ Gift Cards
    cards = [
        # Gaming
        (
            "steam-wallet", "Steam Wallet Gift Card", "Valve Steam", "gaming",
            "Top-up your Steam account to purchase PC games, downloadable content, and in-game items across 50,000+ titles.",
            "50,000+ PC గేమ్‌లు, DLCలు మరియు ఇన్-గేమ్ ఐటెమ్‌ల కొనుగోలు కోసం మీ స్టీమ్ వాలెట్‌ను సులభంగా రీఛార్జ్ చేయండి.",
            5.0, json.dumps([250, 500, 1000, 2500, 5000]),
            "linear-gradient(135deg, #171a21 0%, #1b2838 50%, #2a475e 100%)",
            "#66c0f4", "fa-brands fa-steam", 4.9, 1420,
            "Valid for 1 year from purchase. Non-refundable. Applicable to Indian Steam Accounts in INR.",
            "1. Open Steam client or visit store.steampowered.com/account/redeemwalletcode. 2. Enter code. 3. Funds will instantly reflect in wallet.",
            1, 1, 1, 890
        ),
        (
            "playstation-store", "PlayStation Store Card", "Sony PlayStation", "gaming",
            "Get games, add-ons, subscriptions, and more for PS4 and PS5 directly from PlayStation Store.",
            "PS4 మరియు PS5 కన్సోల్‌లలో సరికొత్త గేమ్‌లు, PS Plus సబ్‌స్క్రిప్షన్‌ల కోసం ప్లేస్టేషన్ స్టోర్ కార్డ్.",
            6.0, json.dumps([500, 1000, 2000, 4000]),
            "linear-gradient(135deg, #003791 0%, #00225b 70%, #001233 100%)",
            "#0070d1", "fa-brands fa-playstation", 4.9, 940,
            "Valid for PSN India accounts. Code expires after 12 months.",
            "1. Sign in to PlayStation Network. 2. Go to 'Redeem Codes' in Store. 3. Enter 12-digit code.",
            1, 1, 1, 620
        ),
        (
            "xbox-game-pass", "Xbox Gift Card / Game Pass", "Microsoft Xbox", "gaming",
            "Buy full games, add-ons, or access 100+ high-quality titles with Game Pass on Xbox console and PC.",
            "Xbox మరియు PC గేమర్స్ కోసం Game Pass సబ్‌స్క్రిప్షన్ & లేటెస్ట్ గేమ్‌ల కొనుగోలుకు బెస్ట్ గిఫ్ట్.",
            7.0, json.dumps([499, 1000, 2500, 4999]),
            "linear-gradient(135deg, #107c10 0%, #0e5c0e 60%, #052605 100%)",
            "#107c10", "fa-brands fa-xbox", 4.8, 510,
            "Valid for Microsoft Xbox India accounts.",
            "1. Visit microsoft.com/redeem. 2. Enter 25-character Xbox code. 3. Enjoy gaming instantly.",
            0, 1, 1, 410
        ),
        (
            "roblox-card", "Roblox Robux Digital Card", "Roblox", "gaming",
            "Unlock Robux currency for avatar accessories, upgrades, game passes, and premium perks.",
            "పిల్లలు మరియు టీనేజర్లకు ఎంతో ఇష్టమైన రోబ్లాక్స్ అవతార్‌లు, ఐటెమ్స్ కోసం రోబక్స్ కార్డ్.",
            5.0, json.dumps([400, 800, 2000, 4000]),
            "linear-gradient(135deg, #e02424 0%, #991b1b 60%, #450a0a 100%)",
            "#e02424", "fa-solid fa-cube", 4.8, 730,
            "Valid worldwide. No expiration date.",
            "1. Go to roblox.com/redeem. 2. Log in and enter code. 3. Robux added to your balance.",
            0, 1, 1, 380
        ),
        (
            "bgmi-uc-voucher", "BGMI / Free Fire In-Game Voucher", "Krafton / Garena", "gaming",
            "Instant UC and Diamonds recharge for Battlegrounds Mobile India & Free Fire Max.",
            "మొబైల్ గేమర్స్ కోసం BGMI UC మరియు ఫ్రీ ఫైర్ డైమండ్స్ తక్షణ రీఛార్జ్ కోడ్.",
            8.0, json.dumps([100, 250, 500, 1000, 2500]),
            "linear-gradient(135deg, #d97706 0%, #78350f 70%, #292524 100%)",
            "#f59e0b", "fa-solid fa-crosshairs", 4.9, 1850,
            "Valid for Indian player IDs. Delivered within 30 seconds.",
            "1. Enter your Character ID on redeem portal. 2. Apply digital PIN. 3. UC/Diamonds credited.",
            1, 1, 1, 1200
        ),

        # Shopping
        (
            "amazon-pay", "Amazon Pay Gift Card", "Amazon India", "shopping",
            "Shop millions of products on Amazon India, pay utility bills, recharge mobile, order food, and book tickets.",
            "అమెజాన్‌లో లక్షలాది ప్రోడక్ట్స్ షాపింగ్, మొబైల్ రీఛార్జ్, కరెంట్ బిల్లుల చెల్లింపు కోసం ఆల్-ఇన్-వన్ గిఫ్ట్ కార్డ్.",
            4.0, json.dumps([250, 500, 1000, 2000, 5000, 10000]),
            "linear-gradient(135deg, #232f3e 0%, #131921 60%, #ff9900 100%)",
            "#ff9900", "fa-brands fa-amazon", 5.0, 3840,
            "Valid for 1 year from issuance. Can be combined with all ongoing Amazon offers and credit cards.",
            "1. Visit amazon.in/addgiftcard. 2. Sign in to your account. 3. Enter 16-digit gift card code and click 'Add to your balance'.",
            1, 1, 1, 2800
        ),
        (
            "flipkart-card", "Flipkart E-Gift Voucher", "Flipkart", "shopping",
            "Redeem on electronics, smartphones, fashion, home appliances, and groceries on Flipkart app & web.",
            "ఫ్లిప్‌కార్ట్‌లో ఎలక్ట్రానిక్స్, స్మార్ట్‌ఫోన్‌లు, దుస్తులు మరియు హోమ్ అప్లయన్సెస్ కోసం అద్భుతమైన వోచర్.",
            5.0, json.dumps([250, 500, 1000, 2500, 5000]),
            "linear-gradient(135deg, #2874f0 0%, #1e4bb8 60%, #ffe11b 100%)",
            "#2874f0", "fa-solid fa-cart-shopping", 4.9, 2400,
            "Valid for 12 months. Multiple gift cards can be merged during Flipkart checkout.",
            "1. In Flipkart checkout, select 'Gift Card' payment. 2. Enter 16-digit Card Number and 6-digit PIN.",
            1, 1, 1, 1950
        ),
        (
            "myntra-fashion", "Myntra Fashion Gift Card", "Myntra", "shopping",
            "Upgrade your wardrobe with top trending clothes, footwear, watches, and beauty essentials.",
            "ఫ్యాషన్ ప్రేమికుల కోసం మింత్రా బ్రాండెడ్ బట్టలు, షూస్ మరియు యాక్సెసరీలపై స్పెషల్ డిస్కౌంట్ వోచర్.",
            10.0, json.dumps([500, 1000, 2000, 3000, 5000]),
            "linear-gradient(135deg, #f43f5e 0%, #be123c 60%, #ff3f6c 100%)",
            "#ff3f6c", "fa-solid fa-shirt", 4.9, 1630,
            "Valid for 365 days. Stackable with seasonal sale coupons on Myntra.",
            "1. Go to Myntra Profile > Manage Gift Cards. 2. Enter Card Number & PIN. 3. Balance available instantly at checkout.",
            1, 1, 1, 1420
        ),
        (
            "nykaa-beauty", "Nykaa Cosmetics Voucher", "Nykaa", "shopping",
            "Pamper yourself with premium cosmetics, skincare, fragrances, and grooming products on Nykaa.",
            "నైకా ప్రీమియం కాస్మెటిక్స్, మేకప్, చర్మ సంరక్షణ మరియు బ్యూటీ ప్రోడక్ట్స్ కొనుగోలుకు బెస్ట్ గిఫ్ట్.",
            8.0, json.dumps([500, 1000, 2000, 5000]),
            "linear-gradient(135deg, #e11d48 0%, #9f1239 60%, #fc2779 100%)",
            "#fc2779", "fa-solid fa-wand-magic-sparkles", 4.8, 890,
            "Valid on Nykaa.com and Nykaa Man.",
            "1. Select Gift Card at checkout. 2. Enter Voucher Code & PIN. 3. Instant deduction.",
            0, 1, 1, 650
        ),
        (
            "ajio-trends", "AJIO Fashion Voucher", "AJIO Trends", "shopping",
            "Shop handpicked international brands and Indie ethnic collections with extra flat savings.",
            "లేటెస్ట్ ట్రెండీ బట్టలు మరియు ఇండియన్ ఎత్నిక్ వేర్ కోసం అజియో స్పెషల్ వోచర్.",
            12.0, json.dumps([500, 1000, 2000, 4000]),
            "linear-gradient(135deg, #334155 0%, #1e293b 70%, #e2e8f0 100%)",
            "#f59e0b", "fa-solid fa-vest-patches", 4.7, 720,
            "Valid across all AJIO web and mobile categories.",
            "1. Add items to bag. 2. In Payment page, enter AJIO Gift Voucher code and PIN.",
            0, 1, 1, 510
        ),

        # Entertainment
        (
            "netflix-card", "Netflix Digital Gift Card", "Netflix", "entertainment",
            "Stream unlimited movies, web series, and original shows in 4K HDR across TV, mobile, and laptop.",
            "నెట్‌ఫ్లిక్స్‌లో అన్‌లిమిటెడ్ సినిమాలు, లేటెస్ట్ వెబ్ సిరీస్‌లను 4Kలో ఎంజాయ్ చేయడానికి గిఫ్ట్ కార్డ్.",
            6.0, json.dumps([250, 500, 1000, 2000]),
            "linear-gradient(135deg, #000000 0%, #1c1c1c 60%, #e50914 100%)",
            "#e50914", "fa-solid fa-tv", 4.9, 2150,
            "Applicable to new or existing Netflix accounts in India. Credit never expires until used.",
            "1. Visit netflix.com/redeem. 2. Enter 11-digit PIN code. 3. Balance automatically covers monthly renewals.",
            1, 1, 1, 1800
        ),
        (
            "spotify-premium", "Spotify Premium Voucher", "Spotify", "entertainment",
            "Listen to ad-free music, download songs offline, and enjoy ultra high quality audio playback.",
            "యాడ్స్ లేకుండా నాన్‌స్టాప్ మ్యూజిక్, ఆఫ్‌లైన్ సాంగ్స్ డౌన్‌లోడ్ కోసం స్పాటిఫై ప్రీమియం వోచర్.",
            10.0, json.dumps([119, 389, 719, 1189]),
            "linear-gradient(135deg, #121212 0%, #191414 60%, #1db954 100%)",
            "#1db954", "fa-brands fa-spotify", 4.9, 1340,
            "Valid for Individual Premium plans. Codes are stackable up to 18 months.",
            "1. Go to spotify.com/redeem. 2. Log in and enter PIN code. 3. Premium activates immediately.",
            1, 1, 1, 980
        ),
        (
            "bookmyshow-card", "BookMyShow Movie Voucher", "BookMyShow", "entertainment",
            "Book tickets for latest blockbuster movies, live concerts, standup comedy, and sports events.",
            "సినిమా టిక్కెట్లు, లైవ్ షోలు, స్టాండప్ కామెడీ ఈవెంట్స్ కోసం బుక్‌మైషో సినిమా వోచర్.",
            10.0, json.dumps([250, 500, 1000, 2000]),
            "linear-gradient(135deg, #b91c1c 0%, #7f1d1d 70%, #dc2626 100%)",
            "#dc2626", "fa-solid fa-ticket", 4.8, 1120,
            "Valid on all cinemas and events in India for 1 year.",
            "1. Select your show & seats on BookMyShow. 2. Under 'Unlock Offers or Apply Promo', choose Gift Voucher and enter code.",
            0, 1, 1, 790
        ),
        (
            "youtube-premium", "YouTube Premium Voucher", "Google / YouTube", "entertainment",
            "Enjoy background play, ad-free video streaming, and YouTube Music Premium on all devices.",
            "యాడ్స్ లేని యూట్యూబ్ వీడియోలు, బ్యాక్‌గ్రౌండ్ ప్లే మరియు యూట్యూబ్ మ్యూజిక్ కోసం వోచర్.",
            7.0, json.dumps([129, 399, 799, 1290]),
            "linear-gradient(135deg, #272727 0%, #0f0f0f 70%, #ff0000 100%)",
            "#ff0000", "fa-brands fa-youtube", 4.8, 850,
            "Redeemable via Google Play balance on YouTube.",
            "1. Open YouTube app > Get YouTube Premium. 2. Select redeem code. 3. Enjoy ad-free video.",
            0, 1, 1, 620
        ),

        # Food & Dining
        (
            "zomato-card", "Zomato Food Voucher", "Zomato", "food",
            "Order gourmet meals, daily snacks, and desserts from thousands of top-rated restaurants with instant savings.",
            "జొమాటోలో మీకిష్టమైన బిర్యానీ, పిజ్జా మరియు ఫేవరెట్ రెస్టారెంట్ ఫుడ్ ఆర్డర్లకు స్పెషల్ డిస్కౌంట్.",
            8.0, json.dumps([100, 250, 500, 1000, 2000]),
            "linear-gradient(135deg, #e23744 0%, #991b1b 70%, #cb202d 100%)",
            "#cb202d", "fa-solid fa-bowl-food", 4.9, 2900,
            "Valid for 1 year. Can be used alongside Zomato Gold benefits.",
            "1. Open Zomato Profile > Claim Gift Card. 2. Enter 16-digit Code & PIN. 3. Balance applies at checkout automatically.",
            1, 1, 1, 2300
        ),
        (
            "swiggy-money", "Swiggy Money Voucher", "Swiggy", "food",
            "Use across Swiggy Food Delivery, Instamart Grocery, and Dineout dining bills.",
            "స్విగ్గీ ఫుడ్ డెలివరీ మరియు ఇన్‌స్టామార్ట్ గ్రోసరీ ఆర్డర్ల కోసం సులభమైన స్విగ్గీ మనీ వోచర్.",
            7.0, json.dumps([100, 250, 500, 1000, 2000]),
            "linear-gradient(135deg, #fc8019 0%, #c2410c 70%, #7c2d12 100%)",
            "#fc8019", "fa-solid fa-motorcycle", 4.9, 2480,
            "Instant transfer to Swiggy Money wallet balance. Valid for 1 year.",
            "1. Open Swiggy > Account > Swiggy Money. 2. Tap 'Add Gift Card'. 3. Enter Card Number & PIN.",
            1, 1, 1, 1920
        ),
        (
            "dominos-card", "Domino's Pizza Voucher", "Domino's Pizza", "food",
            "Relish cheesy hot pizzas, garlic breads, pastas, and choco lava cakes with mega discounts.",
            "పిజ్జా లవర్స్ కోసం డొమినోస్ హాట్ పిజ్జాలు, చీజ్ బ్రెడ్స్‌పై 15% సూపర్ సేవింగ్స్ వోచర్.",
            15.0, json.dumps([200, 500, 1000, 2000]),
            "linear-gradient(135deg, #006491 0%, #004d70 60%, #e31837 100%)",
            "#006491", "fa-solid fa-pizza-slice", 4.9, 1750,
            "Valid on Domino's Mobile App and store dine-in.",
            "1. Add pizzas to cart on Dominos app. 2. In Payments, select 'Evoucher'. 3. Enter voucher code.",
            1, 1, 1, 1450
        ),
        (
            "starbucks-card", "Starbucks Coffee Card", "Starbucks", "food",
            "Savor freshly brewed artisanal coffee, iced frappuccinos, and delicious bakery treats at Starbucks.",
            "స్టార్‌బక్స్ కాఫీ, ఫ్రాపుచినో మరియు రుచికరమైన బేకరీ ఐటెమ్స్ కోసం లగ్జరీ గిఫ్ట్ కార్డ్.",
            10.0, json.dumps([250, 500, 1000, 2500]),
            "linear-gradient(135deg, #006241 0%, #00422c 70%, #1e3932 100%)",
            "#006241", "fa-solid fa-mug-hot", 4.8, 980,
            "Valid across all Starbucks India outlets and mobile order app.",
            "1. Show code at Starbucks cashier or link to Starbucks India App. 2. Scan barcode to pay.",
            0, 1, 1, 710
        ),

        # Travel
        (
            "makemytrip-card", "MakeMyTrip Holiday Voucher", "MakeMyTrip", "travel",
            "Book flight tickets, luxury hotels, homestays, and holiday packages across India and worldwide.",
            "విమాన టిక్కెట్లు, హోటల్స్ మరియు ఫ్యామిలీ ట్రిప్పుల కోసం మేక్‌మైట్రిప్ అద్భుతమైన గిఫ్ట్ కార్డ్.",
            6.0, json.dumps([1000, 2500, 5000, 10000, 25000]),
            "linear-gradient(135deg, #d32f2f 0%, #b71c1c 60%, #0288d1 100%)",
            "#d32f2f", "fa-solid fa-plane", 4.9, 870,
            "Stackable with ongoing MakeMyTrip bank discount codes. Valid for 12 months.",
            "1. Select Flight/Hotel on MakeMyTrip. 2. In Payment page, select 'Gift Card'. 3. Enter 16-digit card number and PIN.",
            1, 1, 1, 640
        ),
        (
            "uber-voucher", "Uber Ride & Eats Pass", "Uber", "travel",
            "Enjoy hassle-free cab rides, auto trips, intercity travel, or food deliveries with Uber Cash balance.",
            "రోజువారీ క్యాబ్ జర్నీలు, ఆటో రైడ్స్ కోసం సులువైన ఊబర్ క్యాష్ గిఫ్ట్ కార్డ్.",
            5.0, json.dumps([200, 500, 1000, 2500]),
            "linear-gradient(135deg, #000000 0%, #1c1c1c 70%, #22c55e 100%)",
            "#000000", "fa-solid fa-taxi", 4.8, 1420,
            "Adds directly to your Uber Cash wallet. Valid across India.",
            "1. Open Uber app > Account > Wallet. 2. Tap 'Add Funds' > 'Gift Card'. 3. Enter Code.",
            0, 1, 1, 930
        ),

        # Software & App Stores
        (
            "google-play-card", "Google Play Recharge Code", "Google Play", "software",
            "Buy millions of Android apps, games, ebooks, movies, and in-game currencies seamlessly.",
            "ఆండ్రాయిడ్ యాప్స్, గేమ్‌లు, మూవీస్ మరియు ఇన్-గేమ్ కొనుగోళ్ల కోసం గూగుల్ ప్లే రీఛార్జ్ కోడ్.",
            4.0, json.dumps([100, 250, 500, 1000, 2500, 5000]),
            "linear-gradient(135deg, #01875f 0%, #0b57d0 50%, #ea4335 100%)",
            "#01875f", "fa-brands fa-google-play", 5.0, 3100,
            "Valid for Indian Google Play Store accounts. Never expires.",
            "1. Open Google Play Store > Tap Profile icon. 2. Tap Payments & subscriptions > Redeem code. 3. Enter code.",
            1, 1, 1, 2400
        ),
        (
            "apple-gift-card", "Apple Gift Card (App Store & iTunes)", "Apple", "software",
            "Spend on iPhone apps, iCloud+ storage, Apple Music, games, movies, and subscriptions.",
            "ఐఫోన్ యాప్స్, ఐక్లౌడ్ స్టోరేజ్, ఆపిల్ మ్యూజిక్ సబ్‌స్క్రిప్షన్‌ల కోసం ఆపిల్ గిఫ్ట్ కార్డ్.",
            4.0, json.dumps([250, 500, 1000, 2500, 5000]),
            "linear-gradient(135deg, #374151 0%, #111827 70%, #9ca3af 100%)",
            "#a855f7", "fa-brands fa-apple", 4.9, 1780,
            "Redeem to Apple ID balance in India. Valid on App Store & Mac App Store.",
            "1. Open App Store on iPhone/iPad/Mac. 2. Tap account profile > Redeem Gift Card. 3. Enter code manually or scan.",
            1, 1, 1, 1310
        ),
        (
            "canva-pro-voucher", "Canva Pro Subscription Voucher", "Canva", "software",
            "Unlock 100+ million premium photos, graphics, brand kits, AI tools, and background remover.",
            "గ్రాఫిక్ డిజైనర్స్, యూట్యూబర్స్ కోసం కాన్వా ప్రో ప్రీమియం టూల్స్, AI ఫీచర్స్ వోచర్.",
            12.0, json.dumps([499, 999, 1999, 3999]),
            "linear-gradient(135deg, #7d2ae8 0%, #00c4cc 100%)",
            "#00c4cc", "fa-solid fa-palette", 4.9, 610,
            "Valid for individual Canva account upgrades.",
            "1. Go to canva.com/redeem. 2. Paste digital key. 3. Pro unlocks for selected duration.",
            0, 1, 1, 480
        ),

        # User's Special Discount Vouchers (Direct Cash Inflow)
        (
            "dominos-33off-voucher", "Domino's 33% OFF + Rs.50 Cashback Code", "Domino's Pizza", "coupons",
            "Flat 33% discount + extra Rs.50 cashback code on delicious Domino's pizza orders. Instant code sent to your WhatsApp!",
            "డొమినోస్ పిజ్జా ఆర్డర్లపై ఫ్లాట్ 33% డిస్కౌంట్ + రూ. 50 క్యాష్‌బ్యాక్ ప్రోమో కోడ్. కేవలం ₹25 కే పొందండి!",
            0.0, json.dumps([25]),
            "linear-gradient(135deg, #006491 0%, #004d70 60%, #e31837 100%)",
            "#e31837", "fa-solid fa-pizza-slice", 5.0, 480,
            "Valid on Domino's Mobile App and Website for all users.",
            "1. Apply Promo Code under Offers on Domino's app. 2. 33% discount + Rs.50 cashback is automatically applied.",
            1, 1, 1, 950
        ),
        (
            "boat-500off-voucher", "boAt Lifestyle Rs.500 OFF Voucher", "boAt Lifestyle", "coupons",
            "Flat Rs.500 OFF promo voucher code for boAt earbuds, smartwatches, and headphones on official website.",
            "బోట్ ఇయర్‌బడ్స్, స్మార్ట్‌వాచ్‌లు మరియు హెడ్‌ఫోన్స్‌పై రూ. 500 ఫ్లాట్ డిస్కౌంట్ వోచర్ కోడ్. కేవలం ₹29 కే!",
            0.0, json.dumps([29]),
            "linear-gradient(135deg, #e11d48 0%, #9f1239 60%, #111827 100%)",
            "#e11d48", "fa-solid fa-headphones", 4.9, 620,
            "Valid on boAt official website (boat-lifestyle.com).",
            "1. Add any boAt product to cart. 2. Enter code in promo code field at checkout for Rs.500 instant discount.",
            1, 1, 1, 1120
        ),
        (
            "flight-600off-voucher", "Flight Ticket Rs.600 OFF Discount Code", "Flight Booking", "coupons",
            "Save up to Rs.600 directly on domestic & international flight ticket bookings with this special promo code.",
            "విమాన టిక్కెట్ బుకింగ్స్ పై రూ. 600 వరకు తక్షణ తగ్గింపు కోడ్. ట్రావెల్ ప్రియుల కోసం కేవలం ₹29 కే!",
            0.0, json.dumps([29]),
            "linear-gradient(135deg, #0284c7 0%, #0369a1 60%, #0c4a6e 100%)",
            "#0284c7", "fa-solid fa-plane-departure", 4.8, 310,
            "Applicable on flight booking portals across domestic flights.",
            "1. Select flight tickets. 2. Enter voucher code under Promo Codes during payment page to get up to Rs.600 off.",
            1, 1, 1, 430
        ),
        (
            "audible-2m-voucher", "Audible 2 Months Free Premium Membership", "Amazon Audible", "coupons",
            "Unlock 2 full months of free Audible Premium audiobook membership and access 200,000+ top titles.",
            "అమెజాన్ ఆడబుల్ 2 నెలల ప్రీమియం ఆడియోబుక్ మెంబర్‌షిప్ వోచర్ కోడ్. పుస్తకాలు వినేవారి కోసం కేవలం ₹19 కే!",
            0.0, json.dumps([19]),
            "linear-gradient(135deg, #f59e0b 0%, #d97706 60%, #78350f 100%)",
            "#f59e0b", "fa-solid fa-book-open-reader", 4.9, 540,
            "Valid for all Amazon Audible users.",
            "1. Visit audible.in/ep/redeem. 2. Enter promo code. 3. 2 months free membership activates immediately.",
            1, 1, 1, 780
        ),
        (
            "ccd-600off-voucher", "Cafe Coffee Day (CCD) Rs.600 OFF Code", "Cafe Coffee Day", "coupons",
            "Enjoy up to Rs.600 OFF on delicious artisanal coffees, frappes, and snacks at Cafe Coffee Day outlets.",
            "కేఫ్ కాఫీ డే (CCD) లో కాఫీలు మరియు స్నాక్స్‌పై రూ. 600 వరకు ఆదా చేసే స్పెషల్ వోచర్ కోడ్. కేవలం ₹25 కే!",
            0.0, json.dumps([25]),
            "linear-gradient(135deg, #b91c1c 0%, #881337 60%, #4c0519 100%)",
            "#b91c1c", "fa-solid fa-mug-saucer", 4.8, 290,
            "Valid across Cafe Coffee Day outlets and app orders.",
            "1. Show code at CCD counter or enter on CCD app before payment.",
            0, 1, 1, 360
        ),
        (
            "derma-100cb-voucher", "The Derma Co 100% Cashback Voucher Code", "The Derma Co", "coupons",
            "Get 100% cashback on skincare, sunscreens, and dermatological cosmetics on orders above Rs.899.",
            "డెర్మా కో స్కిన్‌కేర్, సన్‌స్క్రీన్ మరియు బ్యూటీ ప్రోడక్ట్స్‌పై 100% క్యాష్‌బ్యాక్ వోచర్ కోడ్. కేవలం ₹19 కే!",
            0.0, json.dumps([19]),
            "linear-gradient(135deg, #0d9488 0%, #0f766e 60%, #115e59 100%)",
            "#0d9488", "fa-solid fa-pump-soap", 4.9, 410,
            "Valid on thedermaco.com official online store.",
            "1. Add skincare products to cart on thedermaco.com. 2. Apply coupon code at checkout.",
            0, 1, 1, 520
        ),
        (
            "train-50off-voucher", "IRCTC Train Tickets Rs.50 OFF Discount Code", "Train Booking", "coupons",
            "Instant flat Rs.50 discount voucher code for train ticket bookings across India.",
            "రైలు టికెట్ బుకింగ్స్ పై రూ. 50 ఫ్లాట్ డిస్కౌంట్ వోచర్ కోడ్. కేవలం ₹15 కే!",
            0.0, json.dumps([15]),
            "linear-gradient(135deg, #1e3a8a 0%, #172554 60%, #0f172a 100%)",
            "#1e3a8a", "fa-solid fa-train-subway", 4.7, 850,
            "Valid on train ticket booking app checkout.",
            "1. Book train tickets. 2. Apply promo code on payment page.",
            0, 1, 1, 670
        )
    ]
    
    cursor.executemany("""
    INSERT INTO gift_cards (
        id, name, brand, category_id, description, description_te,
        discount_pct, denominations, card_gradient, brand_color,
        logo_icon, rating, total_reviews, terms, redemption_guide,
        featured, instant_delivery, in_stock, sales_count
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cards)

    conn.commit()

def get_all_cards(category: Optional[str] = None, search: Optional[str] = None, sort_by: str = "popular") -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM gift_cards WHERE in_stock = 1"
    params = []

    if category and category.lower() != "all":
        query += " AND category_id = ?"
        params.append(category.lower())

    if search:
        search_term = f"%{search.lower()}%"
        query += " AND (LOWER(name) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(description) LIKE ? OR LOWER(description_te) LIKE ?)"
        params.extend([search_term, search_term, search_term, search_term])

    if sort_by == "discount":
        query += " ORDER BY discount_pct DESC"
    elif sort_by == "rating":
        query += " ORDER BY rating DESC"
    elif sort_by == "price_low":
        query += " ORDER BY discount_pct DESC" # can adjust
    else: # popular / sales
        query += " ORDER BY sales_count DESC, rating DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cards = []
    for r in rows:
        d = dict(r)
        d["denominations"] = json.loads(d["denominations"])
        cards.append(d)
    conn.close()
    return cards

def get_card_by_id(card_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gift_cards WHERE id = ?", (card_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["denominations"] = json.loads(d["denominations"])
        return d
    return None

def get_categories() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT c.*, COUNT(g.id) as card_count FROM categories c LEFT JOIN gift_cards g ON c.id = g.category_id GROUP BY c.id")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_order(
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    recipient_name: str,
    recipient_email: str,
    card_id: str,
    denomination: float,
    discount_amount: float,
    final_price: float,
    gift_message: str = "",
    occasion: str = "General",
    payment_method: str = "UPI"
) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()

    order_id = f"GC-ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    # Generate realistic 16-digit voucher code e.g. 5839-2940-1094-8271 and 4-digit PIN
    code_raw = f"{uuid.uuid4().int % 10**16:016d}"
    voucher_code = f"{code_raw[0:4]}-{code_raw[4:8]}-{code_raw[8:12]}-{code_raw[12:16]}"
    voucher_pin = f"{(uuid.uuid4().int % 10000):04d}"
    created_at = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO orders (
        id, customer_name, customer_email, customer_phone,
        recipient_name, recipient_email, card_id, denomination,
        discount_amount, final_price, voucher_code, voucher_pin,
        gift_message, occasion, payment_method, payment_status,
        is_redeemed, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (
        order_id, customer_name, customer_email, customer_phone,
        recipient_name or customer_name, recipient_email or customer_email,
        card_id, denomination, discount_amount, final_price,
        voucher_code, voucher_pin, gift_message, occasion,
        payment_method, "COMPLETED", created_at
    ))

    # Update card sales count
    cursor.execute("UPDATE gift_cards SET sales_count = sales_count + 1 WHERE id = ?", (card_id,))

    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "recipient_name": recipient_name or customer_name,
        "recipient_email": recipient_email or customer_email,
        "card_id": card_id,
        "denomination": denomination,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "voucher_code": voucher_code,
        "voucher_pin": voucher_pin,
        "gift_message": gift_message,
        "occasion": occasion,
        "payment_method": payment_method,
        "payment_status": "COMPLETED",
        "created_at": created_at
    }

def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT o.*, g.name as card_name, g.brand, g.logo_icon, g.card_gradient, g.redemption_guide, g.terms
    FROM orders o
    JOIN gift_cards g ON o.card_id = g.id
    WHERE o.id = ?
    """, (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_recent_orders(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT o.*, g.name as card_name, g.brand, g.logo_icon
    FROM orders o
    JOIN gift_cards g ON o.card_id = g.id
    ORDER BY o.created_at DESC LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def check_card_balance(code_or_order: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cleaned = code_or_order.strip().upper()
    cursor.execute("""
    SELECT o.*, g.name as card_name, g.brand
    FROM orders o
    JOIN gift_cards g ON o.card_id = g.id
    WHERE o.voucher_code = ? OR o.id = ?
    """, (cleaned, cleaned))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_admin_stats() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(final_price), 0), COALESCE(SUM(discount_amount), 0) FROM orders")
    order_count, total_revenue, total_savings = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM gift_cards")
    total_cards = cursor.fetchone()[0]

    cursor.execute("""
    SELECT g.name, g.brand, g.sales_count, g.discount_pct, g.category_id
    FROM gift_cards g
    ORDER BY g.sales_count DESC LIMIT 5
    """)
    top_sellers = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_orders": order_count,
        "total_revenue": round(total_revenue, 2),
        "total_savings": round(total_savings, 2),
        "total_cards": total_cards,
        "top_sellers": top_sellers
    }

def get_merchant_settings() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM merchant_settings WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}

def update_merchant_settings(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE merchant_settings SET
        merchant_name = ?,
        bank_name = ?,
        account_number = ?,
        ifsc_code = ?,
        merchant_upi_id = ?,
        active_gateway = ?,
        razorpay_key_id = ?,
        phonepe_merchant_id = ?
    WHERE id = 1
    """, (
        data.get("merchant_name", "GiftCraft Store Owner"),
        data.get("bank_name", "HDFC Bank"),
        data.get("account_number", "50100492817291"),
        data.get("ifsc_code", "HDFC0001234"),
        data.get("merchant_upi_id", "giftcraft@okhdfcbank"),
        data.get("active_gateway", "Razorpay"),
        data.get("razorpay_key_id", "rzp_test_YOUR_KEY_HERE"),
        data.get("phonepe_merchant_id", "MERCHANTUAT")
    ))
    conn.commit()
    conn.close()
    return get_merchant_settings()

def get_settlements_history() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settlements ORDER BY settled_at DESC LIMIT 10")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    if not rows:
        # Generate sample recent automated settlements for illustration
        return [
            {
                "id": "SETTL-20261027-01",
                "amount": 28450.00,
                "bank_account": "HDFC Bank (A/C: ****7291)",
                "utr_ref": "UTR2026102709182390",
                "status": "COMPLETED & CREDITED",
                "settled_at": "Yesterday at 08:00 AM (T+1 Settlement)"
            },
            {
                "id": "SETTL-20261026-02",
                "amount": 42100.00,
                "bank_account": "HDFC Bank (A/C: ****7291)",
                "utr_ref": "UTR2026102608149102",
                "status": "COMPLETED & CREDITED",
                "settled_at": "26 Oct 2026 at 08:00 AM (T+1 Settlement)"
            }
        ]
    return rows

# Initialize on module load
init_db()
