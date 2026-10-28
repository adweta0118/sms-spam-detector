import streamlit as st
import joblib
import re
import html

st.set_page_config(
    page_title="SMS Shield | Spam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_models():
    model = joblib.load("sms_spam_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_models()
except Exception as e:
    st.error("Unable to load the trained model. Please check your model files.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #635bff;
    --secondary: #8b5cf6;
    --text: #172033;
    --muted: #64748b;
    --surface: #ffffff;
    --border: #e5e7eb;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #ede9fe 0%, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #dbeafe 0%, transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1100px;
    padding: 1.5rem 2rem 3rem 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 5px 0 35px 0;
}

.brand-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 48px;
    height: 48px;
    border-radius: 15px;
    color: white;
    font-size: 25px;
    background: linear-gradient(135deg, #635bff, #a855f7);
    box-shadow: 0 8px 20px #635bff35;
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #172033;
    letter-spacing: -0.8px;
}

.brand-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
}

.status-pill {
    display: inline-block;
    padding: 7px 12px;
    border: 1px solid #bbf7d0;
    background: #f0fdf4;
    color: #15803d;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
}

.hero {
    text-align: center;
    padding: 15px 10px 25px 10px;
}

.eyebrow {
    color: #635bff;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 53px);
    line-height: 1.13;
    letter-spacing: -2px;
    font-weight: 800;
    color: #172033;
    margin: 0 0 17px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #635bff, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 570px;
    margin: auto;
    color: #64748b;
    font-size: 15px;
    line-height: 1.8;
}

.feature-row {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 22px 0 28px 0;
}

.feature-chip {
    padding: 9px 13px;
    border: 1px solid #e5e7eb;
    background: #ffffffc9;
    border-radius: 30px;
    color: #475569;
    font-size: 12px;
    font-weight: 600;
}

.main-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 15px 45px #1e293b0b;
}

.section-label {
    color: #172033;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 7px;
}

.section-help {
    color: #64748b;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 20px;
}

div[data-testid="stTextArea"] textarea {
    border: 1px solid #dbe2ef;
    border-radius: 13px;
    background: #fbfcff;
    color: #172033;
    font-size: 15px;
    line-height: 1.7;
    padding: 15px;
    min-height: 155px;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #635bff;
    box-shadow: 0 0 0 3px #635bff18;
}

.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #635bff, #8055f6);
    color: white;
    border: none;
    box-shadow: 0 5px 15px #635bff30;
}

.stButton > button:hover {
    border-color: #635bff;
    transform: translateY(-1px);
}

.result-card {
    border-radius: 17px;
    padding: 23px;
    margin-top: 20px;
    border: 1px solid;
}

.result-spam {
    background: #fff1f2;
    border-color: #fecdd3;
}

.result-safe {
    background: #f0fdf4;
    border-color: #bbf7d0;
}

.result-title {
    font-size: 23px;
    font-weight: 800;
    margin: 8px 0;
}

.result-description {
    font-size: 13px;
    line-height: 1.7;
    color: #475569;
}

.result-icon {
    font-size: 30px;
}

.confidence-track {
    background: #e2e8f0;
    border-radius: 20px;
    height: 8px;
    overflow: hidden;
    margin: 12px 0;
}

.confidence-fill {
    height: 8px;
    border-radius: 20px;
    background: linear-gradient(90deg, #635bff, #a855f7);
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 15px;
    padding: 16px;
    margin-top: 15px;
}

.metric-label {
    color: #64748b;
    font-size: 12px;
    margin-bottom: 7px;
}

.metric-value {
    color: #172033;
    font-size: 22px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.info-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 17px;
    padding: 20px;
    height: 100%;
}

.info-icon {
    font-size: 25px;
    margin-bottom: 12px;
}

.info-title {
    color: #172033;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 7px;
}

.info-text {
    color: #64748b;
    font-size: 12px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 28px 10px 10px 10px;
    line-height: 1.8;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }

    .brand {
        margin-bottom: 25px;
    }

    .brand-name {
        font-size: 19px;
    }

    .hero {
        padding: 5px 0 15px 0;
    }

    .hero h1 {
        font-size: 35px;
        letter-spacing: -1.2px;
    }

    .hero p {
        font-size: 13px;
    }

    .main-card {
        padding: 18px 14px;
        border-radius: 17px;
    }

    .feature-row {
        gap: 7px;
    }

    .feature-chip {
        font-size: 11px;
        padding: 8px 10px;
    }

    .result-title {
        font-size: 21px;
    }

    .stButton > button {
        width: 100%;
    }
}

@media (max-width: 420px) {
    .hero h1 {
        font-size: 30px;
    }

    .brand-icon {
        width: 42px;
        height: 42px;
        font-size: 21px;
    }

    .main-card {
        padding: 15px 11px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand">
    <div class="brand-icon">🛡️</div>
    <div>
        <div class="brand-name">SMS Shield</div>
        <div class="brand-sub">Smart message protection</div>
    </div>
</div>

<div class="hero">
    <div class="eyebrow">AI-powered message security</div>
    <h1>Stay safe from<br><span class="gradient-text">SMS scams.</span></h1>
    <p>
        Check suspicious text messages in seconds.
        Our machine learning model helps you identify spam
        and keep unwanted messages at a distance.
    </p>
</div>

<div class="feature-row">
    <div class="feature-chip">🤖 Machine Learning</div>
    <div class="feature-chip">⚡ Instant Analysis</div>
    <div class="feature-chip">📱 Mobile Friendly</div>
    <div class="feature-chip">🔐 Privacy Focused</div>
</div>
""", unsafe_allow_html=True)

left_space, center, right_space = st.columns([0.5, 8, 0.5])

with center:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">✉️ Analyze a message</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="section-help">Paste an SMS below, or try one of the examples to see how the detector works.</div>',
        unsafe_allow_html=True
    )

    examples = {
        "🎁 Prize message": "Congratulations! You have won a free prize. Click here to claim your reward now!",
        "🏦 Bank alert": "URGENT! Your bank account will be blocked. Verify your details immediately.",
        "👋 Normal message": "Hey, are we still meeting at college tomorrow? Let me know."
    }

    if "sms_input" not in st.session_state:
        st.session_state.sms_input = ""

    st.markdown("**Try a sample message**")

    sample_cols = st.columns(3)

    for i, (label, message) in enumerate(examples.items()):
        with sample_cols[i]:
            if st.button(label, key=f"sample_{i}", use_container_width=True):
                st.session_state.sms_input = message
                st.session_state.pop("prediction_result", None)
                st.rerun()

    sms = st.text_area(
        "Your SMS message",
        key="sms_input",
        placeholder="Example: Congratulations! You have won a free gift...",
        height=155,
        max_chars=5000,
        label_visibility="collapsed"
    )

    word_count = len(re.findall(r"\b[\w']+\b", sms))
    char_count = len(sms)

    metric1, metric2 = st.columns(2)

    with metric1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Characters</div>
            <div class="metric-value">{char_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Words</div>
            <div class="metric-value">{word_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    check_col, clear_col = st.columns([2, 1])

    with check_col:
        check_clicked = st.button(
            "🛡️  Analyze Message",
            type="primary",
            use_container_width=True
        )

    with clear_col:
        clear_clicked = st.button(
            "↻  Clear",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state.sms_input = ""
        st.session_state.pop("prediction_result", None)
        st.rerun()

    if check_clicked:
        if not sms.strip():
            st.warning("Please enter a message before analyzing.")
        else:
            try:
                transformed_message = vectorizer.transform([sms])
                prediction = str(model.predict(transformed_message)[0]).lower()

                if prediction in ("spam", "1", "true"):
                    is_spam = True
                elif prediction in ("ham", "not spam", "not_spam", "0", "false"):
                    is_spam = False
                else:
                    st.error("The model returned an unrecognized label.")
                    st.stop()

                confidence = None

                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(transformed_message)[0]
                    confidence = float(max(probabilities)) * 100

                st.session_state.prediction_result = {
                    "is_spam": is_spam,
                    "confidence": confidence
                }

            except Exception:
                st.error("Unable to analyze this message. Please check the model files and try again.")

    result = st.session_state.get("prediction_result")

    if result:
        if result["is_spam"]:
            result_class = "result-spam"
            result_icon = "🚨"
            result_title = "Potential Spam Detected"
            result_description = (
                "This message has been classified as spam. "
                "Be cautious with unknown links, requests for money, "
                "and messages asking for personal information."
            )
            result_color = "#be123c"
        else:
            result_class = "result-safe"
            result_icon = "✅"
            result_title = "Likely a Normal Message"
            result_description = (
                "This message has been classified as legitimate (ham). "
                "However, always verify suspicious requests independently."
            )
            result_color = "#15803d"

        st.markdown(f"""
        <div class="result-card {result_class}">
            <div class="result-icon">{result_icon}</div>
            <div class="result-title" style="color:{result_color}">
                {result_title}
            </div>
            <div class="result-description">
                {result_description}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if result["confidence"] is not None:
            confidence = result["confidence"]

            st.markdown(f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; gap:10px;">
                    <span style="font-weight:700;color:#172033;">
                        Model confidence
                    </span>
                    <span style="font-weight:800;color:#635bff;">
                        {confidence:.1f}%
                    </span>
                </div>
                <div class="confidence-track">
                    <div class="confidence-fill"
                         style="width:{confidence:.1f}%;">
                    </div>
                </div>
                <div class="info-text">
                    Confidence is the model's estimated probability for its
                    predicted class, not a guarantee that the message is safe.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown("## Built for smarter messaging")
st.write("")

info1, info2, info3 = st.columns(3)

features = [
    (
        info1,
        "🧠",
        "Machine Learning",
        "Uses a trained Naive Bayes classifier and TF-IDF text features to analyze message content."
    ),
    (
        info2,
        "⚡",
        "Fast Results",
        "Get an immediate classification after entering your SMS message."
    ),
    (
        info3,
        "📱",
        "Responsive Design",
        "The layout adapts to different screen widths for phones, tablets, and desktops."
    )
]

for col, icon, title, description in features:
    with col:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-icon">{icon}</div>
            <div class="info-title">{title}</div>
            <div class="info-text">{description}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="info-card">
    <div class="info-title">🔐 Privacy & safety</div>
    <div class="info-text">
        Messages are processed to generate a prediction. This app does not
        intentionally save submitted messages to a database. Avoid entering
        passwords, OTPs, bank details, or other sensitive information.
        A message classified as normal can still be fraudulent.
    </div>
</div>

<div class="footer">
    <b>SMS Shield</b> · Machine Learning Project<br>
    Built with Python, Streamlit, TF-IDF and Naive Bayes<br>
    Made for safer messaging 💜
</div>
""", unsafe_allow_html=True)
