"""
CREATE INSTAGRAM SESSION FILE
Run this ONCE to save login cookies
This helps avoid 429 errors
"""

import instaloader

# You need a REAL Instagram account for this
# Create a dummy account if you don't have one
USERNAME = "demo.01_verify"  # ← REPLACE THIS
PASSWORD = "BYX2h@nSG8yj$tP"  # ← REPLACE THIS

print("🔐 Creating Instagram session...")

L = instaloader.Instaloader()

try:
    # Login to Instagram
    L.login(USERNAME, PASSWORD)
    print("✅ Login successful!")
    
    # Save session to file
    L.save_session_to_file("instagram_session")
    print("💾 Session saved to 'instagram_session'")
    print("   This session file will help avoid rate limits")
    
except Exception as e:
    print(f"❌ Login failed: {e}")
    print("   Make sure your username and password are correct")
    print("   If you don't have an account, create one at instagram.com")