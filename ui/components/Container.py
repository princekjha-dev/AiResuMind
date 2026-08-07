import streamlit as st

def container_start():
    """Start centered max-width content container"""
    st.markdown('<div class="app-container">', unsafe_allow_html=True)

def container_end():
    """End centered max-width content container"""
    st.markdown('</div>', unsafe_allow_html=True)
