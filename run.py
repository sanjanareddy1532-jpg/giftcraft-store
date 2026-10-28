"""
GiftCraft AI - Universal Gift Card Marketplace Launcher
Starts FastAPI web server and opens the interactive web platform in browser.
"""

import sys
import os
import socket
import webbrowser
import threading
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def find_available_port(start_port=8000, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

def open_browser_after_delay(url, delay=1.5):
    def _open():
        time.sleep(delay)
        print(f"\n🚀 Opening GiftCraft AI Platform in your default browser: {url}")
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()

def main():
    import uvicorn
    from backend.server import app

    port = find_available_port(8000)
    url = f"http://127.0.0.1:{port}"

    print("=" * 70)
    print(" 🎁 GiftCraft AI - All-in-One Gift Card Selling Platform with AI")
    print("    అన్ని రకాల గిఫ్ట్ కార్డ్‌లు & AI సేల్స్ అసిస్టెంట్ ప్లాట్‌ఫారమ్")
    print("=" * 70)
    print(f" -> Local URL        : {url}")
    print(f" -> AI Sales Agent   : GiftGenie AI (Active in Telugu & English)")
    print(f" -> Available Brands : Amazon, Steam, Flipkart, Netflix, Google Play,")
    print(f"                       Zomato, Swiggy, Apple, Domino's, PlayStation & more")
    print("=" * 70)

    open_browser_after_delay(url)

    try:
        uvicorn.run("backend.server:app", host="127.0.0.1", port=port, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n[+] GiftCraft AI Server shut down cleanly. Good bye!")

if __name__ == "__main__":
    main()
