import streamlit as st

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def sidebar_navigation():
    st.sidebar.title("Student menu")
    selection = st.sidebar.radio("Go to", [
        "Province Summary", 
        "Faculty Summary", 
        "Top Provinces and Faculties", 
        "Province and Faculty Distribution", 
        "Province, Faculty, and School Distribution"
    ])
    return selection
