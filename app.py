import streamlit as st
from auth import login_section
from player import show_player

# Page Theme & Configuration
st.set_page_config(page_title=" Music", page_icon="🍎", layout="wide")
st.markdown("<style>.stApp { background: radial-gradient(circle at top right, #321d2a, #121212); color: white; }</style>", unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'is_playing' not in st.session_state: st.session_state.is_playing = False

# Navigation Logic
if not st.session_state.logged_in:
    login_section()
else:
    show_player()