# Bag Battle Streamlit App

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bag Battle",
    page_icon="🌱",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #eefbea 0%, #f7fff5 45%, #e2f6dc 100%);
}

/* Hide Streamlit default footer/header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #1b5e20, #43a047);
    padding: 45px 35px;
    border-radius: 28px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 30px rgba(27, 94, 32, 0.25);
    margin-bottom: 28px;
}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 21px;
    opacity: 0.95;
}

/* Cards */
.card {
    background-color: white;
    padding: 26px;
    border-radius: 24px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    border: 1px solid #d8ecd2;
    margin-bottom: 22px;
}

.section-title {
    color: #1b5e20;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 12px;
}

.small-text {
    color: #52734d;
    font-size: 15px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 20px;
    font-size: 17px;
    font-weight: 700;
    width: 100%;
    box-shadow: 0 6px 14px rgba(46, 125, 50, 0.25);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1b5e20, #43a047);
    color: white;
    transform: translateY(-1px);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 12px;
}

/* Leaderboard cards */
.leader-card {
    background: linear-gradient(135deg, #ffffff, #ecf8e8);
    padding: 18px 22px;
    border-radius: 20px;
    border-left: 8px solid #43a047;
    box-shadow: 0 6px 16px rgba(0,0,0,0.07);
    margin-bottom: 14px;
}

.leader-rank {
    font-size: 30px;
    font-weight: 900;
    color: #1b5e20;
}

.leader-name {
    font-size: 23px;
    font-weight: 800;
    color: #263b26;
}

.leader-info {
    font-size: 16px;
    color: #4b6043;
}

.points-pill {
    display: inline-block;
    margin-top: 8px;
    background-color: #dff5dc;
    color: #1b5e20;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 800;
}

.badge-pill {
    display: inline-block;
    margin-top: 8px;
    margin-left: 6px;
    background-color: #fff8d6;
    color: #7a5c00;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #2e7d32;
    font-weight: 700;
    padding: 20px;
}
            
/* Fix metric visibility */
[data-testid="stMetricLabel"] {
    color: #1b5e20 !important;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #2f2f2f !important;
    font-weight: 800;
}
            

</style>
""", unsafe_allow_html=True)

# =========================
# DATA SETUP
# =========================
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTj5CAnFDBeDVR_AQcllFrzzcKNwfrcVIg53-uKKGGg0edEByX_Sg44tu99INkLjI0Bfuu2xVvghHvu/pub?output=csv"

df = pd.read_csv(SHEET_URL)

# clean column names
df.columns = df.columns.str.strip()

# rename Google Form columns
df = df.rename(columns={
    "Timestamp": "date",
    "Name": "name",
    "Bags Collected": "bags",
    "Location": "location"
})

# make bags numeric
df["bags"] = pd.to_numeric(df["bags"], errors="coerce").fillna(0).astype(int)

# =========================
# HELPER FUNCTIONS
# =========================
def get_badge(bags):
    if bags >= 50:
        return "🌍 Planet Protector"
    elif bags >= 25:
        return "🌳 Eco Hero"
    elif bags >= 10:
        return "🌿 Green Warrior"
    elif bags >= 5:
        return "🍃 Cleanup Starter"
    else:
        return "🌱 New Challenger"


def get_rank_icon(position):
    if position == 1:
        return "🥇"
    elif position == 2:
        return "🥈"
    elif position == 3:
        return "🥉"
    else:
        return f"#{position}"

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">🌱 Bag Battle</div>
    <div class="hero-subtitle">Pick up trash, collect points, climb the leaderboard.</div>
</div>
""", unsafe_allow_html=True)

# =========================
# STATS
# =========================
total_bags = int(df["bags"].sum()) if not df.empty else 0
total_points = total_bags * 10
total_players = df["name"].nunique() if not df.empty else 0
total_cleanups = len(df)

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.metric("🗑️ Total Bags", total_bags)

with stat2:
    st.metric("⭐ Total Points", total_points)

with stat3:
    st.metric("👥 Players", total_players)

with stat4:
    st.metric("⚔️ Battles Logged", total_cleanups)

# =========================
# MAIN LAYOUT
# =========================
left_col, right_col = st.columns([1, 1.3])

# =========================
# SUBMIT FORM
# =========================
with left_col:
    st.markdown('<div class="section-title">⚔️ Enter the Battle</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-text">Log your cleanup and earn 10 points for every bag collected.</div>', unsafe_allow_html=True)

    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScKwpVKZx-EaoLGQ6ODSGbH7Qs18dP3NH67BBwk2lmsTgn7Bw/viewform?usp=publish-editor"
    st.link_button("🌱 Submit Cleanup", FORM_URL)


with left_col:
    st.markdown('<div class="section-title">🎮 How Points Work</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#52734d;margin-left: 25px;">🗑️ 1 bag = 10 points</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#52734d;margin-left: 25px;">🏆 Top 3 players get medals</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#52734d;margin-left: 25px;">🌿 More bags unlock better badges</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#52734d;margin-left: 25px;">🌍 Every cleanup adds to the community total</p>', unsafe_allow_html=True)
 

# =========================
# LEADERBOARD
# =========================
with right_col:
    st.markdown('<div class="section-title">🏆 Leaderboard</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No cleanups yet. Be the first to enter Bag Battle!")
    else:
        leaderboard = (
            df.groupby("name", as_index=False)["bags"]
            .sum()
            .sort_values("bags", ascending=False)
            .reset_index(drop=True)
        )

        leaderboard["points"] = leaderboard["bags"] * 10

        for i, row in leaderboard.iterrows():
            position = i + 1
            rank_icon = get_rank_icon(position)
            badge = get_badge(int(row["bags"]))

            st.markdown(f"""
            <div class="leader-card">
                <div class="leader-rank">{rank_icon}</div>
                <div class="leader-name">{row['name']}</div>
                <div class="leader-info">🗑️ {int(row['bags'])} bags collected</div>
                <span class="points-pill">⭐ {int(row['points'])} points</span>
                <span class="badge-pill">{badge}</span>
            </div>
            """, unsafe_allow_html=True)


# =========================
# RECENT ACTIVITY
# =========================
with left_col:
    st.markdown('<div class="section-title">📍 Recent Cleanup Activity</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown(
            '<p style="color:#52734d; margin-left:25px;">No activity yet.</p>',
            unsafe_allow_html=True
        )
    else:
        recent = df.sort_values("date", ascending=False).head(5)

        for _, row in recent.iterrows():
            st.markdown(
            f'<p style="color:#52734d;margin-left: 25px;">🌱 <b>{row["name"]}</b> collected <b>{int(row["bags"])}</b> bag(s) at <b>{row["location"]}</b></p>',
            unsafe_allow_html=True
        )



# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    🌿 Small actions. Big impact. Keep battling for a cleaner planet. 🌿
</div>
""", unsafe_allow_html=True)