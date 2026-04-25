"""
Create Instagram session using browser cookies
This is the most reliable method according to Instaloader developers
"""

import instaloader
import os

print("🔐 Creating Instagram session from cookies...")

L = instaloader.Instaloader()

# Path to your cookies file
cookies_file = "cookies.txt"

if os.path.exists(cookies_file):
    try:
        # Load session from browser cookies
        # IMPORTANT: Replace "your_username" with your actual Instagram username
        YOUR_USERNAME = "demo.01_verify"  # ← CHANGE THIS to your Instagram username
        
        L.load_session_from_file(YOUR_USERNAME, cookies_file)
        print("✅ Session loaded from cookies!")
        
        # Verify it works by fetching a profile
        profile = instaloader.Profile.from_username(L.context, "instagram")
        print(f"✅ Verification successful!")
        print(f"   Profile: @{profile.username}")
        print(f"   Followers: {profile.followers:,}")
        
        # Save session for future use
        L.save_session_to_file("instagram_session")
        print("💾 Session saved to 'instagram_session'")
        print("\n✅ You can now use your scraper normally!")
        
    except Exception as e:
        print(f"❌ Error loading cookies: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you exported cookies while logged into Instagram")
        print("2. Don't log out of Instagram in your browser")
        print("3. Try re-exporting the cookies file")
        print("4. Make sure you changed 'your_username' to your actual username")
else:
    print("❌ cookies.txt not found!")
    print("   Please export cookies from browser first:")
    print("   1. Log into Instagram in Chrome/Firefox")
    print("   2. Install 'Get cookies.txt LOCALLY' extension")
    print("   3. Export cookies and save as 'cookies.txt' in this folder")