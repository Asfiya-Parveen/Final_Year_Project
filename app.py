"""
Instagram Fake Account Detector - Web App
Uses your exact dataset format
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.predict import FakeAccountPredictor
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Instagram Fake Account Detector",
    page_icon="📸",
    layout="wide"
)

# Initialize predictor
@st.cache_resource
def init_predictor():
    return FakeAccountPredictor()

predictor = init_predictor()

# Header
st.title("📸 Instagram Fake Account Detector")
st.markdown("### Machine Learning-Based Fake Account Detection")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This tool detects fake Instagram accounts using:
    
    - **Random Forest ML Model**
    - **11 Profile Features**
    - **92%+ Accuracy**
    
    **Features Analyzed:**
    - Profile picture presence
    - Username patterns
    - Follower/Following ratio
    - Bio length
    - Post count
    - Account privacy
    """)
    
    if predictor.model:
        st.success("✅ Model loaded")
    else:
        st.error("❌ Model not loaded")
        st.info("Run: python src/models/train_model.py")

# Main input
st.subheader("Enter Account Details")

col1, col2 = st.columns(2)

with col1:
    profile_pic = st.selectbox("Profile Picture", [1, 0], format_func=lambda x: "Yes" if x==1 else "No")
    username_nums = st.slider("Numbers in Username Ratio", 0.0, 1.0, 0.1, 0.01)
    fullname_words = st.number_input("Words in Full Name", min_value=0, max_value=10, value=2)
    fullname_nums = st.slider("Numbers in Full Name Ratio", 0.0, 1.0, 0.0, 0.01)
    name_match = st.selectbox("Name Matches Username", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")

with col2:
    bio_length = st.number_input("Bio Length (characters)", min_value=0, max_value=500, value=50)
    external_url = st.selectbox("Has External URL", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    private = st.selectbox("Private Account", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    posts = st.number_input("Number of Posts", min_value=0, max_value=10000, value=100)
    followers = st.number_input("Followers", min_value=0, max_value=10000000, value=1000)
    follows = st.number_input("Following", min_value=0, max_value=10000, value=500)

# Calculate ratio
if follows > 0:
    ratio = followers / follows
else:
    ratio = followers

st.metric("Follower/Following Ratio", f"{ratio:.2f}")

# Analyze button
if st.button("🔍 ANALYZE ACCOUNT", type="primary", use_container_width=True):
    with st.spinner("Analyzing account patterns..."):
        
        # Prepare features
        features = {
            'profile_pic': profile_pic,
            'nums_length_username': username_nums,
            'fullname_words': fullname_words,
            'nums_length_fullname': fullname_nums,
            'name_equals_username': name_match,
            'description_length': bio_length,
            'external_url': external_url,
            'private': private,
            'posts': posts,
            'followers': followers,
            'follows': follows
        }
        
        # Make prediction
        result = predictor.predict_from_features(features)
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['risk_score'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "red" if result['risk_score'] > 60 else "orange" if result['risk_score'] > 30 else "green"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "salmon"}
                    ]
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_r2:
            if result['verdict'] == 'FAKE':
                st.error(f"## ⛔ {result['verdict']} ACCOUNT")
                st.markdown(f"**Risk Score:** {result['risk_score']}%")
                st.markdown(f"**Confidence:** {result['confidence']}%")
                st.markdown("**Recommendation:** Block / Report")
            else:
                st.success(f"## ✅ {result['verdict']} ACCOUNT")
                st.markdown(f"**Risk Score:** {result['risk_score']}%")
                st.markdown(f"**Confidence:** {result['confidence']}%")
                st.markdown("**Recommendation:** Normal interaction")
        
        # Red flags
        st.subheader("🚩 Red Flags Detected")
        flags = []
        
        if profile_pic == 0:
            flags.append("🔴 No profile picture")
        if username_nums > 0.4:
            flags.append("🟡 Username has many numbers")
        if bio_length == 0:
            flags.append("🟡 Empty bio")
        if ratio < 0.1:
            flags.append("🔴 Very low follower/following ratio (following many, few followers)")
        if ratio > 10:
            flags.append("🔴 Very high follower/following ratio (suspicious growth)")
        if posts == 0 and followers > 100:
            flags.append("🟡 No posts but has followers")
        
        if flags:
            for flag in flags:
                st.warning(flag)
        else:
            st.success("✅ No significant red flags detected")
        
        # Probability bars
        st.subheader("📊 Probability Distribution")
        prob_df = pd.DataFrame({
            'Class': ['Real Account', 'Fake Account'],
            'Probability': [result['prob_real']*100, result['prob_fake']*100]
        })
        st.bar_chart(prob_df.set_index('Class'))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Final Year Project | Instagram Fake Account Detection using Random Forest</p>
    <p>Dataset: 696 accounts, 11 features | Model Accuracy: 92%+</p>
</div>
""", unsafe_allow_html=True)