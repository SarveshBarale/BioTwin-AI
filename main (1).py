import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime, date, timedelta
import json
import hashlib
import os

st.set_page_config(
    page_title="BioTwin AI - Your Digital Health Twin",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(99,102,241,0.3);
        box-shadow: 0 8px 32px rgba(99,102,241,0.15);
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
    }

    .main-header p {
        color: #a5b4fc;
        font-size: 1rem;
        margin-top: 0.3rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .section-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: inline-block;
    }

    .risk-low {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #6ee7b7;
        font-weight: 600;
        font-size: 1.3rem;
    }

    .risk-moderate {
        background: linear-gradient(135deg, #78350f, #92400e);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #fcd34d;
        font-weight: 600;
        font-size: 1.3rem;
    }

    .risk-high {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #fca5a5;
        font-weight: 600;
        font-size: 1.3rem;
    }

    .insight-card {
        background: rgba(30, 27, 75, 0.6);
        border-left: 4px solid #6366f1;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #e0e7ff;
    }

    .organ-card {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.3rem 0;
    }

    .gamification-badge {
        background: linear-gradient(135deg, #1e3a5f, #1a1a2e);
        border: 2px solid #3b82f6;
        border-radius: 50px;
        padding: 0.4rem 1rem;
        color: #93c5fd;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }

    .health-age-card {
        background: linear-gradient(135deg, #2d1b69, #1a0533);
        border: 2px solid #8b5cf6;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }

    .women-module {
        background: linear-gradient(135deg, #4a0030, #2d0020);
        border: 1px solid #ec4899;
        border-radius: 12px;
        padding: 1.2rem;
    }

    .xai-bar {
        background: rgba(99,102,241,0.15);
        border-radius: 6px;
        padding: 0.5rem 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #6366f1;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30,27,75,0.5);
        padding: 0.5rem;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #a5b4fc;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
    }

    .footer-note {
        text-align: center;
        color: #6b7280;
        font-size: 0.8rem;
        padding: 1rem;
        border-top: 1px solid rgba(99,102,241,0.2);
        margin-top: 2rem;
    }

    .login-card {
        background: linear-gradient(135deg, #0f0c29, #1e1b4b);
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 480px;
        margin: 2rem auto;
        box-shadow: 0 20px 60px rgba(99,102,241,0.2);
    }

    .daily-log-card {
        background: linear-gradient(135deg, #0d1117, #1a1a2e);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }

    .streak-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        border-radius: 50px;
        padding: 0.3rem 0.8rem;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }

    .goal-met {
        background: rgba(16,185,129,0.15);
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        color: #6ee7b7;
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }

    .goal-missed {
        background: rgba(239,68,68,0.1);
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        color: #fca5a5;
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ====================== DATA STORAGE ======================
DATA_FILE = "biotwin_users.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_user(username):
    data = load_data()
    return data.get(username)

def create_user(username, password, profile):
    data = load_data()
    data[username] = {
        "password": hash_password(password),
        "profile": profile,
        "daily_logs": {},
        "created_at": str(date.today())
    }
    save_data(data)

def save_daily_log(username, log_date, log_entry):
    data = load_data()
    if username not in data:
        return
    if "daily_logs" not in data[username]:
        data[username]["daily_logs"] = {}
    data[username]["daily_logs"][str(log_date)] = log_entry
    save_data(data)

def get_daily_logs(username):
    user = get_user(username)
    if user:
        return user.get("daily_logs", {})
    return {}


# ====================== AI ENGINE ======================
@st.cache_resource
def train_model():
    np.random.seed(42)
    n = 1000
    data = pd.DataFrame({
        'age': np.random.randint(18, 80, n),
        'bmi': np.random.normal(25, 5, n).clip(15, 40),
        'sleep_hours': np.random.normal(7, 1.5, n).clip(3, 12),
        'daily_steps': np.random.normal(7000, 3000, n).clip(1000, 20000),
        'diet_score': np.random.randint(1, 11, n),
        'stress_level': np.random.randint(1, 11, n),
        'smoking': np.random.choice([0, 1], n, p=[0.7, 0.3]),
    })
    data['risk_score'] = (
        (data['bmi'] > 30) * 0.4 +
        (data['sleep_hours'] < 6) * 0.3 +
        (data['daily_steps'] < 5000) * 0.25 +
        (data['stress_level'] > 7) * 0.2 +
        data['smoking'] * 0.25 +
        np.random.normal(0, 0.1, n)
    ).clip(0, 1)
    data['risk_label'] = (data['risk_score'] > 0.5).astype(int)

    X = data.drop(['risk_score', 'risk_label'], axis=1)
    y = data['risk_label']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model, X.columns


model, feature_cols = train_model()


# ====================== HELPER FUNCTIONS ======================
def compute_pcos_risk(sleep, stress, steps, diet, bmi, cycle_irregular, gender):
    if gender != "Female":
        return None, []
    score = 0
    reasons = []
    if sleep < 6:
        score += 2
        reasons.append("Poor sleep disrupts hormonal balance")
    if stress > 6:
        score += 2
        reasons.append("High stress elevates cortisol, affecting hormones")
    if steps < 5000:
        score += 1.5
        reasons.append("Low activity linked to insulin resistance")
    if diet < 5:
        score += 1.5
        reasons.append("Poor diet quality increases PCOS risk")
    if bmi > 27:
        score += 2
        reasons.append("Elevated BMI is a common PCOS risk factor")
    if cycle_irregular:
        score += 3
        reasons.append("Irregular cycles are a key PCOS indicator")
    pct = min(score / 12 * 100, 100)
    return round(pct, 1), reasons


def compute_health_age(age, bmi, sleep, steps, diet, stress, smoking):
    delta = 0
    if bmi > 30:
        delta += 3
    elif bmi > 25:
        delta += 1
    if sleep < 6:
        delta += 2
    elif sleep >= 8:
        delta -= 1
    if steps >= 10000:
        delta -= 2
    elif steps < 5000:
        delta += 2
    if diet >= 8:
        delta -= 1.5
    elif diet < 4:
        delta += 2
    if stress > 7:
        delta += 2
    if smoking:
        delta += 4
    health_age = round(age + delta)
    return health_age, round(delta, 1)


def get_feature_importances(input_df):
    importances = model.feature_importances_
    explanations = {}
    for feat, imp in zip(feature_cols, importances):
        val = input_df[feat].values[0]
        direction = "↑ Risk" if (
            (feat == 'bmi' and val > 25) or
            (feat == 'sleep_hours' and val < 7) or
            (feat == 'daily_steps' and val < 7000) or
            (feat == 'stress_level' and val > 5) or
            (feat == 'smoking' and val == 1) or
            (feat == 'diet_score' and val < 6)
        ) else "✓ OK"
        explanations[feat] = (round(imp * 100, 1), direction)
    return dict(sorted(explanations.items(), key=lambda x: -x[1][0]))


def get_gamification_badges(sleep, steps, diet, stress, smoking, bmi):
    badges = []
    if not smoking:
        badges.append("🚭 Non-Smoker")
    if steps >= 10000:
        badges.append("🏃 Step Champion")
    elif steps >= 7500:
        badges.append("👟 Active Walker")
    if sleep >= 8:
        badges.append("😴 Sleep Master")
    elif sleep >= 7:
        badges.append("🌙 Good Sleeper")
    if diet >= 8:
        badges.append("🥗 Nutrition Pro")
    if stress <= 4:
        badges.append("🧘 Zen Mode")
    if bmi >= 18.5 and bmi < 25:
        badges.append("⚖️ Healthy Weight")
    if len(badges) >= 5:
        badges.append("🏆 Health Champion")
    return badges


def get_cycle_recommendations(cycle_day):
    if cycle_day is None:
        return []
    if 1 <= cycle_day <= 5:
        phase = "Menstrual"
        tips = ["🍫 Opt for iron-rich foods (spinach, lentils)", "🧘 Light yoga or walking recommended", "💤 Prioritize extra rest today", "🫖 Ginger or chamomile tea for cramps"]
    elif 6 <= cycle_day <= 13:
        phase = "Follicular"
        tips = ["⚡ Great time for high-intensity workouts", "🥦 Focus on lean proteins and complex carbs", "🧠 Cognitive performance is peaking — tackle hard tasks", "💧 Stay well hydrated"]
    elif 14 <= cycle_day <= 16:
        phase = "Ovulation"
        tips = ["🏋️ Peak physical strength — ideal for strength training", "🍓 Antioxidant-rich foods support hormonal health", "😊 Social energy is highest this phase"]
    else:
        phase = "Luteal"
        tips = ["🍵 Reduce caffeine to ease PMS symptoms", "🚶 Moderate activity like walking or cycling", "🫁 Deep breathing helps with mood swings", "🥜 Magnesium-rich snacks reduce bloating"]
    return phase, tips


def compute_diet_score_from_calories(calories_consumed, target_cal, protein_consumed, target_protein):
    """Convert calorie/protein adherence into a diet quality score (1–10)."""
    cal_ratio = min(calories_consumed / max(target_cal, 1), 1.5)
    pro_ratio = min(protein_consumed / max(target_protein, 1), 1.5)
    # Good adherence = ratio near 1.0
    cal_score = max(0, 10 - abs(cal_ratio - 1.0) * 10)
    pro_score = max(0, 10 - abs(pro_ratio - 1.0) * 10)
    return round((cal_score * 0.5 + pro_score * 0.5), 1)


def compute_stress_score_from_workload(workload_hours, sleep_hrs, mood):
    """Estimate stress from workload hours, sleep, and mood."""
    base = 1
    if workload_hours >= 10:
        base += 4
    elif workload_hours >= 8:
        base += 3
    elif workload_hours >= 6:
        base += 2
    else:
        base += 1
    if sleep_hrs < 6:
        base += 2
    elif sleep_hrs < 7:
        base += 1
    mood_penalty = {"Great 😄": -1, "Good 🙂": 0, "Okay 😐": 1, "Stressed 😟": 2, "Exhausted 😩": 3}
    base += mood_penalty.get(mood, 0)
    return min(10, max(1, round(base)))


def get_daily_targets(profile):
    """Return personalized daily calorie and protein targets."""
    weight = profile.get("weight", 65)
    height = profile.get("height", 165)
    age = profile.get("age", 25)
    gender = profile.get("gender", "Female")
    activity = profile.get("activity_level", "Moderate")

    # Mifflin-St Jeor BMR
    if gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

    activity_factors = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Very Active": 1.9}
    tdee = bmr * activity_factors.get(activity, 1.55)

    # Protein: 1.2–1.6g per kg body weight
    protein = round(weight * 1.4, 0)

    return round(tdee, 0), protein


def compute_streak(logs):
    """Count consecutive days with a log entry up to today."""
    streak = 0
    check_date = date.today()
    while str(check_date) in logs:
        streak += 1
        check_date -= timedelta(days=1)
    return streak


# ====================== LOGIN / SIGNUP SCREEN ======================
def show_login_screen():
    st.markdown("""
    <div class="main-header">
        <h1>🧬 BioTwin AI</h1>
        <p>Your Real-Time Digital Health Twin • Simulating Your Future Body • AI-Powered Preventive Health</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #0f0c29, #1e1b4b); border:1px solid rgba(99,102,241,0.4);
                    border-radius:20px; padding:2.5rem; box-shadow:0 20px 60px rgba(99,102,241,0.2);">
        """, unsafe_allow_html=True)

        st.markdown("#### 👤 Welcome Back")
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])

        with tab_login:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pw")
            if st.button("🚀 Login", use_container_width=True):
                user = get_user(username)
                if user and user["password"] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["profile"] = user["profile"]
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        with tab_signup:
            st.markdown("**Create your account**")
            new_user = st.text_input("Choose Username", key="su_user")
            new_pw = st.text_input("Choose Password", type="password", key="su_pw")
            new_pw2 = st.text_input("Confirm Password", type="password", key="su_pw2")

            st.markdown("**Your Profile**")
            c1, c2 = st.columns(2)
            with c1:
                su_name = st.text_input("Full Name", key="su_name")
                su_age = st.number_input("Age", 14, 80, 25, key="su_age")
                su_weight = st.number_input("Weight (kg)", 30, 200, 60, key="su_weight")
            with c2:
                su_gender = st.selectbox("Gender", ["Female", "Male", "Non-binary"], key="su_gender")
                su_height = st.number_input("Height (cm)", 140, 220, 162, key="su_height")
                su_activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"], index=2, key="su_act")

            su_smoking = st.checkbox("I smoke", key="su_smoke")
            su_cycle_irreg = st.checkbox("Irregular menstrual cycle (if applicable)", key="su_cycle")

            if st.button("✅ Create Account", use_container_width=True):
                if not new_user or not new_pw:
                    st.error("Please fill in all fields.")
                elif new_pw != new_pw2:
                    st.error("Passwords do not match.")
                elif get_user(new_user):
                    st.error("Username already exists.")
                else:
                    profile = {
                        "name": su_name,
                        "age": su_age,
                        "gender": su_gender,
                        "weight": su_weight,
                        "height": su_height,
                        "activity_level": su_activity,
                        "smoking": su_smoking,
                        "cycle_irregular": su_cycle_irreg
                    }
                    create_user(new_user, new_pw, profile)
                    st.success("🎉 Account created! Please login.")

        st.markdown("</div>", unsafe_allow_html=True)


# ====================== MAIN APP ======================
def show_main_app():
    username = st.session_state["username"]
    profile = st.session_state["profile"]
    logs = get_daily_logs(username)

    # Compute profile vars
    age = profile.get("age", 25)
    gender = profile.get("gender", "Female")
    weight = profile.get("weight", 65)
    height = profile.get("height", 165)
    smoking = profile.get("smoking", False)
    cycle_irregular = profile.get("cycle_irregular", False)
    bmi = round(weight / ((height / 100) ** 2), 1)

    target_calories, target_protein = get_daily_targets(profile)

    # Minimum steps criteria (WHO / PCOD research based)
    MIN_STEPS = 7500
    MIN_CALORIES_PCT = 0.85  # at least 85% of target
    MAX_CALORIES_PCT = 1.15  # not more than 115%
    MIN_PROTEIN_PCT = 0.90

    # ====================== SIDEBAR ======================
    st.sidebar.markdown(f"## 👋 Hello, {profile.get('name', username)}!")
    streak = compute_streak(logs)
    if streak > 0:
        st.sidebar.markdown(f'<div class="streak-badge">🔥 {streak}-day streak!</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # Get today's log if exists
    today_str = str(date.today())
    today_log = logs.get(today_str, {})

    # Use today's log values or fall back to profile-based defaults
    sleep = today_log.get("sleep", 6.5)
    steps = today_log.get("steps", 6500)
    stress = today_log.get("stress", 5)
    diet = today_log.get("diet_score", 6)

    st.sidebar.markdown("### 🏃 Live Health Snapshot")
    st.sidebar.caption("Based on today's logged data (or defaults if not logged)")
    st.sidebar.metric("Today's Steps", f"{int(steps):,}", f"{'✅' if steps >= MIN_STEPS else '⚠️'} Target: {MIN_STEPS:,}")
    st.sidebar.metric("Diet Score", f"{diet}/10")
    st.sidebar.metric("Stress Level", f"{stress}/10")
    st.sidebar.metric("Sleep", f"{sleep} hrs")
    st.sidebar.metric("BMI", f"{bmi}")

    if st.sidebar.button("🚪 Logout"):
        for key in ["logged_in", "username", "profile"]:
            del st.session_state[key]
        st.rerun()

    # Women-specific
    cycle_day = None
    if gender == "Female":
        st.sidebar.markdown("### 🌸 Women's Health")
        cycle_day_input = st.sidebar.number_input("Current cycle day (1–28)", min_value=1, max_value=28, value=14, step=1)
        cycle_day = int(cycle_day_input)

    # ====================== COMPUTE CORE METRICS ======================
    input_data = pd.DataFrame([[age, bmi, sleep, steps, diet, stress, int(smoking)]], columns=feature_cols)
    current_risk_prob = model.predict_proba(input_data)[0][1] * 100

    if current_risk_prob < 30:
        risk_label = "🟢 Low Risk"
        risk_class = "risk-low"
    elif current_risk_prob < 60:
        risk_label = "🟡 Moderate Risk"
        risk_class = "risk-moderate"
    else:
        risk_label = "🔴 High Risk"
        risk_class = "risk-high"

    health_age, age_delta = compute_health_age(age, bmi, sleep, steps, diet, stress, smoking)
    badges = get_gamification_badges(sleep, steps, diet, stress, smoking, bmi)
    feature_explanations = get_feature_importances(input_data)

    # ====================== HEADER ======================
    st.markdown("""
    <div class="main-header">
        <h1>🧬 BioTwin AI</h1>
        <p>Your Real-Time Digital Health Twin • Simulating Your Future Body • AI-Powered Preventive Health</p>
    </div>
    """, unsafe_allow_html=True)

    # ====================== TABS ======================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard",
        "📝 Daily Log",
        "⏳ Future Simulation",
        "🧠 Explainable AI",
        "🌸 Women's Health",
        "🏆 Health Score",
        "📅 Monthly Report"
    ])

    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        st.markdown("### 📊 Current Health Snapshot")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            bmi_status = "✅ Healthy" if bmi < 25 else ("⚠️ Overweight" if bmi < 30 else "🔴 Obese")
            st.metric("BMI", f"{bmi}", bmi_status)
        with c2:
            st.metric("Sleep", f"{sleep} hrs", "✅ Optimal" if sleep >= 7 else "⚠️ Low")
        with c3:
            st.metric("Daily Steps", f"{int(steps):,}", "✅ Active" if steps >= MIN_STEPS else "⚠️ Sedentary")
        with c4:
            st.metric("Diet Score", f"{diet}/10", "✅ Good" if diet >= 7 else "⚠️ Improve")
        with c5:
            st.metric("Stress Level", f"{stress}/10", "✅ Low" if stress <= 4 else "⚠️ High")

        st.markdown("---")
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown(f'<div class="{risk_class}">🔬 Simulated 5-Year Metabolic Risk: {risk_label} — {current_risk_prob:.1f}%</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=current_risk_prob,
                title={'text': "Metabolic Risk Score", 'font': {'size': 18, 'color': '#a5b4fc'}},
                number={'font': {'color': '#e0e7ff', 'size': 48}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#6b7280'},
                    'bar': {'color': "#6366f1", 'thickness': 0.3},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'bordercolor': 'rgba(99,102,241,0.3)',
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(16,185,129,0.3)"},
                        {'range': [30, 60], 'color': "rgba(245,158,11,0.3)"},
                        {'range': [60, 100], 'color': "rgba(239,68,68,0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "#818cf8", 'width': 3},
                        'thickness': 0.75,
                        'value': current_risk_prob
                    }
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e7ff'},
                height=300,
                margin=dict(t=60, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("#### 🫀 Organ-Level Impact")

            organ_scores = {"❤️ Heart": 0, "🫁 Lungs": 0, "🧠 Brain": 0, "⚡ Metabolism": 0, "🩺 Immune": 0}

            if smoking:
                organ_scores["❤️ Heart"] += 2
                organ_scores["🫁 Lungs"] += 3
                organ_scores["🩺 Immune"] += 1
            if sleep < 6:
                organ_scores["🧠 Brain"] += 3
                organ_scores["❤️ Heart"] += 1
                organ_scores["🩺 Immune"] += 2
            if diet < 5:
                organ_scores["⚡ Metabolism"] += 3
                organ_scores["🩺 Immune"] += 1
            if steps < 5000:
                organ_scores["⚡ Metabolism"] += 2
                organ_scores["❤️ Heart"] += 1
            if stress > 7:
                organ_scores["🧠 Brain"] += 2
                organ_scores["❤️ Heart"] += 1
                organ_scores["🩺 Immune"] += 1
            if bmi > 30:
                organ_scores["⚡ Metabolism"] += 2
                organ_scores["❤️ Heart"] += 1

            for organ, score in organ_scores.items():
                if score <= 1:
                    level, color, bar_pct = "🟢 Low", "#10b981", max(5, score * 15)
                elif score <= 3:
                    level, color, bar_pct = "🟡 Moderate", "#f59e0b", min(score * 20, 65)
                else:
                    level, color, bar_pct = "🔴 High", "#ef4444", min(score * 15, 100)

                st.markdown(f"""
                <div class="organ-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#e0e7ff; font-weight:600;">{organ}</span>
                        <span style="color:{color}; font-size:0.85rem;">{level}</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.1); border-radius:4px; height:6px; margin-top:6px;">
                        <div style="background:{color}; width:{bar_pct}%; height:100%; border-radius:4px; opacity:0.8;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            worst = max(organ_scores, key=organ_scores.get)
            st.warning(f"⚠️ Most affected: **{worst}**")

        # Insights
        st.markdown("---")
        st.markdown("#### 💡 Digital Twin Interpretation")

        insights = []
        if smoking:
            insights.append(("🚬", "Smoking", "Accelerating lung and heart damage — projected 35% higher cardiovascular risk in 3 years"))
        if sleep < 6:
            insights.append(("⏰", "Sleep Deficit", "Chronic short sleep impairs brain recovery and elevates metabolic stress hormones"))
        if steps < 5000:
            insights.append(("🏃", "Low Activity", "Sedentary lifestyle is a primary hidden driver of future metabolic disorder"))
        if stress > 7:
            insights.append(("😟", "High Stress", "Elevated cortisol is silently raising cardiovascular risk even if other numbers look okay"))
        if diet < 5:
            insights.append(("🍔", "Poor Diet", "Low diet quality is fueling inflammation and increasing metabolic syndrome risk"))
        if bmi > 30:
            insights.append(("⚖️", "BMI Concern", "Obesity significantly elevates risk for diabetes, heart disease, and sleep apnea"))

        if insights:
            cols = st.columns(min(len(insights), 3))
            for i, (icon, title, desc) in enumerate(insights):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size:1.5rem;">{icon}</div>
                        <div style="color:#818cf8; font-weight:600; margin:4px 0;">{title}</div>
                        <div style="color:#c7d2fe; font-size:0.85rem;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✅ Your current habits are well-balanced — your digital twin looks healthy! Keep it up.")


    # ========== TAB 2: DAILY LOG ==========
    with tab2:
        st.markdown("### 📝 Daily Health Log")
        st.caption("Log your daily activity, meals, and wellness. Data is stored and used for your monthly report.")

        # Target display
        st.markdown("#### 🎯 Your Personalized Daily Targets")
        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e3a5f,#1a1a2e); border:1px solid #3b82f6;
                        border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:2rem;">👟</div>
                <div style="color:#93c5fd; font-size:1.4rem; font-weight:700;">{MIN_STEPS:,}</div>
                <div style="color:#6b7280; font-size:0.85rem;">Min Steps / Day</div>
                <div style="color:#a5b4fc; font-size:0.75rem; margin-top:4px;">Reduces PCOD risk when sustained for 30+ days</div>
            </div>
            """, unsafe_allow_html=True)
        with t2:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#064e3b,#065f46); border:1px solid #10b981;
                        border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:2rem;">🍽️</div>
                <div style="color:#6ee7b7; font-size:1.4rem; font-weight:700;">{int(target_calories)} kcal</div>
                <div style="color:#6b7280; font-size:0.85rem;">Target Calories / Day</div>
                <div style="color:#a5b4fc; font-size:0.75rem; margin-top:4px;">Based on your BMR + {profile.get('activity_level','Moderate')} activity</div>
            </div>
            """, unsafe_allow_html=True)
        with t3:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#4a0030,#2d0020); border:1px solid #ec4899;
                        border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:2rem;">💪</div>
                <div style="color:#f9a8d4; font-size:1.4rem; font-weight:700;">{int(target_protein)}g</div>
                <div style="color:#6b7280; font-size:0.85rem;">Target Protein / Day</div>
                <div style="color:#a5b4fc; font-size:0.75rem; margin-top:4px;">1.4g × {weight}kg body weight</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### ✍️ Log Today's Data")

        log_date = st.date_input("Date", value=date.today(), max_value=date.today())
        existing = logs.get(str(log_date), {})

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**🏃 Activity**")
            log_steps = st.number_input("Steps walked today", 0, 50000,
                                        value=existing.get("steps", 5000), step=100)
            log_sleep = st.slider("Sleep last night (hrs)", 3.0, 12.0,
                                   value=float(existing.get("sleep", 6.5)), step=0.5)
            log_exercise_min = st.number_input("Exercise duration (minutes)", 0, 300,
                                               value=existing.get("exercise_min", 0), step=5)
            log_exercise_type = st.selectbox("Exercise type",
                                             ["None", "Walking", "Running", "Yoga", "Cycling", "Strength Training", "Swimming", "Dance/Zumba", "Other"],
                                             index=["None", "Walking", "Running", "Yoga", "Cycling", "Strength Training", "Swimming", "Dance/Zumba", "Other"].index(
                                                 existing.get("exercise_type", "None")))

        with col_b:
            st.markdown("**🍽️ Nutrition**")
            log_calories = st.number_input(
                f"Calories consumed today (target: {int(target_calories)} kcal)",
                0, 5000, value=existing.get("calories", int(target_calories * 0.9)), step=50)
            log_protein = st.number_input(
                f"Protein consumed today (target: {int(target_protein)}g)",
                0, 300, value=existing.get("protein", int(target_protein * 0.85)), step=5)
            log_water = st.slider("Water intake (glasses)", 0, 20,
                                   value=existing.get("water_glasses", 6))
            st.markdown("**Meal summary (optional)**")
            log_meal_notes = st.text_area("What did you eat today?",
                                          value=existing.get("meal_notes", ""),
                                          placeholder="e.g. Oats for breakfast, dal rice for lunch, salad for dinner",
                                          height=80)

        st.markdown("**😰 Stress & Workload**")
        col_c, col_d = st.columns(2)
        with col_c:
            log_workload = st.slider("Work/Study hours today (workload indicator)", 0, 16,
                                      value=existing.get("workload_hours", 6))
            log_mood = st.selectbox("How are you feeling?",
                                    ["Great 😄", "Good 🙂", "Okay 😐", "Stressed 😟", "Exhausted 😩"],
                                    index=["Great 😄", "Good 🙂", "Okay 😐", "Stressed 😟", "Exhausted 😩"].index(
                                        existing.get("mood", "Okay 😐")))
        with col_d:
            auto_stress = compute_stress_score_from_workload(log_workload, log_sleep, log_mood)
            st.markdown(f"""
            <div style="background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3);
                        border-radius:10px; padding:1rem; text-align:center; margin-top:1.5rem;">
                <div style="color:#a5b4fc; font-size:0.85rem;">Estimated Stress Level</div>
                <div style="font-size:2.5rem; font-weight:700; color:{'#ef4444' if auto_stress>=7 else '#f59e0b' if auto_stress>=5 else '#10b981'};">
                    {auto_stress}/10</div>
                <div style="color:#6b7280; font-size:0.75rem;">Based on workload ({log_workload}h), sleep ({log_sleep}h), mood</div>
            </div>
            """, unsafe_allow_html=True)

        # Compute derived diet score
        auto_diet = compute_diet_score_from_calories(log_calories, target_calories, log_protein, target_protein)
        st.markdown(f"""
        <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);
                    border-radius:10px; padding:0.8rem 1.2rem; margin-top:0.5rem;">
            <span style="color:#6ee7b7; font-weight:600;">🥗 Auto Diet Score: {auto_diet}/10</span>
            <span style="color:#6b7280; font-size:0.85rem; margin-left:1rem;">
                Calories: {log_calories}/{int(target_calories)} kcal | Protein: {log_protein}/{int(target_protein)}g
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Goal check display
        goals_check = []
        goals_check.append(("👟 Steps", log_steps >= MIN_STEPS, f"{log_steps:,} / {MIN_STEPS:,}"))
        goals_check.append(("🍽️ Calories", MIN_CALORIES_PCT * target_calories <= log_calories <= MAX_CALORIES_PCT * target_calories,
                             f"{log_calories} / {int(target_calories)} target"))
        goals_check.append(("💪 Protein", log_protein >= MIN_PROTEIN_PCT * target_protein, f"{log_protein}g / {int(target_protein)}g"))
        goals_check.append(("😴 Sleep", log_sleep >= 7, f"{log_sleep} hrs / 7 hrs needed"))
        goals_check.append(("💧 Water", log_water >= 8, f"{log_water} / 8 glasses"))

        st.markdown("**Daily Goal Check:**")
        gc_cols = st.columns(5)
        for i, (name, met, detail) in enumerate(goals_check):
            with gc_cols[i]:
                icon = "✅" if met else "❌"
                color = "#10b981" if met else "#ef4444"
                st.markdown(f"""
                <div style="background:rgba({'16,185,129' if met else '239,68,68'},0.1); border:1px solid {color};
                            border-radius:10px; padding:0.6rem; text-align:center;">
                    <div style="font-size:1.4rem;">{icon}</div>
                    <div style="color:{color}; font-weight:600; font-size:0.85rem;">{name}</div>
                    <div style="color:#9ca3af; font-size:0.75rem;">{detail}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Today's Log", use_container_width=True, type="primary"):
            entry = {
                "steps": log_steps,
                "sleep": log_sleep,
                "exercise_min": log_exercise_min,
                "exercise_type": log_exercise_type,
                "calories": log_calories,
                "protein": log_protein,
                "water_glasses": log_water,
                "meal_notes": log_meal_notes,
                "workload_hours": log_workload,
                "mood": log_mood,
                "stress": auto_stress,
                "diet_score": auto_diet,
                "goals_met": sum(1 for _, m, _ in goals_check if m)
            }
            save_daily_log(username, log_date, entry)
            st.success(f"✅ Log saved for {log_date}! {sum(1 for _,m,_ in goals_check if m)}/5 goals met.")
            st.rerun()

        # Recent logs table
        if logs:
            st.markdown("---")
            st.markdown("#### 📋 Recent Logs")
            recent = sorted(logs.items(), reverse=True)[:14]
            rows = []
            for d, lg in recent:
                rows.append({
                    "Date": d,
                    "Steps": f"{lg.get('steps',0):,}",
                    "Sleep (h)": lg.get("sleep", "-"),
                    "Calories": lg.get("calories", "-"),
                    "Protein (g)": lg.get("protein", "-"),
                    "Stress": f"{lg.get('stress','-')}/10",
                    "Goals Met": f"{lg.get('goals_met',0)}/5",
                    "Mood": lg.get("mood", "-")
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


    # ========== TAB 3: FUTURE SIMULATION ==========
    with tab3:
        st.markdown("### ⏳ Simulate Your Future Body (1–5 Years)")

        scenario = st.radio(
            "Choose simulation scenario:",
            ["📉 Current Lifestyle Continues", "📈 Improved Habits (+1h sleep, +2000 steps, -2 stress, better diet)", "🎯 Custom Scenario"],
            horizontal=False
        )

        custom_sleep_delta = custom_steps_delta = custom_stress_delta = custom_diet_delta = 0
        custom_quit_smoking = False

        if scenario == "🎯 Custom Scenario":
            st.markdown("#### Configure your custom lifestyle changes:")
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1:
                custom_sleep_delta = st.slider("Sleep change (hrs)", -2.0, 4.0, 1.0, 0.5)
            with cc2:
                custom_steps_delta = st.slider("Steps change", -3000, 8000, 2000, 500)
            with cc3:
                custom_stress_delta = st.slider("Stress change", -5, 3, -2)
            with cc4:
                custom_diet_delta = st.slider("Diet quality change", -3, 5, 2)
            if smoking:
                custom_quit_smoking = st.checkbox("Quit smoking?")

        years = list(range(1, 6))
        risks_current, risks_improved = [], []

        for y in years:
            proj_sleep = max(3, sleep - y * 0.2)
            proj_steps = max(1000, steps - y * 300)
            proj_stress = min(10, stress + y * 0.3)
            proj_diet = max(1, diet - y * 0.3)
            proj_df_current = pd.DataFrame([[age + y, bmi + y * 0.5, proj_sleep, proj_steps,
                                             proj_diet, proj_stress, int(smoking)]], columns=feature_cols)
            risks_current.append(model.predict_proba(proj_df_current)[0][1] * 100)

            if scenario == "📈 Improved Habits (+1h sleep, +2000 steps, -2 stress, better diet)":
                imp_sleep, imp_steps, imp_stress, imp_diet, imp_smoke = min(9, sleep + 1), min(18000, steps + 2000), max(1, stress - 2), min(10, diet + 2), 0
            elif scenario == "🎯 Custom Scenario":
                imp_sleep = min(12, sleep + custom_sleep_delta)
                imp_steps = min(20000, steps + custom_steps_delta)
                imp_stress = max(1, stress + custom_stress_delta)
                imp_diet = min(10, diet + custom_diet_delta)
                imp_smoke = 0 if custom_quit_smoking else int(smoking)
            else:
                imp_sleep, imp_steps, imp_stress, imp_diet, imp_smoke = proj_sleep, proj_steps, proj_stress, proj_diet, int(smoking)

            proj_df_imp = pd.DataFrame([[age + y, max(15, bmi - y * 0.3), imp_sleep, imp_steps,
                                         imp_diet, imp_stress, imp_smoke]], columns=feature_cols)
            risks_improved.append(model.predict_proba(proj_df_imp)[0][1] * 100)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=years, y=risks_current, name="Current Lifestyle",
            line=dict(color="#ef4444", width=3), fill='tozeroy', fillcolor='rgba(239,68,68,0.08)',
            mode='lines+markers', marker=dict(size=8, color="#ef4444")))
        fig2.add_trace(go.Scatter(x=years, y=risks_improved, name="Improved Lifestyle",
            line=dict(color="#10b981", width=3), fill='tozeroy', fillcolor='rgba(16,185,129,0.08)',
            mode='lines+markers', marker=dict(size=8, color="#10b981")))
        fig2.add_hrect(y0=0, y1=30, fillcolor="rgba(16,185,129,0.05)", line_width=0, annotation_text="Low Risk Zone")
        fig2.add_hrect(y0=30, y1=60, fillcolor="rgba(245,158,11,0.05)", line_width=0, annotation_text="Moderate Zone")
        fig2.add_hrect(y0=60, y1=100, fillcolor="rgba(239,68,68,0.05)", line_width=0, annotation_text="High Risk Zone")
        fig2.update_layout(
            title=dict(text="Your Digital Twin Future Trajectory", font=dict(color='#a5b4fc', size=18)),
            xaxis=dict(title="Years Ahead", color='#6b7280', tickvals=years),
            yaxis=dict(title="Risk of Metabolic Disorder (%)", color='#6b7280', range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,17,40,0.8)',
            legend=dict(bgcolor='rgba(30,27,75,0.8)', bordercolor='rgba(99,102,241,0.4)'),
            height=420
        )
        st.plotly_chart(fig2, use_container_width=True)

        if scenario != "📉 Current Lifestyle Continues":
            risk_diff = risks_current[4] - risks_improved[4]
            if risk_diff > 0:
                st.success(f"✅ By making these lifestyle improvements, you could reduce your 5-year risk by **{risk_diff:.1f} percentage points**!")

        # Radar chart
        st.markdown("#### 🕸️ Lifestyle Balance Radar")
        categories = ["Sleep Quality", "Physical Activity", "Diet Quality", "Stress Management", "Healthy Weight", "Non-Smoking"]
        values = [
            min(sleep / 8 * 10, 10),
            min(steps / 10000 * 10, 10),
            diet,
            10 - stress,
            max(0, 10 - max(0, bmi - 18.5) / 6.5 * 10),
            10 if not smoking else 0
        ]
        fig_radar = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(99,102,241,0.2)',
            line=dict(color='#6366f1', width=2),
            marker=dict(color='#818cf8', size=6)
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10], color='#6b7280'),
                       angularaxis=dict(color='#a5b4fc')),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e7ff'),
            height=380
        )
        st.plotly_chart(fig_radar, use_container_width=True)


    # ========== TAB 4: EXPLAINABLE AI ==========
    with tab4:
        st.markdown("### 🧠 Explainable AI — Why is Your Risk This Level?")

        col_xai, col_bar = st.columns([1, 1])

        with col_xai:
            st.markdown("#### 🔬 Feature Importance Analysis")
            feature_display_names = {
                'bmi': 'BMI', 'sleep_hours': 'Sleep Hours', 'daily_steps': 'Daily Steps',
                'diet_score': 'Diet Quality', 'stress_level': 'Stress Level',
                'smoking': 'Smoking', 'age': 'Age'
            }
            colors_map = {"↑ Risk": "#ef4444", "✓ OK": "#10b981"}

            for feat, (importance_pct, direction) in feature_explanations.items():
                color = colors_map.get(direction, "#6366f1")
                bar_width = importance_pct * 4
                val = input_data[feat].values[0]
                val_str = f"{val:.1f}" if feat not in ['smoking'] else ("Yes" if val else "No")

                st.markdown(f"""
                <div class="xai-bar">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="color:#c7d2fe; font-weight:600;">{feature_display_names.get(feat, feat)}</span>
                        <span style="color:{color}; font-weight:600;">{direction}</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="flex:1; background:rgba(255,255,255,0.1); border-radius:4px; height:8px;">
                            <div style="background:{color}; width:{min(bar_width,100)}%; height:100%; border-radius:4px; opacity:0.8;"></div>
                        </div>
                        <span style="color:#9ca3af; font-size:0.8rem; min-width:40px;">{importance_pct}%</span>
                    </div>
                    <div style="color:#6b7280; font-size:0.75rem; margin-top:2px;">Your value: {val_str}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_bar:
            st.markdown("#### 🔍 Risk Factor Breakdown")
            risk_contributions = {
                "BMI Impact": max(0, (bmi - 18.5) / 21.5 * 25) if bmi > 25 else 0,
                "Sleep Deficit": max(0, (7 - sleep) / 4 * 25) if sleep < 7 else 0,
                "Inactivity": max(0, (7000 - steps) / 6000 * 20) if steps < 7000 else 0,
                "High Stress": max(0, (stress - 5) / 5 * 15) if stress > 5 else 0,
                "Smoking": 25 if smoking else 0,
                "Poor Diet": max(0, (6 - diet) / 5 * 15) if diet < 6 else 0,
            }
            total = sum(risk_contributions.values()) or 1
            labels = list(risk_contributions.keys())
            values_pie = [v / total * current_risk_prob for v in risk_contributions.values()]
            colors_pie = ['#ef4444', '#f59e0b', '#6366f1', '#8b5cf6', '#dc2626', '#10b981']

            fig_pie = go.Figure(go.Pie(
                labels=labels, values=values_pie,
                marker_colors=colors_pie,
                hole=0.5,
                textinfo='label+percent',
                textfont=dict(color='white', size=11)
            ))
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e7ff'),
                showlegend=False,
                height=350,
                annotations=[dict(text=f'{current_risk_prob:.0f}%<br>Risk', x=0.5, y=0.5,
                                  font_size=14, font_color='#a5b4fc', showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Personalized recommendations
        st.markdown("---")
        st.markdown("#### 🎯 Personalized Recommendations (AI-Generated)")

        recs = []
        if sleep < 7:
            recs.append(("💤", "Improve Sleep", f"You need {round(7 - sleep, 1)} more hours/night. Try a consistent sleep schedule and limit screens after 9 PM."))
        if steps < 7500:
            recs.append(("👟", "Increase Activity", f"Add {7500 - steps:,} more daily steps. A 20-minute brisk walk significantly improves metabolic health."))
        if diet < 7:
            recs.append(("🥗", "Improve Diet", "Aim for more whole grains, vegetables, and lean proteins. Cut ultra-processed foods."))
        if stress > 6:
            recs.append(("🧘", "Manage Stress", "Practice 10 minutes of daily mindfulness or box breathing. High cortisol accelerates biological aging."))
        if smoking:
            recs.append(("🚭", "Quit Smoking", "Quitting smoking reduces your cardiovascular risk by 50% within 1 year."))
        if bmi > 27:
            recs.append(("⚖️", "Weight Management", f"Your BMI of {bmi} is elevated. A 5–10% reduction can significantly lower metabolic risk."))

        if recs:
            for icon, title, desc in recs:
                st.markdown(f"""
                <div style="background:rgba(30,27,75,0.7); border:1px solid rgba(99,102,241,0.3); border-radius:10px; 
                            padding:1rem; margin:0.5rem 0; display:flex; gap:1rem; align-items:flex-start;">
                    <div style="font-size:1.8rem; min-width:40px;">{icon}</div>
                    <div>
                        <div style="color:#818cf8; font-weight:700; margin-bottom:4px;">{title}</div>
                        <div style="color:#c7d2fe; font-size:0.9rem;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🏆 Excellent! Your lifestyle factors are well optimized. Keep maintaining these habits!")


    # ========== TAB 5: WOMEN'S HEALTH ==========
    with tab5:
        if gender != "Female":
            st.info("🌸 This module is designed for female users. Update your gender in your account profile.")
        else:
            st.markdown("### 🌸 Women's Health Intelligence Module")

            col_w1, col_w2 = st.columns([1, 1])

            with col_w1:
                st.markdown("#### 🌀 PCOS/PCOD Risk Assessment")
                pcos_risk, pcos_reasons = compute_pcos_risk(sleep, stress, steps, diet, bmi, cycle_irregular, gender)

                if pcos_risk is not None:
                    if pcos_risk < 30:
                        pcos_color, pcos_level = "#10b981", "🟢 Low Risk"
                    elif pcos_risk < 60:
                        pcos_color, pcos_level = "#f59e0b", "🟡 Moderate Risk"
                    else:
                        pcos_color, pcos_level = "#ef4444", "🔴 High Risk"

                    fig_pcos = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=pcos_risk,
                        title={'text': "PCOS/PCOD Lifestyle Risk", 'font': {'color': '#f9a8d4', 'size': 14}},
                        number={'suffix': "%", 'font': {'color': '#fce7f3', 'size': 36}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': '#9ca3af'},
                            'bar': {'color': "#ec4899"},
                            'bgcolor': 'rgba(0,0,0,0)',
                            'steps': [
                                {'range': [0, 30], 'color': "rgba(16,185,129,0.2)"},
                                {'range': [30, 60], 'color': "rgba(245,158,11,0.2)"},
                                {'range': [60, 100], 'color': "rgba(239,68,68,0.2)"}
                            ]
                        }
                    ))
                    fig_pcos.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', height=260,
                        font=dict(color='#fce7f3'),
                        margin=dict(t=60, b=10, l=20, r=20)
                    )
                    st.plotly_chart(fig_pcos, use_container_width=True)
                    st.markdown(f"**Risk Level: {pcos_level}**")

                    if pcos_reasons:
                        st.markdown("**Contributing lifestyle factors:**")
                        for reason in pcos_reasons:
                            st.markdown(f"<div style='color:#f9a8d4; padding:4px 0; font-size:0.9rem;'>⚠️ {reason}</div>", unsafe_allow_html=True)

                    st.caption("⚠️ This is a lifestyle-based awareness indicator. Please consult a gynaecologist for clinical diagnosis.")

            with col_w2:
                st.markdown("#### 🩺 Hormonal Health Insights")
                hormonal_insights = []
                if sleep < 6:
                    hormonal_insights.append(("😴", "Sleep & Hormones", "Sleep deprivation suppresses estrogen and elevates cortisol, disrupting the hormonal cascade."))
                if stress > 7:
                    hormonal_insights.append(("😰", "Stress & Cortisol", "Chronic stress raises cortisol, which competes with progesterone receptors and disrupts cycle regularity."))
                if diet < 5:
                    hormonal_insights.append(("🥗", "Nutrition & Hormones", "Low dietary quality reduces micronutrients needed for estrogen metabolism and thyroid function."))
                if steps < 5000:
                    hormonal_insights.append(("🏃", "Activity & Balance", "Low activity leads to insulin resistance, which dysregulates androgen levels — a key PCOS driver."))
                if bmi > 27:
                    hormonal_insights.append(("⚖️", "Weight & Estrogen", "Adipose tissue produces estrogen; excess weight can cause estrogen dominance and hormonal imbalance."))

                if hormonal_insights:
                    for icon, title, desc in hormonal_insights:
                        st.markdown(f"""
                        <div style="background:rgba(74,0,48,0.5); border:1px solid rgba(236,72,153,0.3); border-radius:10px;
                                    padding:0.8rem; margin:0.4rem 0;">
                            <div style="color:#f9a8d4; font-weight:600;">{icon} {title}</div>
                            <div style="color:#fbcfe8; font-size:0.85rem; margin-top:4px;">{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ Your lifestyle is supporting healthy hormonal balance!")

            # PCOD Risk Reduction Graph (from logged data)
            st.markdown("---")
            st.markdown("#### 📉 How Your Habits Reduce PCOD Risk Over Time")

            if len(logs) >= 3:
                sorted_logs = sorted(logs.items())
                dates_pcos = []
                pcos_risks_over_time = []
                steps_over_time = []
                cal_adherence_over_time = []

                for d, lg in sorted_logs:
                    s_steps = lg.get("steps", 5000)
                    s_sleep = lg.get("sleep", 6.5)
                    s_stress = lg.get("stress", 6)
                    s_diet = lg.get("diet_score", 5)
                    r, _ = compute_pcos_risk(s_sleep, s_stress, s_steps, s_diet, bmi, cycle_irregular, "Female")
                    if r is not None:
                        dates_pcos.append(d)
                        pcos_risks_over_time.append(r)
                        steps_over_time.append(s_steps)
                        cal_adherence = abs(lg.get("calories", target_calories) - target_calories) / target_calories * 100
                        cal_adherence_over_time.append(round(100 - cal_adherence, 1))

                if len(dates_pcos) >= 2:
                    fig_pcos_trend = go.Figure()
                    fig_pcos_trend.add_trace(go.Scatter(
                        x=dates_pcos, y=pcos_risks_over_time,
                        name="PCOD Risk %",
                        line=dict(color="#ec4899", width=3),
                        fill='tozeroy', fillcolor='rgba(236,72,153,0.1)',
                        mode='lines+markers', marker=dict(size=7, color="#ec4899")
                    ))
                    fig_pcos_trend.add_trace(go.Scatter(
                        x=dates_pcos, y=[MIN_STEPS / 1000 for _ in dates_pcos],
                        name=f"Step Target ({MIN_STEPS:,})",
                        line=dict(color="#f59e0b", width=1, dash='dot'),
                        yaxis='y2'
                    ))
                    fig_pcos_trend.add_hrect(y0=0, y1=30, fillcolor="rgba(16,185,129,0.05)", line_width=0,
                                             annotation_text="Safe Zone", annotation_font_color="#10b981")
                    fig_pcos_trend.update_layout(
                        title=dict(text="Your PCOD Risk Trend — Does Meeting Daily Goals Lower Risk?",
                                   font=dict(color='#f9a8d4', size=15)),
                        xaxis=dict(title="Date", color='#6b7280'),
                        yaxis=dict(title="PCOD Risk %", color='#ec4899', range=[0, 100]),
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)',
                        legend=dict(bgcolor='rgba(74,0,48,0.6)'),
                        height=350
                    )
                    st.plotly_chart(fig_pcos_trend, use_container_width=True)

                    # Steps vs PCOD risk correlation
                    fig_steps_pcos = go.Figure()
                    fig_steps_pcos.add_trace(go.Bar(
                        x=dates_pcos, y=steps_over_time,
                        name="Daily Steps",
                        marker_color=['#10b981' if s >= MIN_STEPS else '#ef4444' for s in steps_over_time]
                    ))
                    fig_steps_pcos.add_hline(y=MIN_STEPS, line_dash="dot", line_color="#f59e0b",
                                             annotation_text=f"Min {MIN_STEPS:,} steps target")
                    fig_steps_pcos.update_layout(
                        title=dict(text=f"Daily Steps vs. Target ({MIN_STEPS:,})", font=dict(color='#f9a8d4', size=14)),
                        xaxis=dict(color='#6b7280'), yaxis=dict(color='#6b7280'),
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)', height=280
                    )
                    st.plotly_chart(fig_steps_pcos, use_container_width=True)

                    # Long-run explanation
                    days_met = sum(1 for s in steps_over_time if s >= MIN_STEPS)
                    total_days = len(steps_over_time)
                    adherence_pct = round(days_met / total_days * 100, 1) if total_days else 0

                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#4a0030,#2d0020); border:1px solid #ec4899;
                                border-radius:14px; padding:1.2rem; margin-top:0.5rem;">
                        <div style="color:#f9a8d4; font-size:1.05rem; font-weight:700; margin-bottom:0.5rem;">
                            🔬 How Steps Reduce PCOD Risk in the Long Run
                        </div>
                        <div style="color:#fbcfe8; font-size:0.9rem; line-height:1.7;">
                            You've met your step goal on <b style="color:#f472b6;">{days_met}/{total_days} days ({adherence_pct}%)</b> of logged days.<br><br>
                            ✅ <b>Walking ≥{MIN_STEPS:,} steps daily</b> reduces insulin resistance by improving glucose uptake in muscles — 
                            directly countering one of the core drivers of PCOD/PCOS.<br><br>
                            🔁 Over 30+ consistent days, sustained activity lowers <b>fasting insulin</b>, reduces <b>androgen levels</b>, 
                            and helps restore regular ovulation cycles — improving PCOD outcomes by <b>up to 30–40%</b> according to clinical studies.<br><br>
                            📈 Keep hitting your daily targets — even partial improvement compounds over months!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("📊 Log data for at least 2 days to see your PCOD risk trend chart.")
            else:
                st.info("📊 Log your daily data for 3+ days to see personalized PCOD risk reduction graphs.")

            # Calorie/Protein vs PCOD
            if len(logs) >= 3:
                st.markdown("---")
                st.markdown("#### 🍽️ How Nutrition Goals Affect PCOD Risk")
                sorted_logs_n = sorted(logs.items())
                dates_n = [d for d, _ in sorted_logs_n]
                cal_vals = [lg.get("calories", 0) for _, lg in sorted_logs_n]
                pro_vals = [lg.get("protein", 0) for _, lg in sorted_logs_n]
                target_cal_line = [target_calories] * len(dates_n)
                target_pro_line = [target_protein] * len(dates_n)

                fig_nut = go.Figure()
                fig_nut.add_trace(go.Bar(x=dates_n, y=cal_vals, name="Calories Consumed",
                    marker_color=['#10b981' if MIN_CALORIES_PCT * target_calories <= c <= MAX_CALORIES_PCT * target_calories else '#ef4444' for c in cal_vals]))
                fig_nut.add_trace(go.Scatter(x=dates_n, y=target_cal_line, name=f"Target ({int(target_calories)} kcal)",
                    line=dict(color="#f59e0b", dash="dot", width=2)))
                fig_nut.update_layout(
                    title=dict(text="Daily Calorie Intake vs Target", font=dict(color='#6ee7b7', size=14)),
                    xaxis=dict(color='#6b7280'), yaxis=dict(color='#6b7280'),
                    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(17,17,40,0.8)', height=280,
                    legend=dict(bgcolor='rgba(30,27,75,0.8)')
                )
                st.plotly_chart(fig_nut, use_container_width=True)

                fig_pro = go.Figure()
                fig_pro.add_trace(go.Bar(x=dates_n, y=pro_vals, name="Protein Consumed (g)",
                    marker_color=['#10b981' if p >= MIN_PROTEIN_PCT * target_protein else '#ef4444' for p in pro_vals]))
                fig_pro.add_trace(go.Scatter(x=dates_n, y=target_pro_line, name=f"Target ({int(target_protein)}g)",
                    line=dict(color="#ec4899", dash="dot", width=2)))
                fig_pro.update_layout(
                    title=dict(text="Daily Protein Intake vs Target", font=dict(color='#f9a8d4', size=14)),
                    xaxis=dict(color='#6b7280'), yaxis=dict(color='#6b7280'),
                    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(17,17,40,0.8)', height=280,
                    legend=dict(bgcolor='rgba(74,0,48,0.6)')
                )
                st.plotly_chart(fig_pro, use_container_width=True)

                st.markdown("""
                <div style="background:rgba(74,0,48,0.3); border:1px solid rgba(236,72,153,0.3); border-radius:12px; padding:1rem;">
                    <div style="color:#f9a8d4; font-weight:600; margin-bottom:0.4rem;">🥗 Why Protein & Calorie Balance Matters for PCOD</div>
                    <div style="color:#fbcfe8; font-size:0.88rem; line-height:1.6;">
                        • <b>Adequate protein</b> (1.2–1.6g/kg) improves insulin sensitivity and supports muscle metabolism — 
                        reducing androgen-driving insulin spikes linked to PCOS.<br>
                        • <b>Calorie balance</b> (not too high, not too low) prevents the metabolic stress that triggers cortisol and 
                        disrupts ovarian function.<br>
                        • Meeting both goals consistently over 30 days can reduce fasting insulin by up to 20%, 
                        which directly lowers PCOD hormonal disruption.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Cycle-Aware Recommendations
            st.markdown("---")
            st.markdown("#### 📅 Cycle-Aware Recommendations")

            if cycle_day:
                phase_result = get_cycle_recommendations(cycle_day)
                if isinstance(phase_result, tuple):
                    phase, tips = phase_result
                else:
                    phase, tips = "Unknown", phase_result

                phases = ["Menstrual (1–5)", "Follicular (6–13)", "Ovulation (14–16)", "Luteal (17–28)"]
                phase_idx = 0 if cycle_day <= 5 else (1 if cycle_day <= 13 else (2 if cycle_day <= 16 else 3))

                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #4a0030, #2d0020); border:1px solid #ec4899; 
                            border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                    <div style="color:#f9a8d4; font-size:1.1rem; font-weight:700; margin-bottom:0.5rem;">
                        📅 Day {cycle_day} — {phase} Phase
                    </div>
                    <div style="display:flex; gap:4px; margin-bottom:1rem;">
                        {' '.join([f'<div style="flex:1; height:6px; border-radius:3px; background:{("rgba(236,72,153,0.8)" if i==phase_idx else "rgba(255,255,255,0.15)")}"></div>' for i, _ in enumerate(phases)])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                tip_cols = st.columns(2)
                for i, tip in enumerate(tips):
                    with tip_cols[i % 2]:
                        st.markdown(f"""
                        <div style="background:rgba(74,0,48,0.4); border-left:3px solid #ec4899; border-radius:0 8px 8px 0;
                                    padding:0.7rem; margin:0.3rem 0; color:#fbcfe8; font-size:0.9rem;">{tip}</div>
                        """, unsafe_allow_html=True)

            # Preventive Guidance
            st.markdown("---")
            st.markdown("#### 🧘 Preventive Lifestyle Guidance for Women")
            preventive = [
                ("🍵", "Anti-inflammatory diet", "Include turmeric, omega-3s, and cruciferous vegetables to support hormonal detox pathways."),
                ("🏊", "Low-impact exercise", "Swimming and yoga are highly effective for hormonal balance without overloading the adrenal system."),
                ("🌙", "Sleep hygiene", "Consistent sleep/wake times regulate melatonin and estrogen rhythm cycles."),
                ("📵", "Digital detox before bed", "Blue light suppresses melatonin and disrupts ovulation-related hormonal surges."),
            ]
            pc1, pc2 = st.columns(2)
            for i, (icon, title, desc) in enumerate(preventive):
                with (pc1 if i % 2 == 0 else pc2):
                    st.markdown(f"""
                    <div style="background:rgba(30,27,75,0.5); border:1px solid rgba(236,72,153,0.2); border-radius:10px;
                                padding:0.8rem; margin:0.3rem 0;">
                        <div style="font-size:1.4rem;">{icon}</div>
                        <div style="color:#f9a8d4; font-weight:600; margin:4px 0;">{title}</div>
                        <div style="color:#fbcfe8; font-size:0.85rem;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)


    # ========== TAB 6: HEALTH SCORE ==========
    with tab6:
        st.markdown("### 🏆 Health Score, Health Age & Achievements")

        col_score1, col_score2 = st.columns([1, 1])

        with col_score1:
            st.markdown("#### 🧬 Biological Health Age")

            age_color = "#10b981" if health_age <= age else "#ef4444"
            age_delta_str = f"{'↓' if age_delta <= 0 else '↑'} {abs(age_delta)} years vs chronological"
            age_emoji = "🟢" if health_age <= age else "🔴"

            st.markdown(f"""
            <div class="health-age-card">
                <div style="color:#a78bfa; font-size:0.9rem; margin-bottom:0.5rem;">Your Biological Health Age</div>
                <div style="font-size:4rem; font-weight:700; color:{age_color};">{health_age}</div>
                <div style="color:#c4b5fd; font-size:1rem;">years old {age_emoji}</div>
                <div style="color:#9ca3af; font-size:0.85rem; margin-top:0.5rem;">Chronological Age: {age} | {age_delta_str}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            health_score = max(0, 100 - current_risk_prob + (5 if not smoking else -15) + (5 if sleep >= 7 else -5) + (5 if steps >= 7500 else -5))
            health_score = round(min(100, max(0, health_score)))
            score_color = "#10b981" if health_score >= 70 else ("#f59e0b" if health_score >= 40 else "#ef4444")
            score_label = "Excellent" if health_score >= 80 else ("Good" if health_score >= 60 else ("Fair" if health_score >= 40 else "Needs Attention"))

            fig_score = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                title={'text': f"Overall Health Score — {score_label}", 'font': {'color': '#a5b4fc', 'size': 14}},
                number={'font': {'color': score_color, 'size': 48}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': score_color},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(239,68,68,0.15)'},
                        {'range': [40, 70], 'color': 'rgba(245,158,11,0.15)'},
                        {'range': [70, 100], 'color': 'rgba(16,185,129,0.15)'}
                    ]
                }
            ))
            fig_score.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', height=280,
                font=dict(color='#e0e7ff'),
                margin=dict(t=60, b=10, l=20, r=20)
            )
            st.plotly_chart(fig_score, use_container_width=True)

        with col_score2:
            st.markdown("#### 🎖️ Your Health Achievements")

            if badges:
                st.markdown("You've earned these badges based on your current lifestyle:")
                badge_html = "".join([f'<span class="gamification-badge">{b}</span>' for b in badges])
                st.markdown(f'<div style="margin:1rem 0;">{badge_html}</div>', unsafe_allow_html=True)
            else:
                st.info("Start improving your habits to unlock health badges!")

            st.markdown("---")
            st.markdown("#### 🎯 Goals to Unlock Next Badge")

            unlock_goals = []
            if smoking:
                unlock_goals.append(("🚭", "Quit Smoking", "Unlock 'Non-Smoker' badge + massive risk reduction"))
            if steps < 7500:
                unlock_goals.append(("👟", f"Reach {7500:,} daily steps", f"You need {7500 - steps:,} more steps/day"))
            if sleep < 7:
                unlock_goals.append(("🌙", "Sleep 7+ hours/night", f"Add {round(7-sleep,1)} more hours nightly"))
            if diet < 8:
                unlock_goals.append(("🥗", "Achieve Diet Score 8+", f"Improve diet by {8-diet} points"))
            if stress > 4:
                unlock_goals.append(("🧘", "Reduce stress to ≤4", f"Lower stress by {stress-4} points"))

            for icon, goal, desc in unlock_goals[:4]:
                st.markdown(f"""
                <div style="background:rgba(30,27,75,0.6); border:1px solid rgba(99,102,241,0.2); border-radius:10px;
                            padding:0.7rem 1rem; margin:0.4rem 0; display:flex; gap:12px; align-items:center;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div>
                        <div style="color:#818cf8; font-weight:600; font-size:0.9rem;">{goal}</div>
                        <div style="color:#6b7280; font-size:0.8rem;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Sensitivity analysis
        st.markdown("---")
        st.markdown("#### 📈 Health Score Sensitivity Analysis")
        st.caption("See how much each improvement would boost your Health Score:")

        improvements = {
            "Quit Smoking": 15 if smoking else 0,
            "+1hr Sleep": 8 if sleep < 7 else 0,
            "+2000 Steps": 7 if steps < 8000 else 0,
            "Diet +2pts": 5 if diet < 8 else 0,
            "Stress -2pts": 6 if stress > 5 else 0,
            "Lose 5kg": 5 if bmi > 25 else 0,
        }
        improvements = {k: v for k, v in improvements.items() if v > 0}

        if improvements:
            fig_imp = go.Figure(go.Bar(
                x=list(improvements.values()),
                y=list(improvements.keys()),
                orientation='h',
                marker=dict(color=list(improvements.values()), colorscale='Viridis', showscale=False),
                text=[f"+{v} pts" for v in improvements.values()],
                textposition='outside',
                textfont=dict(color='#a5b4fc')
            ))
            fig_imp.update_layout(
                xaxis=dict(title="Health Score Improvement (pts)", color='#6b7280', range=[0, 20]),
                yaxis=dict(color='#a5b4fc'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(17,17,40,0.8)',
                font=dict(color='#e0e7ff'),
                height=300,
                margin=dict(l=10, r=60, t=20, b=40)
            )
            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.success("🏆 Your lifestyle is already highly optimized — maximum health score range achieved!")


    # ========== TAB 7: MONTHLY REPORT ==========
    with tab7:
        st.markdown("### 📅 Monthly Health Report")
        st.caption("Comprehensive analysis of your logged data over the past month")

        if not logs:
            st.info("📊 No data logged yet. Start logging daily to generate your monthly report!")
        else:
            # Month selector
            available_months = sorted(set(d[:7] for d in logs.keys()), reverse=True)
            selected_month = st.selectbox("Select Month", available_months)

            month_logs = {d: v for d, v in logs.items() if d.startswith(selected_month)}

            if not month_logs:
                st.warning("No data for selected month.")
            else:
                sorted_month = sorted(month_logs.items())
                dates_m = [d for d, _ in sorted_month]
                steps_m = [lg.get("steps", 0) for _, lg in sorted_month]
                sleep_m = [lg.get("sleep", 0) for _, lg in sorted_month]
                calories_m = [lg.get("calories", 0) for _, lg in sorted_month]
                protein_m = [lg.get("protein", 0) for _, lg in sorted_month]
                stress_m = [lg.get("stress", 5) for _, lg in sorted_month]
                diet_m = [lg.get("diet_score", 5) for _, lg in sorted_month]
                exercise_m = [lg.get("exercise_min", 0) for _, lg in sorted_month]
                goals_m = [lg.get("goals_met", 0) for _, lg in sorted_month]
                n_days = len(sorted_month)

                # Summary metrics
                st.markdown(f"#### 📊 {selected_month} — Summary ({n_days} days logged)")

                m1, m2, m3, m4, m5, m6 = st.columns(6)
                with m1:
                    avg_steps = int(np.mean(steps_m))
                    st.metric("Avg Steps", f"{avg_steps:,}", f"{'✅' if avg_steps >= MIN_STEPS else '⚠️'}")
                with m2:
                    avg_sleep = round(np.mean(sleep_m), 1)
                    st.metric("Avg Sleep", f"{avg_sleep}h", f"{'✅' if avg_sleep >= 7 else '⚠️'}")
                with m3:
                    avg_cal = int(np.mean(calories_m))
                    st.metric("Avg Calories", f"{avg_cal}", f"vs {int(target_calories)}")
                with m4:
                    avg_protein = int(np.mean(protein_m))
                    st.metric("Avg Protein", f"{avg_protein}g", f"vs {int(target_protein)}g")
                with m5:
                    avg_stress = round(np.mean(stress_m), 1)
                    st.metric("Avg Stress", f"{avg_stress}/10", f"{'✅' if avg_stress <= 5 else '⚠️'}")
                with m6:
                    total_exercise = sum(exercise_m)
                    st.metric("Total Exercise", f"{total_exercise} min", f"~{round(total_exercise/n_days,0)} min/day")

                # Goal adherence
                goals_met_pct = round(sum(1 for g in goals_m if g >= 3) / n_days * 100, 1)
                steps_goal_pct = round(sum(1 for s in steps_m if s >= MIN_STEPS) / n_days * 100, 1)
                cal_goal_pct = round(sum(1 for c in calories_m if MIN_CALORIES_PCT * target_calories <= c <= MAX_CALORIES_PCT * target_calories) / n_days * 100, 1)
                protein_goal_pct = round(sum(1 for p in protein_m if p >= MIN_PROTEIN_PCT * target_protein) / n_days * 100, 1)

                st.markdown("---")
                st.markdown("#### 🎯 Monthly Goal Adherence")

                ga1, ga2, ga3, ga4 = st.columns(4)
                for col, label, pct, icon in [
                    (ga1, "Overall Goals (3+ met)", goals_met_pct, "🏆"),
                    (ga2, "Steps Goal", steps_goal_pct, "👟"),
                    (ga3, "Calorie Goal", cal_goal_pct, "🍽️"),
                    (ga4, "Protein Goal", protein_goal_pct, "💪")
                ]:
                    with col:
                        color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                        st.markdown(f"""
                        <div style="background:rgba(17,24,39,0.9); border:1px solid {color}; border-radius:12px; padding:1rem; text-align:center;">
                            <div style="font-size:1.5rem;">{icon}</div>
                            <div style="font-size:1.8rem; font-weight:700; color:{color};">{pct}%</div>
                            <div style="color:#9ca3af; font-size:0.8rem;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

                # Trend charts
                col_r1, col_r2 = st.columns(2)

                with col_r1:
                    fig_steps_m = go.Figure()
                    fig_steps_m.add_trace(go.Bar(x=dates_m, y=steps_m, name="Steps",
                        marker_color=['#10b981' if s >= MIN_STEPS else '#ef4444' for s in steps_m]))
                    fig_steps_m.add_hline(y=MIN_STEPS, line_dash="dot", line_color="#f59e0b",
                                           annotation_text=f"Target: {MIN_STEPS:,}")
                    fig_steps_m.update_layout(
                        title=dict(text="Daily Steps", font=dict(color='#a5b4fc', size=14)),
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)', height=280, showlegend=False
                    )
                    st.plotly_chart(fig_steps_m, use_container_width=True)

                with col_r2:
                    fig_sleep_m = go.Figure()
                    fig_sleep_m.add_trace(go.Scatter(x=dates_m, y=sleep_m, name="Sleep",
                        line=dict(color="#818cf8", width=2),
                        fill='tozeroy', fillcolor='rgba(129,140,248,0.1)',
                        mode='lines+markers', marker=dict(color=['#10b981' if s >= 7 else '#ef4444' for s in sleep_m], size=7)))
                    fig_sleep_m.add_hline(y=7, line_dash="dot", line_color="#f59e0b", annotation_text="7h target")
                    fig_sleep_m.update_layout(
                        title=dict(text="Sleep Duration (hrs)", font=dict(color='#a5b4fc', size=14)),
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)', height=280, showlegend=False
                    )
                    st.plotly_chart(fig_sleep_m, use_container_width=True)

                col_r3, col_r4 = st.columns(2)

                with col_r3:
                    fig_cal_m = go.Figure()
                    fig_cal_m.add_trace(go.Bar(x=dates_m, y=calories_m, name="Calories",
                        marker_color=['#10b981' if MIN_CALORIES_PCT * target_calories <= c <= MAX_CALORIES_PCT * target_calories else '#ef4444' for c in calories_m]))
                    fig_cal_m.add_hline(y=target_calories, line_dash="dot", line_color="#f59e0b",
                                         annotation_text=f"Target: {int(target_calories)}")
                    fig_cal_m.update_layout(
                        title=dict(text="Daily Calories vs Target", font=dict(color='#a5b4fc', size=14)),
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)', height=280, showlegend=False
                    )
                    st.plotly_chart(fig_cal_m, use_container_width=True)

                with col_r4:
                    fig_pro_m = go.Figure()
                    fig_pro_m.add_trace(go.Bar(x=dates_m, y=protein_m, name="Protein (g)",
                        marker_color=['#10b981' if p >= MIN_PROTEIN_PCT * target_protein else '#ef4444' for p in protein_m]))
                    fig_pro_m.add_hline(y=target_protein, line_dash="dot", line_color="#ec4899",
                                         annotation_text=f"Target: {int(target_protein)}g")
                    fig_pro_m.update_layout(
                        title=dict(text="Daily Protein (g)", font=dict(color='#a5b4fc', size=14)),
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(17,17,40,0.8)', height=280, showlegend=False
                    )
                    st.plotly_chart(fig_pro_m, use_container_width=True)

                # Stress trend
                st.markdown("#### 😰 Stress & Workload Trend")
                fig_stress_m = go.Figure()
                fig_stress_m.add_trace(go.Scatter(x=dates_m, y=stress_m, name="Stress Level",
                    line=dict(color="#f59e0b", width=2),
                    fill='tozeroy', fillcolor='rgba(245,158,11,0.1)',
                    mode='lines+markers',
                    marker=dict(color=['#ef4444' if s >= 7 else '#f59e0b' if s >= 5 else '#10b981' for s in stress_m], size=7)))
                fig_stress_m.add_hrect(y0=7, y1=10, fillcolor="rgba(239,68,68,0.07)", line_width=0, annotation_text="High Stress Zone")
                fig_stress_m.add_hrect(y0=0, y1=4, fillcolor="rgba(16,185,129,0.07)", line_width=0, annotation_text="Low Stress Zone")
                fig_stress_m.update_layout(
                    title=dict(text="Daily Stress Level", font=dict(color='#a5b4fc', size=14)),
                    yaxis=dict(range=[0, 10], color='#6b7280'),
                    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(17,17,40,0.8)', height=280, showlegend=False
                )
                st.plotly_chart(fig_stress_m, use_container_width=True)

                # PCOD risk trend (for females)
                if gender == "Female":
                    st.markdown("---")
                    st.markdown("#### 🌸 Monthly PCOD Risk Trend")

                    pcos_risks_m = []
                    for _, lg in sorted_month:
                        r, _ = compute_pcos_risk(
                            lg.get("sleep", 6.5), lg.get("stress", 6),
                            lg.get("steps", 5000), lg.get("diet_score", 5),
                            bmi, cycle_irregular, "Female"
                        )
                        pcos_risks_m.append(r if r else 0)

                    if pcos_risks_m:
                        avg_pcos = round(np.mean(pcos_risks_m), 1)
                        trend = "📉 Improving" if len(pcos_risks_m) > 1 and pcos_risks_m[-1] < pcos_risks_m[0] else "📈 Needs attention"

                        fig_pcos_m = go.Figure()
                        fig_pcos_m.add_trace(go.Scatter(x=dates_m, y=pcos_risks_m, name="PCOD Risk %",
                            line=dict(color="#ec4899", width=3),
                            fill='tozeroy', fillcolor='rgba(236,72,153,0.1)',
                            mode='lines+markers', marker=dict(size=7, color="#ec4899")))
                        fig_pcos_m.add_hline(y=30, line_dash="dot", line_color="#10b981", annotation_text="Safe Zone Threshold")
                        fig_pcos_m.update_layout(
                            title=dict(text=f"PCOD Risk Over Month — Avg: {avg_pcos}% — {trend}", font=dict(color='#f9a8d4', size=14)),
                            yaxis=dict(range=[0, 100], color='#6b7280'),
                            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(17,17,40,0.8)', height=300, showlegend=False
                        )
                        st.plotly_chart(fig_pcos_m, use_container_width=True)

                # Monthly summary text
                st.markdown("---")
                st.markdown("#### 📝 Monthly Health Summary")

                summary_items = []
                if avg_steps >= MIN_STEPS:
                    summary_items.append(f"✅ Great job! You averaged {avg_steps:,} steps/day — above your {MIN_STEPS:,} minimum target.")
                else:
                    summary_items.append(f"⚠️ You averaged {avg_steps:,} steps/day — below the {MIN_STEPS:,} target. Try adding a 15-min walk.")

                if avg_sleep >= 7:
                    summary_items.append(f"✅ Sleep averaged {avg_sleep}h — within the healthy 7–9h range.")
                else:
                    summary_items.append(f"⚠️ Sleep averaged {avg_sleep}h — below the 7h minimum. Consider a consistent sleep schedule.")

                cal_diff = avg_cal - target_calories
                if abs(cal_diff) <= target_calories * 0.15:
                    summary_items.append(f"✅ Calorie intake was well-balanced (avg {avg_cal} kcal vs target {int(target_calories)}).")
                elif cal_diff > 0:
                    summary_items.append(f"⚠️ Calorie intake was {int(cal_diff)} kcal above target on average. Watch portion sizes.")
                else:
                    summary_items.append(f"⚠️ Calorie intake was {int(abs(cal_diff))} kcal below target — ensure you're eating enough.")

                if avg_protein >= target_protein * 0.9:
                    summary_items.append(f"✅ Protein intake averaged {avg_protein}g — meeting your {int(target_protein)}g target.")
                else:
                    summary_items.append(f"⚠️ Protein averaged {avg_protein}g — below the {int(target_protein)}g target. Add more dal, eggs, or paneer.")

                if avg_stress <= 5:
                    summary_items.append(f"✅ Average stress was {avg_stress}/10 — manageable levels.")
                else:
                    summary_items.append(f"⚠️ Average stress was {avg_stress}/10. Try incorporating daily breathing or mindfulness.")

                for item in summary_items:
                    color = "#10b981" if item.startswith("✅") else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:rgba(17,24,39,0.8); border-left:3px solid {color}; border-radius:0 8px 8px 0;
                                padding:0.7rem 1rem; margin:0.4rem 0; color:#e0e7ff; font-size:0.9rem;">{item}</div>
                    """, unsafe_allow_html=True)


    # ====================== FOOTER ======================
    st.markdown("""
    <div class="footer-note">
        ⚠️ BioTwin AI is a simulation tool for awareness and preventive health education. It is NOT a substitute for medical advice, diagnosis, or treatment. 
        Always consult a qualified healthcare professional for medical decisions.<br><br>
        🧬 <strong>BioTwin AI</strong> • Built for Nirmaan 4.0 Hackathon @ MIT Academy of Engineering (GDG On Campus) • 
        Team Clutch Coders: Himani Bhurkunde, Soham Chaudhary, Sarvesh Barale, Kedar Jasud
    </div>
    """, unsafe_allow_html=True)


# ====================== ENTRY POINT ======================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    show_main_app()
else:
    show_login_screen()