import streamlit as st

from train_models import build_models


@st.cache_resource(show_spinner="Loading ML models...")
def get_ml_assets():
    """Train models at runtime so they always match the deployed sklearn version."""
    return build_models()
