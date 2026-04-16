# 🧬 BioTwin AI — Your Digital Health Twin

**BioTwin AI** is an AI-powered preventive healthcare web app that simulates your future health, analyzes lifestyle risks, and provides personalized insights to help you live healthier.

Built using **Streamlit**, **Machine Learning**, and **Data Visualization**, this app acts as your **real-time digital health twin**.

---

## 🚀 Features

### 📊 Smart Health Dashboard
- BMI, sleep, steps, diet, and stress tracking  
- AI-generated **5-year metabolic risk prediction**  
- Organ-level health impact (heart, lungs, brain, etc.)

### 📝 Daily Health Logging
- Track:
  - Steps, sleep, exercise  
  - Calories & protein intake  
  - Mood, stress, workload  
- Automatic:
  - Diet score calculation  
  - Stress estimation  
  - Goal tracking & streaks  

### ⏳ Future Simulation
- Predict your health trajectory for **1–5 years**  
- Compare:
  - Current lifestyle vs improved habits  
  - Custom lifestyle scenarios  
- Visual risk projections with charts  

### 🧠 Explainable AI (XAI)
- Understand **why your risk is high/low**  
- Feature importance breakdown  
- Personalized actionable recommendations  

### 🌸 Women's Health Module
- PCOS/PCOD risk estimation  
- Hormonal health insights  
- Cycle-based recommendations  
- Lifestyle impact tracking on PCOS risk  

### 🏆 Gamification
- Earn badges like:
  - 🏃 Step Champion  
  - 🥗 Nutrition Pro  
  - 🧘 Zen Mode  
- Maintain daily streaks  

### 📅 Monthly Insights
- Track trends over time  
- Correlate habits with risk reduction  

---

## 🧠 AI & Data Science

- Model: `RandomForestClassifier`  
- Synthetic dataset (1000 samples)  

### Features Used
- Age  
- BMI  
- Sleep hours  
- Daily steps  
- Diet score  
- Stress level  
- Smoking  

### Risk Logic
The model predicts **metabolic disorder risk probability (%)** based on lifestyle patterns.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **ML:** Scikit-learn  
- **Visualization:** Plotly  
- **Data:** Pandas, NumPy  
- **Storage:** JSON (local file-based DB)  
- **Auth:** SHA-256 password hashing  

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/biotwin-ai.git

# Navigate into project
cd biotwin-ai

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
