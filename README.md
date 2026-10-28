# 🎁 GiftCraft AI - All-in-One AI Gift Card Marketplace
> **అన్ని రకాల గిఫ్ట్ కార్డ్‌లు కొనుగోలు చేయడానికి అత్యాధునిక AI సేల్స్ ప్లాట్‌ఫారమ్**

**GiftCraft AI** is a full-stack, production-ready gift card e-commerce marketplace powered by an embedded AI Sales Concierge (**GiftGenie AI**). The platform supports all major gift card categories (Gaming, Shopping, Entertainment/OTT, Food & Dining, Travel, Software & App Stores) and offers instant digital voucher generation with realistic scratch-to-reveal delivery.

---

## 🌟 Key Features

### 1. 🤖 AI Sales Concierge ("GiftGenie AI")
- **Bilingual & Natural Language Support**: Speaks fluently in **Telugu (తెలుగు)**, **English**, and **Telugish**!
- **Intelligent Gifting Matcher**: Analyzes recipient (Friend, Brother, Sister, Gamer, Mom/Dad), occasion (Birthday, Anniversary, Diwali, etc.), and budget (e.g. under ₹500, ₹1000, ₹2500) to recommend the highest-value cards.
- **In-Chat Direct Selling**: Recommends cards with 1-click **"Buy Now"** action buttons inside the chat bubble.
- **AI Greeting Wish Generator**: Automatically writes heartfelt, personalized wishes to accompany the gift card.
- **Voice Support**: Integrated speech recognition (Microphone) and text-to-speech audio readout.

### 2. 💳 22+ Top Global & Indian Gift Card Brands
- **Gaming & Esports**: Steam Wallet, Sony PlayStation Store, Xbox Game Pass, Google Play, Roblox Robux, BGMI / Free Fire.
- **Shopping & Retail**: Amazon Pay, Flipkart, Myntra Fashion, Nykaa Beauty, AJIO Trends.
- **Entertainment & OTT**: Netflix, Spotify Premium, BookMyShow Movies, YouTube Premium.
- **Food & Dining**: Zomato, Swiggy Money, Domino's Pizza (15% OFF), Starbucks Coffee.
- **Travel & Mobility**: MakeMyTrip Holidays & Flights, Uber Ride Pass.
- **Software & Utilities**: Apple Gift Card (App Store), Google Play, Canva Pro.

### 3. ⚡ Instant Digital Code Delivery & Scratch Card Experience
- **16-Digit Voucher Code & 4-Digit PIN**: Generates authentic digital voucher codes upon checkout.
- **Interactive Scratch-to-Reveal**: Interactive canvas where users can scratch off the digital surface with their mouse/touch to unveil the code!
- **1-Click Copy & Print Voucher**: Print-ready voucher slip with redemption instructions.

### 4. 💰 Instant Discounts & Coupon Engine
- Built-in brand discounts (up to 15% flat off).
- Promo coupon codes:
  - `WELCOME10`: 10% Flat OFF for new users.
  - `AIDEAL5`: 5% Special AI Discount.
  - `FESTIVE15`: 15% Mega Festive Savings.

### 5. 📊 Real-Time Admin Dashboard & Balance Checker
- Track total orders, revenue, customer savings, and top-selling gift cards.
- Built-in voucher balance and validity checker.

---

## 🚀 Quick Start Guide

### Running the Application
From the project folder, simply run:

```powershell
cd d:\Image\giftcard_platform
python run.py
```

The script will automatically:
1. Detect an available local port (e.g. `http://127.0.0.1:8000`).
2. Initialize the SQLite database with full catalog & seed data.
3. Launch the FastAPI server.
4. Open the web marketplace directly in your default browser!

---

## 🏗️ Architecture & Project Structure

```
d:\Image\giftcard_platform\
├── backend\
│   ├── database.py       # SQLite database schema, 22+ gift cards, order processing
│   ├── ai_engine.py      # GiftGenie AI sales agent engine (Telugu + English NLP)
│   └── server.py         # FastAPI REST API & static file router
├── frontend\
│   ├── index.html        # Glassmorphic, responsive single-page web app
│   ├── style.css         # Modern styling, realistic 3D card visual, animations
│   └── app.js            # Frontend state, chat, checkout, scratch canvas, i18n
├── data\
│   └── giftcards.db      # SQLite database (auto-created on first run)
├── run.py                # Single-click launcher script with browser auto-open
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/api/cards` | Retrieve all gift cards with category & search filter |
| `GET` | `/api/categories` | Retrieve all categories with counts |
| `POST` | `/api/chat` | AI Sales Concierge message endpoint (Telugu/English) |
| `POST` | `/api/checkout` | Process order and generate 16-digit voucher & PIN |
| `POST` | `/api/generate-message`| AI personalized greeting card wish generator |
| `POST` | `/api/coupon/validate`| Validate promo discount coupons |
| `POST` | `/api/check-balance`| Verify gift card voucher balance and validity |
| `GET` | `/api/admin/stats` | Admin platform sales analytics |
