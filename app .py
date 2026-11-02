import streamlit as st
import pickle
import os
import re

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SMS Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f3ff 0%, #eff6ff 100%);
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #5b45d6;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .info-card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .result-safe {
        background: #dcfce7;
        color: #166534;
        padding: 22px;
        border-radius: 15px;
        border-left: 6px solid #16a34a;
        margin-top: 20px;
    }

    .result-spam {
        background: #fee2e2;
        color: #991b1b;
        padding: 22px;
        border-radius: 15px;
        border-left: 6px solid #dc2626;
        margin-top: 20px;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "sms_input" not in st.session_state:
    st.session_state.sms_input = ""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "total_analyzed" not in st.session_state:
    st.session_state.total_analyzed = 0

if "spam_detected" not in st.session_state:
    st.session_state.spam_detected = 0


# --------------------------------------------------
# CALLBACKS
# IMPORTANT: WIDGET STATE IS RESET IN A CALLBACK
# --------------------------------------------------

def clear_sms_input():
    st.session_state.sms_input = ""
    st.session_state.last_prediction = None


def load_prize_message():
    st.session_state.sms_input = (
        "Congratulations! You have won a free prize. "
        "Click this link to claim your reward now!"
    )
    st.session_state.last_prediction = None


def load_bank_message():
    st.session_state.sms_input = (
        "Your bank account has been credited. "
        "Please check your account statement."
    )
    st.session_state.last_prediction = None


def load_normal_message():
    st.session_state.sms_input = (
        "Hi, are we meeting today? "
        "Please let me know when you are free."
    )
    st.session_state.last_prediction = None


def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.sms_input = ""
    st.session_state.last_prediction = None


# --------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

@st.cache_resource
def load_model_files():
    model_path = "sms_spam_model.pkl"
    vectorizer_path = "tfidf_vectorizer.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(
            f"Vectorizer file not found: {vectorizer_path}"
        )

    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    with open(vectorizer_path, "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    return model, vectorizer


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_sms(message, model, vectorizer):
    message_vector = vectorizer.transform([message])

    prediction = model.predict(message_vector)[0]

    # Support common spam/ham labels and numeric labels.
    normalized_prediction = str(prediction).strip().lower()

    if normalized_prediction in ["spam", "1", "true"]:
        is_spam = True
    elif normalized_prediction in ["ham", "not spam", "0", "false"]:
        is_spam = False
    else:
        raise ValueError(
            f"Unexpected model prediction: {prediction}"
        )

    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(message_vector)[0]
        confidence = float(max(probabilities)) * 100

    return is_spam, confidence


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🛡️ SMS Shield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent SMS spam detection assistant'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# DEMO SIGN-IN
# --------------------------------------------------

if not st.session_state.logged_in:

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    st.subheader("🔐 Welcome to SMS Shield")
    st.write(
        "Sign in to access the SMS spam detection dashboard."
    )

    with st.form("signin_form"):

        email = st.text_input(
            "Email address",
            placeholder="you@example.com"
        )

        phone = st.text_input(
            "Phone number",
            placeholder="Enter your phone number"
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )

        if submitted:

            if not email.strip():
                st.error("Please enter your email address.")

            elif not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                email.strip()
            ):
                st.error("Please enter a valid email address.")

            elif not re.fullmatch(
                r"[0-9+\-\s()]{7,20}",
                phone.strip()
            ):
                st.error("Please enter a valid phone number.")

            else:
                st.session_state.logged_in = True
                st.session_state.user_email = email.strip()
                st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.info(
        "Demo sign-in only: this form does not send an actual "
        "OTP or verify your identity."
    )

    st.caption(
        "SMS Shield uses machine learning to classify messages. "
        "Predictions may not always be correct."
    )

    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🛡️ SMS Shield")

    st.write("Your SMS safety dashboard")

    st.divider()

    st.write("👤 **Signed in as**")
    st.write(st.session_state.user_email)

    st.divider()

    st.metric(
        "Messages Analyzed",
        st.session_state.total_analyzed
    )

    st.metric(
        "Spam Messages Detected",
        st.session_state.spam_detected
    )

    st.divider()

    st.button(
        "🚪 Sign Out",
        on_click=logout,
        use_container_width=True
    )

    st.caption("SMS Shield | Machine Learning Project")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.subheader("📩 Analyze an SMS Message")

st.write(
    "Paste an SMS below, or select a sample message to try "
    "the spam detection model."
)


# --------------------------------------------------
# SAMPLE MESSAGE BUTTONS
# --------------------------------------------------

sample1, sample2, sample3 = st.columns(3)

with sample1:
    st.button(
        "🎁 Prize Message",
        on_click=load_prize_message,
        use_container_width=True
    )

with sample2:
    st.button(
        "🏦 Bank Alert",
        on_click=load_bank_message,
        use_container_width=True
    )

with sample3:
    st.button(
        "👋 Normal Message",
        on_click=load_normal_message,
        use_container_width=True
    )


# --------------------------------------------------
# SMS INPUT
# --------------------------------------------------

sms_text = st.text_area(
    "SMS message",
    key="sms_input",
    height=160,
    placeholder="Type or paste your SMS message here..."
)


# --------------------------------------------------
# CHARACTER AND WORD COUNTERS
# --------------------------------------------------

character_count = len(sms_text)
word_count = len(sms_text.split())

counter1, counter2 = st.columns(2)

with counter1:
    st.metric(
        "Characters",
        character_count
    )

with counter2:
    st.metric(
        "Words",
        word_count
    )


# --------------------------------------------------
# ANALYZE AND CLEAR BUTTONS
# --------------------------------------------------

analyze_col, clear_col = st.columns([2, 1])

with analyze_col:

    analyze_clicked = st.button(
        "🔍 Analyze Message",
        type="primary",
        use_container_width=True
    )

with clear_col:

    st.button(
        "Clear",
        on_click=clear_sms_input,
        use_container_width=True
    )


# --------------------------------------------------
# RUN PREDICTION
# --------------------------------------------------

if analyze_clicked:

    if not sms_text.strip():

        st.warning(
            "Please enter a message containing text before "
            "analyzing it."
        )

    else:

        try:
            with st.spinner("Analyzing your message..."):

                model, vectorizer = load_model_files()

                is_spam, confidence = predict_sms(
                    sms_text,
                    model,
                    vectorizer
                )

            st.session_state.total_analyzed += 1

            if is_spam:
                st.session_state.spam_detected += 1

            st.session_state.last_prediction = {
                "message": sms_text,
                "is_spam": is_spam,
                "confidence": confidence
            }

        except FileNotFoundError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                "Unable to analyze this message. "
                "Please check your model files and try again."
            )

            st.caption(f"Technical details: {error}")


# --------------------------------------------------
# DISPLAY PREDICTION RESULT
# --------------------------------------------------

result = st.session_state.last_prediction

if result is not None:

    st.divider()

    st.subheader("📊 Analysis Result")

    if result["is_spam"]:

        st.markdown(
            """
            <div class="result-spam">
                <h3>🚨 Spam Message Detected</h3>
                <p>
                    This message has been classified as spam.
                    Be cautious with suspicious links, prize claims,
                    and requests for personal information.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="result-safe">
                <h3>✅ Likely a Normal Message</h3>
                <p>
                    The model has classified this message as
                    non-spam. Still, be careful with unexpected
                    links and requests for sensitive information.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if result["confidence"] is not None:

        st.write(
            f"**Model confidence:** "
            f"{result['confidence']:.2f}%"
        )

        st.progress(
            min(
                max(result["confidence"] / 100, 0.0),
                1.0
            )
        )

        st.caption(
            "Confidence is the model's estimated probability "
            "for its predicted class; it is not a guarantee "
            "that the prediction is correct."
        )

    with st.expander("View analyzed message"):

        st.write(result["message"])


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:15px;">
        <b>🛡️ SMS Shield</b><br>
        Machine Learning-Based SMS Spam Detection<br>
        Built with Python, Scikit-learn and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
