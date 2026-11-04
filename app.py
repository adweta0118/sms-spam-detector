import streamlit as st
import joblib
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
