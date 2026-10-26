
import streamlit as st
import joblib

st.set_page_config(
    page_title="SMS Shield | Spam Detector",
    page_icon="📩",
    layout="centered"
)

@st.cache_resource
def load_model():
    model = joblib.load("sms_spam_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
}
.main-title {
    text-align: center;
    color: #4338ca;
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #475569;
    font-size: 17px;
}
.result-box {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">📩 SMS Shield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered SMS Spam Detection</div>',
    unsafe_allow_html=True
)

st.write("")
st.write(
    "Protect yourself from suspicious messages using "
    "a Machine Learning classification model."
)

st.divider()

st.subheader("🔍 Check Your SMS")

message = st.text_area(
    "Enter your message",
    placeholder="Example: Congratulations! You have won a free prize!",
    height=140
)

if st.button("Check Message", use_container_width=True):

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        features = vectorizer.transform([message])
        prediction = model.predict(features)[0]

        probabilities = model.predict_proba(features)[0]
        classes = model.classes_

        confidence = max(probabilities) * 100

        st.divider()

        if prediction == "spam":
            st.error("🚨 SPAM MESSAGE DETECTED")

            st.write(
                "The model classifies this message as likely spam. "
                "Avoid suspicious links and requests for personal information."
            )

        else:
            st.success("✅ NOT SPAM — CLASSIFIED AS HAM")

            st.write(
                "The model classifies this message as likely legitimate. "
                "This does not guarantee that the message is safe."
            )

        st.metric(
            label="Model Confidence Score",
            value=f"{confidence:.2f}%"
        )

        st.caption(
            "Confidence is the model's estimated probability, "
            "not a guarantee that the prediction is correct."
        )

st.divider()

st.subheader("🧪 Try Sample Messages")

col1, col2 = st.columns(2)

with col1:
    st.write("**Sample spam**")
    st.code("Congratulations! You won a free prize!")

with col2:
    st.write("**Sample ham**")
    st.code("Hey, see you at college tomorrow.")

st.divider()

st.subheader("📊 About This Project")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Algorithm**")
    st.write("Multinomial Naive Bayes")

    st.markdown("**Feature Extraction**")
    st.write("TF-IDF")

with col2:
    st.markdown("**Dataset**")
    st.write("UCI SMS Spam Collection")

    st.markdown("**ML Task**")
    st.write("Binary Classification")

st.info(
    "Academic project developed using Python and Machine Learning. "
    "Always verify suspicious messages independently."
)

st.caption("SMS Shield | IML Mini Project | B.Tech")
