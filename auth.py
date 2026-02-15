import streamlit as st

# Your requested credentials
USERS = {"user1": "pass1", "user2": "pass2", "user3": "pass3"}
ADMINS = {"admin1": "admin_pass1"}

def login_section():
    st.markdown("""
        <style>
        .login-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            max-width: 400px;
            margin: 80px auto;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#fa243c;'> Music Login</h1>", unsafe_allow_html=True)
    
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        if user in ADMINS and ADMINS[user] == pw:
            st.session_state.logged_in, st.session_state.role = True, "admin"
            st.rerun()
        elif user in USERS and USERS[user] == pw:
            st.session_state.logged_in, st.session_state.role = True, "user"
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown('</div>', unsafe_allow_html=True)