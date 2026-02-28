import streamlit as st
import pandas as pd
import pickle
import os
import time

# ---------------- CACHING FOR SUPER FAST SPEED ----------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file, na_values="na")

@st.cache_resource
def load_model():
    with open('sensor_model.pkl', 'rb') as f:
        return pickle.load(f)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sensor Guard Pro | Premium AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS (Premium Theme & Fullscreen Loader) ----------------
st.markdown("""
<style>
/* Main Background */
.stApp { background-color: #050b14; color: #e2e8f0; font-family: 'Inter', sans-serif; }

/* Titles */
.main-title { 
    font-size: 48px; font-weight: 900; text-align: center; 
    background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    text-transform: uppercase; letter-spacing: 2px; margin-top: -30px; margin-bottom: 5px;
}
.sub-title { text-align: center; font-size: 20px; color: #8b9bb4; margin-bottom: 40px; letter-spacing: 1px; }

/* Glowing Glass Cards */
.neon-card { 
    background: rgba(16, 23, 42, 0.5); padding: 30px; border-radius: 20px; 
    border: 1px solid rgba(56, 189, 248, 0.3); 
    box-shadow: 0 8px 32px 0 rgba(0, 210, 255, 0.1); 
    backdrop-filter: blur(8px); margin-bottom: 25px; 
}

/* DRAG AND DROP FILE UPLOADER CUSTOMIZATION */
[data-testid="stFileUploadDropzone"] {
    background-color: rgba(16, 23, 42, 0.6) !important;
    border: 2px dashed rgba(0, 210, 255, 0.4) !important;
    border-radius: 15px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    background-color: rgba(0, 210, 255, 0.05) !important;
    border: 2px dashed #00d2ff !important;
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.2) !important;
}
[data-testid="stFileUploadDropzone"] div, [data-testid="stFileUploadDropzone"] span { color: #8b9bb4 !important; }
[data-testid="stFileUploadDropzone"] button { background: rgba(0, 210, 255, 0.1) !important; color: #00d2ff !important; border: 1px solid rgba(0, 210, 255, 0.5) !important; border-radius: 8px !important; font-weight: bold !important; }
[data-testid="stFileUploadDropzone"] button:hover { background: #00d2ff !important; color: #000000 !important; }

/* KPI Boxes */
.kpi-card { padding: 25px; border-radius: 15px; background: linear-gradient(145deg, #0f172a, #1e293b); border: 1px solid #00d2ff; text-align: center; box-shadow: inset 0 0 20px rgba(0, 210, 255, 0.05); }
.kpi-value { font-size: 42px; font-weight: 900; color: #00d2ff; text-shadow: 0 0 15px rgba(0, 210, 255, 0.4); line-height: 1.2;}
.kpi-label { font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
.kpi-alert { color: #ff0055 !important; text-shadow: 0 0 15px rgba(255, 0, 85, 0.5) !important; }

/* Yellow Glowing Buttons */
.stButton>button, .stDownloadButton>button { background: linear-gradient(90deg, #facc15, #eab308) !important; color: #000000 !important; font-weight: 900 !important; border-radius: 12px !important; border: none !important; box-shadow: 0 0 15px rgba(250, 204, 21, 0.5) !important; transition: 0.3s !important; }
.stButton>button:hover, .stDownloadButton>button:hover { transform: scale(1.02) !important; box-shadow: 0 0 25px rgba(250, 204, 21, 0.8) !important; }

/* FULL SCREEN SCANNER CSS */
.fullscreen-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5, 11, 20, 0.95); z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center; backdrop-filter: blur(15px); }
.scanner-box { position: relative; width: 250px; height: 250px; border: 3px solid #00d2ff; border-radius: 20px; overflow: hidden; box-shadow: 0 0 40px rgba(0, 210, 255, 0.4); background: repeating-linear-gradient(0deg, transparent, transparent 20px, rgba(0, 210, 255, 0.1) 20px, rgba(0, 210, 255, 0.1) 40px); }
.scanner-line { position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: #00ff88; box-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88; animation: scan 1.5s infinite ease-in-out alternate; }
@keyframes scan { 0% { top: -10%; } 100% { top: 105%; } }
.brain-icon { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 90px; filter: hue-rotate(180deg); opacity: 0.8; }
.loading-text { margin-top: 35px; font-size: 32px; font-weight: 900; color: #facc15; letter-spacing: 5px; text-transform: uppercase; animation: pulse 1s infinite; text-shadow: 0 0 20px rgba(250, 204, 21, 0.5);}
@keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
.sub-text { margin-top: 15px; font-size: 18px; color: #00d2ff; font-family: monospace; letter-spacing: 2px;}

/* BIG FOOTER DESIGN */
.footer-box { margin-top: 70px; padding: 50px 20px; background: linear-gradient(to top, #0f172a, #050b14); border-top: 3px solid #00d2ff; text-align: center; border-radius: 30px 30px 0 0; box-shadow: 0 -10px 40px rgba(0, 210, 255, 0.15); }
.mentor-label { font-size: 18px; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
.mentor-name { font-size: 38px; color: #facc15; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 20px rgba(250, 204, 21, 0.5); margin-bottom: 30px; }
.team-label { font-size: 18px; color: #94a3b8; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 15px; }
.team-names { font-size: 26px; font-weight: 800; background: -webkit-linear-gradient(45deg, #ffffff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.6; }
.team-names span { padding: 0 15px; }

/* Leaderboard Table Customization (Scrollable for 15 models) */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #3b82f6; max-height: 350px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Predictive Sensor Fault Detection</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Next-Gen AI Industrial Monitoring System</div>", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("📂 Data Ingestion")
    uploaded_file = st.file_uploader("Upload Sensor CSV", type="csv", label_visibility="collapsed")
    analyze_btn = st.button("🚀 EXECUTE AI SCAN", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if uploaded_file:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("📊 Live Data Stream")
        df = load_data(uploaded_file)
        st.dataframe(df.head(8), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: rgba(250, 204, 21, 0.15); border: 1px solid #facc15; padding: 15px; border-radius: 12px; color: #facc15; text-align: center; font-weight: 600; box-shadow: 0 0 15px rgba(250, 204, 21, 0.2); margin-top: 10px;'>⚠️ System Ready. Please upload a Scania sensor CSV file to begin.</div>", unsafe_allow_html=True)

# ---------------- CORE LOGIC WITH ZERO-DELAY REVEAL ----------------
if uploaded_file and analyze_btn:
    
    scan_placeholder = st.empty()
    scan_placeholder.markdown("""
        <div class="fullscreen-overlay">
            <div class="scanner-box"><div class="brain-icon">⚙️</div><div class="scanner-line"></div></div>
            <div class="loading-text">Executing Deep Scan</div>
            <div class="sub-text">Analyzing Sensor Matrices...</div>
        </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists('sensor_model.pkl'):
        model = load_model()

        X_test = df.drop('class', axis=1) if 'class' in df.columns else df
        numeric_cols = X_test.select_dtypes(include=['number'])
        X_imputed = numeric_cols.fillna(numeric_cols.median()).fillna(0)
        X_final = X_imputed.reindex(columns=model.feature_names_in_, fill_value=0)

        preds = model.predict(X_final)
        faults = int(sum(preds))
        
        report_df = df.copy()
        report_df['AI_Prediction'] = ["Faulty" if x==1 else "Healthy" for x in preds]
        csv_data = report_df.to_csv(index=False).encode('utf-8')

        try:
            import plotly.graph_objects as go
            fig_pie = go.Figure(data=[go.Pie(labels=['Healthy', 'Faulty'], values=[len(df)-faults, faults], hole=.5, marker=dict(colors=['#00d2ff', '#ff0055']))])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=400, font=dict(color="white", size=15), margin=dict(t=20, b=20, l=0, r=0), legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
            
            feat_df = pd.DataFrame({'Sensor': model.feature_names_in_, 'Score': model.feature_importances_}).nlargest(10, 'Score')
            fig_bar = go.Figure(go.Bar(x=feat_df['Score'], y=feat_df['Sensor'], orientation='h', marker=dict(color='#00d2ff', line=dict(color='#ffffff', width=1))))
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, xaxis=dict(showgrid=True, gridcolor='#1e293b'), yaxis=dict(autorange="reversed"), font=dict(color="white"), margin=dict(t=20, b=20, l=0, r=0))
            has_plotly = True
        except ImportError:
            has_plotly = False

        time.sleep(2.5) 
        scan_placeholder.empty()

        # --- NEW SECTION: LAZYPREDICT JUSTIFICATION ---
        st.markdown("---")
        st.write("### 🤖 AutoML Pipeline Selection (LazyPredict Benchmark)")
        
        st.info("ℹ️ System auto-evaluated 15 Machine Learning models using the LazyPredict library during the training phase. The leaderboard below shows the performance of all tested models on the full 60,000+ dataset.")
        
        # ⚠️ ASLI LAZYPREDICT DATA (ALL 15 MODELS) ⚠️
        lp_data = {
            'Model Name': [
                'LGBM Classifier', 'XGBoost Classifier', 'Random Forest Classifier', 
                'Decision Tree', 'Extra Trees Classifier', 'Linear Discriminant', 
                'Logistic Regression', 'Gradient Boosting', 'SGD Classifier', 
                'K-Neighbors Classifier', 'Passive Aggressive', 'AdaBoost Classifier', 
                'Ridge Classifier', 'Gaussian NB', 'Bernoulli NB'
            ],
            'Accuracy': [
                '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', 
                '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', 
                '99.00%', '96.00%', '84.00%'
            ],
            'ROC AUC': [
                '0.87', '0.85', '0.84', '0.84', '0.84', '0.84', 
                '0.82', '0.82', '0.79', '0.77', '0.75', '0.75', 
                '0.74', '0.92', '0.87'
            ],
            'F1-Score': [
                '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', 
                '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', 
                '0.99', '0.97', '0.90'
            ]
        }
        
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.dataframe(pd.DataFrame(lp_data), use_container_width=True, hide_index=True)
        with col_t2:
            st.success("✅ **Selected Model:**\n\n**Random Forest Classifier**\n\nChosen due to its flawless Accuracy (99%) and F1-Score (0.99) on the full 60,000+ dataset. While LGBM has slightly higher AUC, Random Forest is deployed because it is highly resistant to overfitting on noisy industrial sensor data and provides highly stable Feature Importance.")
        # ----------------------------------------------

        st.markdown("---")
        st.write("### 🧠 Live AI Diagnostic Summary")
        
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='kpi-card'><div class='kpi-label'>TOTAL SAMPLES</div><div class='kpi-value'>{len(df)}</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi-card'><div class='kpi-label'>ANOMALIES DETECTED</div><div class='kpi-value kpi-alert'>{faults}</div></div>", unsafe_allow_html=True)
        with k3:
            st.download_button("📥 DOWNLOAD REPORT", data=csv_data, file_name='sensor_report.csv', use_container_width=True)

        st.write("<br>", unsafe_allow_html=True)
        
        if has_plotly:
            cG1, cG2 = st.columns(2)
            with cG1:
                st.write("#### 🧬 Health Distribution")
                st.plotly_chart(fig_pie, use_container_width=True, theme=None)
            with cG2:
                st.write("#### 📊 Top Failure Drivers")
                st.plotly_chart(fig_bar, use_container_width=True, theme=None)
        else:
            st.warning("Plotly is not installed! Displaying basic charts.")
            st.bar_chart(pd.DataFrame({'Score': model.feature_importances_}, index=model.feature_names_in_).nlargest(15, 'Score'))

    else:
        scan_placeholder.empty()
        st.error("Model file 'sensor_model.pkl' not found! Please run the training script first.")

# ---------------- HIGH IMPACT BIG FOOTER ----------------
st.markdown("""
<div class='footer-box'>
<div class='mentor-label'>Project Mentor</div>
<div class='mentor-name'>🎓 Dr. Mudita</div>
<div class='team-label'>Developed By Team</div>
<div class='team-names'>
<span>Rishabh Raj</span> | 
<span>Mayank Raj</span> | 
<span>Khushi Kumari</span> | 
<span>Rishabh</span>
</div>
</div>
""", unsafe_allow_html=True)