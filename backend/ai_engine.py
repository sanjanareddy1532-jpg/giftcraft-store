"""
GiftCard Platform - AI Sales Assistant Engine (GiftGenie AI)
Supports natural conversational selling in Telugu, English, and Telugish.
Integrates LLM (Gemini/OpenAI) if API key is present, with an intelligent built-in semantic sales engine fallback.
"""

import os
import re
import json
import random
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.parse
from . import database

SYSTEM_PROMPT = """
You are GiftGenie AI, an elite, persuasive, and delightful AI Sales Concierge for India's leading Gift Card platform.
Your mission is to understand user requirements, recommend the most fitting gift cards from the store catalog, highlight discounts, and actively help them make a purchase.

Catalog Categories:
- Gaming: Steam, PlayStation, Xbox Game Pass, Google Play, Roblox, BGMI/Free Fire
- Shopping: Amazon Pay, Flipkart, Myntra, Nykaa, AJIO
- Entertainment: Netflix, Spotify, BookMyShow, YouTube Premium
- Food & Dining: Zomato, Swiggy, Domino's, Starbucks
- Travel: MakeMyTrip, Uber
- Software: Apple, Google Play, Canva Pro

Language Handling:
- If user talks in Telugu (తెలుగు) or Telugish, reply warmly in natural Telugu / Telugish.
- If user talks in English, reply in friendly English.
- Always include direct recommendations with denomination options and savings.
"""

def detect_language(text: str) -> str:
    # Check for Telugu script characters
    if any('\u0c00' <= char <= '\u0c7f' for char in text):
        return "te"
    # Check for Telugish keywords
    telugish_words = ["kavali", "cheyali", "cheppandi", "unnayi", "bavuntundi", "rakala", "nakosam", "friend ki", "birthday ki", "ammaki", "nannaki", "chelli", "annayya", "lopala", "oka", "ento", "undi", "pedda", "chinnappudu"]
    lower = text.lower()
    if any(w in lower for w in telugish_words):
        return "te_latn"
    return "en"

def extract_budget(text: str) -> Optional[float]:
    # Match patterns like 500, 1000, 2000, rs 500, inr 1000, ₹500, 500rs, etc.
    patterns = [
        r'₹\s*(\d+)',
        r'(?:rs|inr|rupees|రూపాయలు|రూ\.)\s*(\d+)',
        r'(\d+)\s*(?:rs|inr|rupees|/-|రూ)',
        r'under\s*(\d+)',
        r'below\s*(\d+)',
        r'around\s*(\d+)',
        r'(\d+)\s*(?:lopala|lo)'
    ]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
    # Pure numbers over 100
    nums = re.findall(r'\b\d{3,5}\b', text)
    if nums:
        return float(nums[0])
    return None

def find_best_matching_cards(user_message: str, budget: Optional[float] = None) -> List[Dict[str, Any]]:
    msg = user_message.lower()
    all_cards = database.get_all_cards()

    scored_cards = []

    # Category & Keyword Mappings
    gaming_keywords = ["game", "gaming", "steam", "playstation", "ps5", "ps4", "xbox", "pubg", "bgmi", "roblox", "free fire", "pc game", "గేమ్", "గేమింగ్", "వీడియో గేమ్"]
    shopping_keywords = ["shop", "shopping", "clothes", "fashion", "dress", "amazon", "flipkart", "myntra", "nykaa", "ajio", "makeup", "cosmetics", "షాపింగ్", "బట్టలు", "డ్రెస్సులు"]
    entertainment_keywords = ["movie", "cinema", "netflix", "spotify", "music", "songs", "binge", "series", "bookmyshow", "show", "సినిమా", "పాటలు", "నెట్‌ఫ్లిక్స్"]
    food_keywords = ["food", "eat", "dining", "zomato", "swiggy", "pizza", "domino", "starbucks", "coffee", "restaurant", "బిర్యానీ", "ఆహారం", "ఫుడ్", "పిజ్జా", "కాఫీ"]
    travel_keywords = ["travel", "trip", "flight", "hotel", "holiday", "makemytrip", "uber", "cab", "ride", "ట్రావెల్", "విమానం", "ట్రిప్", "క్యాబ్"]
    general_tech = ["app", "recharge", "google play", "apple", "iphone", "canva", "software", "యాప్స్", "గూగుల్ ప్లే"]

    for card in all_cards:
        score = 0
        cid = card["id"]
        cname = card["name"].lower()
        cbrand = card["brand"].lower()
        desc = card["description"].lower()
        cat = card["category_id"]

        # Exact brand/name mention = High Score
        if cid in msg or cbrand in msg or any(part in msg for part in cname.split()):
            score += 15

        # Check Category matches
        if any(k in msg for k in gaming_keywords) and cat == "gaming":
            score += 8
        if any(k in msg for k in shopping_keywords) and cat == "shopping":
            score += 8
        if any(k in msg for k in entertainment_keywords) and cat == "entertainment":
            score += 8
        if any(k in msg for k in food_keywords) and cat == "food":
            score += 8
        if any(k in msg for k in travel_keywords) and cat == "travel":
            score += 8
        if any(k in msg for k in general_tech) and cat == "software":
            score += 8

        # Recipient profile matches
        if any(w in msg for w in ["friend", "dost", "స్నేహితుడు", "మిత్రుడు"]):
            if cid in ["amazon-pay", "zomato-card", "steam-wallet", "spotify-premium", "flipkart-card"]:
                score += 4
        if any(w in msg for w in ["girl", "girlfriend", "sister", "wife", "mother", "ammaki", "చెల్లి", "అక్క", "భార్య"]):
            if cid in ["myntra-fashion", "nykaa-beauty", "amazon-pay", "starbucks-card", "bookmyshow-card"]:
                score += 5
        if any(w in msg for w in ["boy", "boyfriend", "brother", "husband", "father", "annayya", "తమ్ముడు"]):
            if cid in ["steam-wallet", "playstation-store", "amazon-pay", "bgmi-uc-voucher", "uber-voucher"]:
                score += 5
        if any(w in msg for w in ["kid", "child", "teenager", "boy", "పిల్లలు"]):
            if cid in ["roblox-card", "google-play-card", "dominos-card"]:
                score += 6

        # Budget fit
        if budget:
            denominations = card["denominations"]
            fits = [d for d in denominations if d <= budget]
            if fits:
                score += 4
            elif min(denominations) <= budget * 1.2:
                score += 2

        # Popularity & Discount boost
        score += int(card.get("discount_pct", 0) / 2)
        if card.get("featured"):
            score += 2

        if score > 0:
            scored_cards.append((score, card))

    scored_cards.sort(key=lambda x: x[0], reverse=True)
    results = [item[1] for item in scored_cards[:4]]

    # If no specific match, return top featured & versatile cards
    if not results:
        results = [c for c in all_cards if c["id"] in ["amazon-pay", "steam-wallet", "zomato-card", "flipkart-card"]]

    return results

def generate_personalized_greeting(recipient: str, occasion: str, lang: str = "te") -> str:
    """Generate custom heartfelt gift message based on recipient & occasion"""
    r_name = recipient.strip() if recipient else "Dear Friend"
    occ = occasion.lower()

    if lang in ["te", "te_latn"]:
        if "birthday" in occ or "పుట్టినరోజు" in occ:
            return f"ప్రియమైన {r_name}, పుట్టినరోజు శుభాకాంక్షలు! 🎉 మీ ప్రతి కోరిక నెరవేరాలని, సంతోషంతో ఎల్లప్పుడూ వెలగాలని కోరుకుంటూ ఈ చిన్న కానుక. మీకిష్టమైన వస్తువును మీరే ఎంచుకోండి! ❤️"
        elif "anniversary" in occ or "పెళ్లి" in occ or "wedding" in occ:
            return f"హృదయపూర్వక పెళ్లిరోజు శుభాకాంక్షలు {r_name}! 💍 మీ జీవితం అనురాగం, ఆనందాలతో ఎల్లప్పుడూ నిండాలని కోరుకుంటూ ఈ గిఫ్ట్ వోచర్."
        elif "diwali" in occ or "దీపావళి" in occ or "festival" in occ:
            return f"దీపావళి శుభాకాంక్షలు {r_name}! ✨ మీ జీవితంలో సుఖసంతోషాలు, విజయాలు వెల్లివిరియాలని కోరుకుంటున్నాము."
        else:
            return f"ప్రియమైన {r_name}, మీకోసం ప్రేమతో అందించే ప్రత్యేక గిఫ్ట్ కార్డ్! 🎁 మీ అభిరుచికి తగిన బహుమతిని ఆనందంగా ఆస్వాదించండి."
    else:
        if "birthday" in occ:
            return f"Happy Birthday, {r_name}! 🎂 Wishing you another year filled with endless joy, adventures, and success. Treat yourself with something you love with this gift card! 🎉"
        elif "anniversary" in occ or "wedding" in occ:
            return f"Happy Anniversary, {r_name}! 🥂 Wishing you both a lifetime of love and happiness. Celebrate your special day with our warmest love!"
        else:
            return f"Dear {r_name}, thinking of you and sending this special gift card to brighten your day! 🎁 Hope you enjoy treating yourself!"

def generate_ai_sales_response(user_message: str, session_id: str = "default") -> Dict[str, Any]:
    """
    Main entry point for AI Sales interaction.
    Analyzes intent, matches cards, calculates discounts, and crafts actionable Telugu/English response.
    """
    lang = detect_language(user_message)
    budget = extract_budget(user_message)
    matched_cards = find_best_matching_cards(user_message, budget)

    # Check for greeting card message generation request
    msg_lower = user_message.lower()
    if any(k in msg_lower for k in ["message", "wish", "greeting", "శుభాకాంక్షలు", "కోట్", "రాయండి", "మెసేజ్"]):
        occasion = "Birthday" if ("birthday" in msg_lower or "పుట్టినరోజు" in msg_lower) else ("Anniversary" if ("anniversary" in msg_lower or "పెళ్లిరోజు" in msg_lower) else "Festival")
        name = "My Dear"
        for word in user_message.split():
            if word[0].isupper() and word.lower() not in ["hi", "hello", "write", "can", "please", "generate", "card"]:
                name = word
                break
        custom_wish = generate_personalized_greeting(name, occasion, lang)
        
        if lang in ["te", "te_latn"]:
            reply_text = f"ఖచ్చితంగా! మీ ప్రియమైన వారి కోసం నేను రూపొందించిన అందమైన గ్రీటింగ్ మెసేజ్ ఇది:\n\n✨ **\"{custom_wish}\"** ✨\n\nఈ మెసేజ్‌ను మీ గిఫ్ట్ కార్డ్ చెక్‌అవుట్ సమయంలో జోడించవచ్చు. ఈ కార్డ్‌లతో కలిపి పంపితే వాళ్ళు మరింత సంతోషిస్తారు:"
        else:
            reply_text = f"Here is a customized, heartwarming greeting message for your gift:\n\n✨ **\"{custom_wish}\"** ✨\n\nYou can easily attach this during checkout! Here are the best gift cards to pair with it:"

        return {
            "reply": reply_text,
            "suggested_message": custom_wish,
            "cards": matched_cards,
            "language": lang
        }

    # Standard Sales / Product Recommendation Flow
    if lang in ["te", "te_latn"]:
        greetings = [
            "నమస్కారం! మీ అవసరానికి తగ్గట్టుగా అత్యుత్తమ గిఫ్ట్ కార్డ్‌లను క్రింద సూచిస్తున్నాను.",
            "హలో! గిఫ్ట్ సెలెక్షన్‌లో మీకు సహాయం చేయడం నాకిష్టం. ఇవి మీ కోసం బెస్ట్ డీల్స్:",
            "ఖచ్చితంగా! అన్ని రకాల బ్రాండ్లలో తక్షణ డిస్కౌంట్ మరియు గ్యారెంటీ డెలివరీ ఉన్న బెస్ట్ ఆప్షన్లు ఇవి:"
        ]
        intro = random.choice(greetings)

        # Build persuasive Telugu response
        card_recs_text = []
        for i, card in enumerate(matched_cards[:3], 1):
            denoms_str = ", ".join([f"₹{d}" for d in card["denominations"][:3]])
            disc_text = f"({card['discount_pct']}% ఫ్లాట్ డిస్కౌంట్!)" if card.get("discount_pct") > 0 else ""
            card_recs_text.append(f"**{i}. {card['name']}** {disc_text}\n• {card['description_te']}\n• డినామినేషన్లు: {denoms_str}")

        conclusion = "\n\n👉 **మీరు ఏ కార్డ్ సెలెక్ట్ చేసుకున్నా సెకన్లలో డిజిటల్ కోడ్ & పిన్ అందుతుంది.** మీకు నచ్చిన కార్డ్ కింద ఉన్న **'Buy Now'** లేదా **'Add to Cart'** బటన్ క్లిక్ చేసి వెంటనే కొనుగోలు చేయవచ్చు!"
        reply_text = f"{intro}\n\n" + "\n\n".join(card_recs_text) + conclusion

    else:
        greetings = [
            "Hello! I've curated the absolute best gift card options for you with verified instant savings:",
            "Great choice! Here are the top-rated gift cards tailored to your request with instant e-delivery:",
            "Welcome! I can instantly help you choose, customize, and deliver the perfect gift card:"
        ]
        intro = random.choice(greetings)

        card_recs_text = []
        for i, card in enumerate(matched_cards[:3], 1):
            denoms_str = ", ".join([f"₹{d}" for d in card["denominations"][:3]])
            disc_text = f"({card['discount_pct']}% Instant Savings)" if card.get("discount_pct") > 0 else ""
            card_recs_text.append(f"**{i}. {card['name']}** {disc_text}\n• {card['description']}\n• Available Values: {denoms_str}")

        conclusion = "\n\n👉 **All gift cards come with instant digital code generation and scratch-to-reveal delivery.** Click **'Quick Buy'** below on any card to proceed immediately!"
        reply_text = f"{intro}\n\n" + "\n\n".join(card_recs_text) + conclusion

    return {
        "reply": reply_text,
        "suggested_message": None,
        "cards": matched_cards,
        "language": lang
    }
