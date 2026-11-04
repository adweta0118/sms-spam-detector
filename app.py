
import streamlit as st
import joblib
import os

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
# SESSION STATE INITIALIZATION
# --------------------------------------------------

defaults = {
    "sms_input": "",
    "logged_in": False,
    "user_email": "",
    "prediction": None,
    "confidence": None,
    "analyzed_text": "",
    "validation_error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    model_path = "sms_spam_model.pkl"
    vectorizer_path = "tfidf_vectorizer.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "sms_spam_model.pkl is missing from the repository."
        )

    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(
            "tfidf_vectorizer.pkl is missing from the repository."
        )

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer


# --------------------------------------------------
# CALLBACK FUNCTIONS
# --------------------------------------------------

def clear_sms():
    st.session_state.sms_input = ""
    st.session_state.prediction = None
    st.session_state.confidence = None
    st.session_state.analyzed_text = ""
    st.session_state.validation_error = ""


def clear_previous_result():
    st.session_state.prediction = None
    st.session_state.confidence = None
    st.session_state.analyzed_text = ""
    st.session_state.validation_error = ""


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f5f3ff 0%,
        #eff6ff 100%
    );
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
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🛡️ SMS Shield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your Smart AI-Powered SMS Spam Detection System'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOGIN SECTION
# --------------------------------------------------

if not st.session_state.logged_in:

    st.markdown("---")

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("### Welcome to SMS Shield")
        st.write(
            "Sign in to check whether your SMS messages "
            "are safe or potentially spam."
        )

        email = st.text_input(
            "Enter your email address",
            placeholder="example@gmail.com"
        )

        if st.button(
            "Continue to SMS Shield",
            use_container_width=True
        ):

            if not email.strip():
                st.warning("Please enter your email address.")

            elif "@" not in email or "." not in email:
                st.warning("Please enter a valid email address.")

            else:
                st.session_state.user_email = email.strip()
                st.session_state.logged_in = True
                st.rerun()

        st.caption(
            "Demo sign-in only. This does not verify your email."
        )

    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🛡️ SMS Shield")

    st.write("Welcome!")
    st.write(st.session_state.user_email)

    st.markdown("---")

    st.markdown("### Navigation")
    st.write("📩 SMS Spam Detection")
    st.write("📊 Dashboard")

    st.markdown("---")

    if st.button("Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        clear_sms()
        st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.markdown("## 📊 SMS Detection Dashboard")

st.write(
    "Enter any SMS message below and let our machine learning "
    "model determine whether it is Spam or Safe."
)

st.markdown("---")


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

try:
    model, vectorizer = load_model()

except Exception as e:
    st.error("Unable to load the machine learning model.")
    st.code(str(e))
    st.info(
        "Check that both model files are present in the "
        "main GitHub repository folder."
    )
    st.stop()


# --------------------------------------------------
# SMS INPUT SECTION
# --------------------------------------------------

st.markdown("### 📩 Enter Your SMS Message")

sms_text = st.text_area(
    "SMS Message",
    key="sms_input",
    height=150,
    placeholder="Type or paste your SMS message here...",
    on_change=clear_previous_result,
    label_visibility="collapsed"
)


# --------------------------------------------------
# CHARACTER AND WORD COUNTERS
# --------------------------------------------------

character_count = len(sms_text)
word_count = len(sms_text.split())

col1, col2 = st.columns(2)

with col1:
    st.metric("Characters", character_count)

with col2:
    st.metric("Words", word_count)


# --------------------------------------------------
# ANALYZE AND CLEAR BUTTONS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    analyze_clicked = st.button(
        "🔍 Analyze SMS",
        use_container_width=True,
        type="primary"
    )

with col2:

    st.button(
        "🗑️ Clear",
        use_container_width=True,
        on_click=clear_sms
    )


# --------------------------------------------------
# SMS ANALYSIS
# --------------------------------------------------

if analyze_clicked:

    message = sms_text.strip()

    if not message:

        st.session_state.prediction = None
        st.session_state.confidence = None
        st.session_state.analyzed_text = ""

        st.session_state.validation_error = (
            "Please enter a valid SMS message. "
            "Spaces alone cannot be analyzed."
        )

    else:

        try:

            transformed_message = vectorizer.transform(
                [message]
            )

            prediction = model.predict(
                transformed_message
            )[0]

            confidence = None

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(
                    transformed_message
                )[0]

                confidence = float(max(probabilities)) * 100

            prediction_text = str(prediction).strip().lower()

            if prediction_text in ["spam", "1", "true"]:

                result = "Spam"

            elif prediction_text in ["ham", "0", "false"]:

                result = "Safe"

            else:

                result = str(prediction)

            st.session_state.prediction = result
            st.session_state.confidence = confidence
            st.session_state.analyzed_text = message
            st.session_state.validation_error = ""

        except Exception as e:

            st.session_state.prediction = None
            st.session_state.confidence = None

            st.error("An error occurred during SMS analysis.")
            st.code(str(e))


# --------------------------------------------------
# VALIDATION MESSAGE
# --------------------------------------------------

if st.session_state.validation_error:

    st.warning(st.session_state.validation_error)


# --------------------------------------------------
# PREDICTION RESULT
# --------------------------------------------------

if st.session_state.prediction is not None:

    st.markdown("---")

    st.markdown("### 📋 Analysis Result")

    if st.session_state.prediction == "Safe":

        st.markdown(
            """
            <div class="result-safe">
                <h2>✅ Safe Message</h2>
                <p>This SMS appears to be a legitimate message.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.prediction == "Spam":

        st.markdown(
            """
            <div class="result-spam">
                <h2>🚨 Spam Message Detected!</h2>
                <p>This SMS may contain unwanted or suspicious content.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Model prediction: "
            + str(st.session_state.prediction)
        )

    if st.session_state.confidence is not None:

        st.metric(
            "Model Confidence",
            f"{st.session_state.confidence:.2f}%"
        )

    st.caption(
        "Analyzed message: "
        + st.session_state.analyzed_text
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">
        <p>🛡️ SMS Shield | AI-Powered Spam Detection</p>
        <p>Developed using Python, Streamlit and Machine Learning</p>
    </div>
    """,
    unsafe_allow_html=True
)
