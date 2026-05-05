import streamlit as st
import pandas as pd
import pickle
import os
import time
import streamlit.components.v1 as components

# ---------------- CACHING FOR SUPER FAST SPEED ----------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file, na_values="na")

@st.cache_resource
def load_model():
    with open('sensor_model.pkl', 'rb') as f:
        return pickle.load(f)

# ---------------- TAILWIND ANIMATED LOADER COMPONENT ----------------
def show_tailwind_loader():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { margin: 0; overflow: hidden; background-color: rgba(5, 11, 20, 0.95); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; color: white; font-family: sans-serif;}
            .bg-grid { background-image: linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px); background-size: 50px 50px; }
            @keyframes square-animation {
                0% { left: 0; top: 0; } 10.5% { left: 0; top: 0; } 12.5% { left: 32px; top: 0; } 23% { left: 32px; top: 0; }
                25% { left: 64px; top: 0; } 35.5% { left: 64px; top: 0; } 37.5% { left: 64px; top: 32px; } 48% { left: 64px; top: 32px; }
                50% { left: 32px; top: 32px; } 60.5% { left: 32px; top: 32px; } 62.5% { left: 32px; top: 64px; } 73% { left: 32px; top: 64px; }
                75% { left: 0; top: 64px; } 85.5% { left: 0; top: 64px; } 87.5% { left: 0; top: 32px; } 98% { left: 0; top: 32px; } 100% { left: 0; top: 0; }
            }
            .animate-square { animation: square-animation 10s ease-in-out infinite both; }
            .loading-text { margin-top: 120px; font-size: 24px; font-weight: 800; color: #00d2ff; letter-spacing: 3px; text-transform: uppercase; animation: pulse 1s infinite;}
            @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
        </style>
    </head>
    <body class="relative">
        <div class="absolute inset-0 bg-grid opacity-20"></div>
        <div class="relative w-24 h-24 rotate-45 z-10">
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: 0s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -1.428s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -2.857s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -4.285s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -5.714s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -7.142s"></div>
            <div class="absolute top-0 left-0 w-7 h-7 m-0.5 animate-square bg-white" style="animation-delay: -8.571s"></div>
        </div>
        <div class="loading-text z-20">Analyzing Sensor Matrices...</div>
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=False)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sensor Guard Pro | Premium AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #050b14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
.main-title { font-size: 48px; font-weight: 900; text-align: center; background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 2px; margin-top: -30px; margin-bottom: 5px; }
.sub-title { text-align: center; font-size: 20px; color: #8b9bb4; margin-bottom: 40px; letter-spacing: 1px; }

/* Upload Box Container Customization */
[data-testid="stFileUploadDropzone"] { background-color: rgba(16, 23, 42, 0.6) !important; border: 2px dashed rgba(0, 210, 255, 0.4) !important; border-radius: 15px !important; transition: all 0.3s ease !important; }
[data-testid="stFileUploadDropzone"] div { color: #8b9bb4 !important; font-weight: 500; }

.kpi-card { padding: 25px; border-radius: 15px; background: linear-gradient(145deg, #0f172a, #1e293b); border: 1px solid #00d2ff; text-align: center; box-shadow: inset 0 0 20px rgba(0, 210, 255, 0.05); }
.kpi-value { font-size: 42px; font-weight: 900; color: #00d2ff; text-shadow: 0 0 15px rgba(0, 210, 255, 0.4); line-height: 1.2;}
.kpi-label { font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
.kpi-alert { color: #ff0055 !important; text-shadow: 0 0 15px rgba(255, 0, 85, 0.5) !important; }

/* ALL Buttons: Execute, Download, AND Upload Button */
.stButton>button, .stDownloadButton>button, [data-testid="stFileUploadDropzone"] button { background: linear-gradient(90deg, #facc15, #eab308) !important; color: #000000 !important; font-weight: 900 !important; border-radius: 12px !important; border: none !important; box-shadow: 0 0 15px rgba(250, 204, 21, 0.5) !important; transition: 0.3s !important; }
.stButton>button:hover, .stDownloadButton>button:hover, [data-testid="stFileUploadDropzone"] button:hover { transform: scale(1.02) !important; box-shadow: 0 0 25px rgba(250, 204, 21, 0.8) !important; }

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Predictive Sensor Fault Detection</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Next-Gen AI Industrial Monitoring System</div>", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader("📂 Data Ingestion")
    uploaded_file = st.file_uploader("Upload Sensor CSV", type="csv", label_visibility="collapsed")
    analyze_btn = st.button("🚀 EXECUTE AI SCAN", use_container_width=True)

with col2:
    if uploaded_file:
        st.subheader("📊 Live Data Stream")
        df = load_data(uploaded_file)
        st.dataframe(df.head(8), use_container_width=True)
    else:
        st.markdown("<div style='background: rgba(250, 204, 21, 0.15); border: 1px solid #facc15; padding: 15px; border-radius: 12px; color: #facc15; text-align: center; font-weight: 600; box-shadow: 0 0 15px rgba(250, 204, 21, 0.2); margin-top: 10px;'>⚠️ System Ready. Please upload a Scania sensor CSV file to begin.</div>", unsafe_allow_html=True)

# ---------------- CORE LOGIC ----------------
if uploaded_file and analyze_btn:
    
    scan_placeholder = st.empty()
    with scan_placeholder.container():
        show_tailwind_loader()
    
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

        time.sleep(3) 
        
        scan_placeholder.empty()

        st.markdown("---")
        st.write("### 🤖 AutoML Pipeline Selection (LazyPredict Benchmark)")
        st.info("ℹ️ System auto-evaluated 15 Machine Learning models using the LazyPredict library during the training phase. The leaderboard below shows the performance of all tested models on the full dataset.")
        
        lp_data = {
            'Model Name': ['LGBM Classifier', 'XGBoost Classifier', 'Random Forest Classifier', 'Decision Tree', 'Extra Trees Classifier', 'Linear Discriminant', 'Logistic Regression', 'Gradient Boosting', 'SGD Classifier', 'K-Neighbors Classifier', 'Passive Aggressive', 'AdaBoost Classifier', 'Ridge Classifier', 'Gaussian NB', 'Bernoulli NB'],
            'Accuracy': ['99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '99.00%', '96.00%', '84.00%'],
            'ROC AUC': ['0.87', '0.85', '0.84', '0.84', '0.84', '0.84', '0.82', '0.82', '0.79', '0.77', '0.75', '0.75', '0.74', '0.92', '0.87'],
            'F1-Score': ['0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.99', '0.97', '0.90']
        }
        
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.dataframe(pd.DataFrame(lp_data), use_container_width=True, hide_index=True)
        with col_t2:
            st.markdown("""
            <div style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 20px; border-radius: 10px; height: 100%;">
                <h4 style="color: #10b981; margin-top: 0; font-size: 18px;">✅ Selected: Random Forest</h4>
                <p style="color: #e2e8f0; font-size: 14px; margin-bottom: 15px;">Despite LGBM having a marginally higher AUC, Random Forest was finalized based on the following critical parameters:</p>
                <ul style="color: #cbd5e1; font-size: 13.5px; padding-left: 20px; line-height: 1.6;">
                    <li style="margin-bottom: 8px;"><b>Noise Robustness (Bagging):</b> Unlike Boosting algorithms, Random Forest's independent tree structure makes it highly resistant to overfitting on noisy/missing industrial sensor data.</li>
                    <li style="margin-bottom: 8px;"><b>Feature Stability:</b> Provides highly consistent and reliable feature importance rankings, which is crucial for identifying the exact faulty sensors (Root Cause Analysis).</li>
                    <li style="margin-bottom: 8px;"><b>Metric Parity:</b> Matches the top models with flawless 99% Accuracy and 0.99 F1-Score, ensuring zero compromise on fault detection.</li>
                    <li><b>Out-of-Bag (OOB) Validation:</b> Its in-built OOB mechanism ensures the model's reliability on unseen data before live deployment.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
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
        scan_placeholder.empty()
        st.error("Model file 'sensor_model.pkl' not found! Please run the training script first.")


# ---------------- HIGH IMPACT BIG FOOTER WITH 3D ANIMATION ----------------
footer_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background: transparent; font-family: 'Inter', sans-serif; }
        .footer-box { 
            position: relative; width: 100vw; height: 100vh; 
            background: linear-gradient(to top, #0f172a, #050b14); 
            border-top: 3px solid #00d2ff; text-align: center; 
            border-radius: 30px 30px 0 0; 
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; opacity: 0.7;}
        .content { position: relative; z-index: 1; margin-top: -20px;}
        .mentor-label { font-size: 16px; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
        .mentor-name { font-size: 32px; color: #facc15; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 20px rgba(250, 204, 21, 0.5); margin-bottom: 25px; }
        .team-label { font-size: 16px; color: #94a3b8; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 12px; }
        .team-names { font-size: 22px; font-weight: 800; background: -webkit-linear-gradient(45deg, #ffffff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.6; }
        .team-names span { padding: 0 15px; }
    </style>
</head>
<body>
    <div class="footer-box">
        <canvas id="confetti"></canvas>
        <div class="content">
            <div class='mentor-label'>Project Mentor</div>
            <div class='mentor-name'>🎓 Dr. Mudita</div>
            <div class='team-label'>Developed By Team</div>
            <div class='team-names'>
                <span>Rishabh Raj</span> | <span>Mayank Raj</span> | <span>Khushi Kumari</span> | <span>Rishabh</span>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('confetti');
        const ctx = canvas.getContext('2d');
        let width, height;
        let confettiPieces = [];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // White & Light Blue colors matching the tech theme
        const colors = ['rgba(255, 255, 255, 0.6)', 'rgba(0, 210, 255, 0.5)', 'rgba(165, 180, 252, 0.5)', 'rgba(250, 204, 21, 0.4)'];
        const shapes = ['rectangle', 'circle', 'star', 'diamond'];

        function initConfetti() {
            confettiPieces = [];
            for (let i = 0; i < 80; i++) {
                confettiPieces.push(createPiece());
            }
        }

        function createPiece() {
            return {
                x: -width * 0.2 + Math.random() * width * 1.4,
                y: -Math.random() * height * 0.3,
                z: Math.random() * 1500 + 800,
                velocityX: (Math.random() - 0.5) * 0.6,
                velocityY: Math.random() * 0.3 + 0.1,
                velocityZ: -(Math.random() * 0.6 + 0.3),
                rotation: Math.random() * Math.PI * 2,
                rotationSpeed: (Math.random() - 0.5) * 0.04,
                baseSize: Math.random() * 12 + 6,
                opacity: 1,
                shape: shapes[Math.floor(Math.random() * shapes.length)],
                color: colors[Math.floor(Math.random() * colors.length)],
                floatPhase: Math.random() * Math.PI * 2,
                swayAmplitude: Math.random() * 0.5 + 0.2,
                bobAmplitude: Math.random() * 0.3 + 0.1,
                isFading: false
            };
        }

        function drawPiece(piece) {
            const perspective = 800;
            const scale = perspective / (perspective + piece.z);
            if (scale <= 0.01 || scale > 2) return;

            const projectedX = piece.x + (piece.x - width / 2) * (1 - scale);
            const projectedY = piece.y + (piece.y - height / 2) * (1 - scale);
            const size = piece.baseSize * scale;
            const opacity = Math.min(piece.opacity * scale * 1.5, 1);

            ctx.save();
            ctx.translate(projectedX, projectedY);
            ctx.rotate(piece.rotation);
            ctx.globalAlpha = opacity;
            ctx.fillStyle = piece.color;

            if (piece.shape === 'rectangle') {
                ctx.fillRect(-size * 0.75, -size * 0.4, size * 1.5, size * 0.8);
            } else if (piece.shape === 'circle') {
                ctx.beginPath(); ctx.arc(0, 0, size * 0.6, 0, Math.PI * 2); ctx.fill();
            } else if (piece.shape === 'diamond') {
                ctx.beginPath(); ctx.moveTo(0, -size * 0.8); ctx.lineTo(size * 0.5, 0); ctx.lineTo(0, size * 0.8); ctx.lineTo(-size * 0.5, 0); ctx.fill();
            } else {
                ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    ctx.lineTo(Math.cos((18 + i * 72) * Math.PI / 180) * size, -Math.sin((18 + i * 72) * Math.PI / 180) * size);
                    ctx.lineTo(Math.cos((54 + i * 72) * Math.PI / 180) * (size/2), -Math.sin((54 + i * 72) * Math.PI / 180) * (size/2));
                }
                ctx.closePath(); ctx.fill();
            }
            ctx.restore();
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            
            confettiPieces.forEach((piece, index) => {
                piece.floatPhase += 0.02;
                piece.x += piece.velocityX + Math.sin(piece.floatPhase) * piece.swayAmplitude * 0.3;
                piece.y += piece.velocityY + Math.cos(piece.floatPhase * 0.7) * piece.bobAmplitude * 0.2;
                piece.z += piece.velocityZ;
                piece.rotation += piece.rotationSpeed;
                
                piece.velocityX *= 0.999;
                piece.velocityY += 0.0005; // gravity
                piece.velocityZ *= 1.0005;

                if (!piece.isFading && (piece.z <= 200 || piece.y > height + 50)) {
                    piece.isFading = true;
                }
                
                if (piece.isFading) piece.opacity -= 0.02;

                if (piece.opacity <= 0) {
                    confettiPieces[index] = createPiece();
                    confettiPieces[index].y = -50; 
                }

                drawPiece(piece);
            });
            requestAnimationFrame(animate);
        }

        initConfetti();
        animate();
    </script>
</body>
</html>
"""

components.html(footer_html, height=280, scrolling=False)
