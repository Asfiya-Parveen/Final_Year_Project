"""
Create Instagram session using browser cookies directly
This is the most reliable method according to Instaloader developers[citation:2]
"""

import instaloader
import browser_cookie3
import os

print("🔐 Loading Instagram cookies from your browser...")

# Load cookies from Chrome (change to 'firefox' if you use Firefox)
# This gets your logged-in Instagram cookies directly from your browser
cj = browser_cookie3.chrome(domain_name='.instagram.com')

L = instaloader.Instaloader()

# Import the cookies into Instaloader
L.context._session.cookies.update(cj)

# Now test if it works
try:
    profile = instaloader.Profile.from_username(L.context, "instagram")
    print(f"✅ Success! Logged in as browser user")
    print(f"   Test profile: @{profile.username} has {profile.followers:,} followers")
    
    # Save the session for future use
    L.save_session_to_file("instagram_session")
    print("💾 Session saved to 'instagram_session'")
    
except Exception as e:
    print(f"❌ Failed to load cookies: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you're logged into Instagram in your browser")
    print("2. Try closing and reopening your browser")
    print("3. For Firefox, change 'chrome' to 'firefox' in the code")