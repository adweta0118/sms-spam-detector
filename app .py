
import streamlit as st
import joblib
import re
import secrets
import time

st.set_page_config(
    page_title="SMS Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------

defaults = {
    "page": "auth",
    "auth_mode": "Sign In",
    "users": {},
    "pending_user": None,
    "demo_otp": None,
    "otp_expiry": 0,
    "user": None,
    "sms_input": "",
    "prediction": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- MODEL LOADING ----------------

@st.cache_resource
def load_models():
    model = joblib.load("sms_spam_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer


try:
    model, vectorizer = load_models()
except Exception:
    st.error(
        "Model files could not be loaded. "
        "Check that sms_spam_model.pkl and "
        "tfidf_vectorizer.pkl exist in your repository."
    )
    st.stop()


# ---------------- RESPONSIVE DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #ede9fe 0%, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #dbeafe 0%, transparent 35%),
        #f8fafc;
}

.block-container {
    max-width: 1050px;
    padding: 1.5rem 1.5rem 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 30px;
}

.brand-icon {
    background: linear-gradient(135deg, #635bff, #a855f7);
    color: white;
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    box-shadow: 0 8px 20px #635bff30;
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #172033;
}

.brand-sub {
    font-size: 12px;
    color: #64748b;
}

.auth-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 20px 60px #1720330d;
}

.auth-heading {
    color: #172033;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 8px;
}

.auth-subtitle {
    color: #64748b;
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 22px;
}

.hero-panel {
    background: linear-gradient(145deg, #5145ed, #8b5cf6 60%, #a855f7);
    border-radius: 24px;
    padding: 38px 30px;
    color: white;
    min-height: 460px;
}

.hero-panel h1 {
    font-size: clamp(32px, 4vw, 47px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -1.5px;
    color: white;
}

.hero-panel p {
    color: #f0edff;
    font-size: 14px;
    line-height: 1.9;
}

.hero-badge {
    background: #ffffff20;
    border: 1px solid #ffffff35;
    padding: 8px 12px;
    border-radius: 25px;
    display: inline-block;
    font-size: 12px;
    margin-bottom: 24px;
}

.hero-feature {
    margin-top: 25px;
    padding: 13px;
    border-radius: 12px;
    background: #ffffff15;
    font-size: 13px;
    margin-bottom: 10px;
}

.stButton > button {
    min-height: 44px;
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid #e2e8f0;
    transition: 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #635bff, #8055f6);
    color: white;
    border: none;
}

.stButton > button:hover {
    border-color: #635bff;
    transform: translateY(-1px);
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 11px;
    border-color: #dbe2ef;
    background: #fbfcff;
}

div[data-testid="stTextArea"] textarea {
    min-height: 140px;
}

.section-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 12px 35px #17203308;
}

.result-card {
    padding: 22px;
    border-radius: 16px;
    margin-top: 15px;
    border: 1px solid;
}

.spam {
    background: #fff1f2;
    border-color: #fecdd3;
}

.safe {
    background: #f0fdf4;
    border-color: #bbf7d0;
}

.result-title {
    font-size: 23px;
    font-weight: 800;
    margin: 8px 0;
}

.muted {
    color: #64748b;
    font-size: 13px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 25px 0;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .auth-card {
        padding: 20px 16px;
    }

    .auth-heading {
        font-size: 28px;
    }

    .hero-panel {
        min-height: auto;
        padding: 25px 20px;
        margin-bottom: 20px;
    }

    .brand-name {
        font-size: 20px;
    }

    .stButton > button {
        width: 100%;
    }
}

@media (max-width: 420px) {
    .auth-card {
        padding: 17px 12px;
        border-radius: 17px;
    }

    .hero-panel {
        border-radius: 17px;
        padding: 22px 16px;
    }

    .hero-panel h1 {
        font-size: 31px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- BRAND ----------------

st.markdown("""
<div class="brand">
    <div class="brand-icon">🛡️</div>
    <div>
        <div class="brand-name">SMS Shield</div>
        <div class="brand-sub">Smart Message Protection</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- DEMO OTP HELPERS ----------------

def generate_demo_otp():
    st.session_state.demo_otp = f"{secrets.randbelow(1000000):06d}"
    st.session_state.otp_expiry = time.time() + 300


def start_demo_verification(user_data):
    st.session_state.pending_user = user_data
    generate_demo_otp()
    st.session_state.page = "verify"
    st.rerun()


def return_to_auth():
    st.session_state.page = "auth"
    st.session_state.pending_user = None
    st.session_state.demo_otp = None
    st.session_state.auth_mode = "Sign In"
    st.rerun()


# ---------------- AUTHENTICATION PAGE ----------------

if st.session_state.page == "auth":

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown("""
        <div class="hero-panel">
            <div class="hero-badge">✦ AI-Powered Security</div>
            <h1>Your messages.<br>Your safety.<br>Your peace of mind.</h1>
            <p>
                Identify suspicious SMS messages with machine learning.
                Check messages before you trust unfamiliar links,
                offers, and requests.
            </p>
            <div class="hero-feature">🛡️ &nbsp; Intelligent spam detection</div>
            <div class="hero-feature">⚡ &nbsp; Instant message analysis</div>
            <div class="hero-feature">📱 &nbsp; Designed for every screen</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="auth-heading">Welcome to SMS Shield</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-subtitle">Sign in or create an account to access your spam detection dashboard.</div>',
            unsafe_allow_html=True
        )

        mode = st.radio(
            "Choose an option",
            ["Sign In", "Create Account"],
            horizontal=True,
            key="auth_mode",
            label_visibility="collapsed"
        )

        if mode == "Create Account":
            st.markdown("#### Create your account")

            full_name = st.text_input(
                "Full name",
                placeholder="Enter your name",
                key="signup_name"
            )

            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="signup_email"
            ).strip().lower()

            phone = st.text_input(
                "Phone number",
                placeholder="Enter your phone number",
                key="signup_phone"
            ).strip()

            if st.button(
                "Create account →",
                type="primary",
                use_container_width=True
            ):
                if not full_name.strip():
                    st.error("Please enter your full name.")
                elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Please enter a valid email address.")
                elif not re.fullmatch(r"\+?[0-9\s()-]{7,20}", phone):
                    st.error("Please enter a valid phone number.")
                elif email in st.session_state.users:
                    st.error("This email already has a demo account. Please sign in.")
                else:
                    user_data = {
                        "name": full_name.strip(),
                        "email": email,
                        "phone": phone
                    }
                    start_demo_verification(user_data)

        else:
            st.markdown("#### Sign in to your account")

            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="signin_email"
            ).strip().lower()

            if st.button(
                "Continue with demo OTP →",
                type="primary",
                use_container_width=True
            ):
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Please enter a valid email address.")
                elif email not in st.session_state.users:
                    st.error("No demo account found. Please create an account first.")
                else:
                    start_demo_verification(
                        st.session_state.users[email]
                    )

            st.markdown(
                '<div class="muted">Demo sign-in uses a simulated OTP. No real email or SMS is sent.</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- OTP VERIFICATION PAGE ----------------

elif st.session_state.page == "verify":

    pending = st.session_state.pending_user

    if not pending:
        return_to_auth()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <div class="hero-panel">
            <div class="hero-badge">🔐 Demo Verification</div>
            <h1>One more step<br>to get started.</h1>
            <p>
                Verify your demo account using the simulated six-digit code.
                In this college-project version, the code appears on this page
                instead of being sent by email or SMS.
            </p>
            <div class="hero-feature">✉️ Email field included</div>
            <div class="hero-feature">📱 Phone field included</div>
            <div class="hero-feature">🧪 Demonstration only</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="auth-heading">Verify your account</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="auth-subtitle">Hello {pending["name"]}! Enter the demo code shown below.</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"DEMO OTP: {st.session_state.demo_otp}\n\n"
            "This code is simulated. No message was sent."
        )

        otp_input = st.text_input(
            "Six-digit verification code",
            max_chars=6,
            placeholder="Enter demo OTP"
        ).strip()

        if st.button(
            "Verify & Continue →",
            type="primary",
            use_container_width=True
        ):
            if time.time() > st.session_state.otp_expiry:
                st.error("This demo code has expired. Generate a new one.")
            elif otp_input != st.session_state.demo_otp:
                st.error("Incorrect code. Please try again.")
            else:
                email = pending["email"]
                st.session_state.users[email] = pending
                st.session_state.user = pending
                st.session_state.page = "dashboard"
                st.session_state.pending_user = None
                st.session_state.demo_otp = None
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Resend demo OTP", use_container_width=True):
                generate_demo_otp()
                st.rerun()

        with col2:
            if st.button("Back to sign in", use_container_width=True):
                return_to_auth()

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- PROTECTED DASHBOARD ----------------

elif st.session_state.page == "dashboard":

    user = st.session_state.user

    if not user:
        st.session_state.page = "auth"
        st.rerun()

    header1, header2 = st.columns([3, 1])

    with header1:
        st.markdown(
            f"## Welcome, {user['name']} 👋"
        )
        st.markdown(
            '<div class="muted">Your personal SMS spam detection dashboard</div>',
            unsafe_allow_html=True
        )

    with header2:
        if st.button("Log out ↗", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "auth"
            st.session_state.prediction = None
            st.session_state.sms_input = ""
            st.rerun()

    st.write("")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown("### 🛡️ Analyze an SMS message")
    st.markdown(
        '<div class="muted">Paste a message below to classify it as Spam or Not Spam.</div>',
        unsafe_allow_html=True
    )

    sample1, sample2, sample3 = st.columns(3)

    with sample1:
        if st.button("🎁 Prize message", use_container_width=True):
            st.session_state.sms_input = (
                "Congratulations! You have won a free prize. "
                "Click here to claim now!"
            )
            st.session_state.prediction = None
            st.rerun()

    with sample2:
        if st.button("🏦 Bank alert", use_container_width=True):
            st.session_state.sms_input = (
                "URGENT! Your bank account will be blocked. "
                "Verify your details immediately."
            )
            st.session_state.prediction = None
            st.rerun()

    with sample3:
        if st.button("👋 Normal message", use_container_width=True):
            st.session_state.sms_input = (
                "Hey, are we still meeting at college tomorrow?"
            )
            st.session_state.prediction = None
            st.rerun()

    sms = st.text_area(
        "SMS message",
        key="sms_input",
        placeholder="Paste your SMS message here...",
        max_chars=5000
    )

    count1, count2 = st.columns(2)

    with count1:
        st.metric("Characters", len(sms))

    with count2:
        st.metric("Words", len(re.findall(r"\b[\w']+\b", sms)))

    analyze_col, clear_col = st.columns([2, 1])

    with analyze_col:
        analyze = st.button(
            "🔍 Analyze Message",
            type="primary",
            use_container_width=True
        )

    with clear_col:
        clear = st.button(
            "Clear",
            use_container_width=True
        )

    if clear:
        st.session_state.sms_input = ""
        st.session_state.prediction = None
        st.rerun()

    if analyze:
        if not sms.strip():
            st.warning("Please enter a message first.")
        else:
            try:
                features = vectorizer.transform([sms])
                prediction = str(model.predict(features)[0]).lower()

                if prediction in ("spam", "1", "true"):
                    is_spam = True
                elif prediction in ("ham", "not spam", "not_spam", "0", "false"):
                    is_spam = False
                else:
                    st.error("The model returned an unrecognized label.")
                    st.stop()

                confidence = None

                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(features)[0]
                    confidence = float(max(probabilities)) * 100

                st.session_state.prediction = {
                    "spam": is_spam,
                    "confidence": confidence
                }

            except Exception:
                st.error("Could not analyze the message. Check your model files.")

    result = st.session_state.prediction

    if result:
        if result["spam"]:
            st.markdown("""
            <div class="result-card spam">
                <div style="font-size:30px">🚨</div>
                <div class="result-title" style="color:#be123c">
                    Potential Spam Detected
                </div>
                <div class="muted">
                    Be careful with suspicious links, requests for money,
                    and messages asking for personal information.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card safe">
                <div style="font-size:30px">✅</div>
                <div class="result-title" style="color:#15803d">
                    Likely a Normal Message
                </div>
                <div class="muted">
                    The model classified this message as legitimate.
                    This does not guarantee that it is safe.
                </div>
            </div>
            """, unsafe_allow_html=True)

        if result["confidence"] is not None:
            st.metric("Model confidence", f"{result['confidence']:.1f}%")
            st.progress(min(result["confidence"] / 100, 1.0))

            st.caption(
                "Confidence is the model's estimated probability for its "
                "predicted class, not a guarantee of safety."
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h3>🔐 Privacy & safety</h3>
        <div class="muted">
            This demo keeps account data in temporary Streamlit session state.
            It does not intentionally save messages to a database.
            Avoid entering passwords, OTPs, bank details, or sensitive information.
            A message classified as normal can still be fraudulent.
        </div>
    </div>
    <div class="footer">
        <b>SMS Shield</b> · Machine Learning College Project<br>
        Python · Streamlit · TF-IDF · Naive Bayes
    </div>
    """, unsafe_allow_html=True)

