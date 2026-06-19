import streamlit as st

from auth_utils import authenticate_user, register_user

AUTH_CSS = """
<style>
.login-title {
    text-align: center;
    color: #1f4e79;
    font-size: 1.8rem;
    margin-bottom: 0.25rem;
}
.login-subtitle {
    text-align: center;
    color: #7f8c8d;
    margin-bottom: 1.5rem;
}
</style>
"""


def show_login_page():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            '<p class="login-title">🏠 House Price Analysis</p>',
            unsafe_allow_html=True,
        )

        login_tab, signup_tab = st.tabs(["Login", "Create Account"])

        with login_tab:
            _show_login_form()

        with signup_tab:
            _show_signup_form()


def _show_login_form():
    st.markdown(
        '<p class="login-subtitle">Sign in with your email and password</p>',
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Your password")
        remember = st.checkbox("Remember me")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    if submitted:
        success, result = authenticate_user(email, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_email = result["email"]
            st.session_state.user_name = result["name"]
            if remember:
                st.session_state.remember_email = result["email"]
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error(result)


def _show_signup_form():
    st.markdown(
        '<p class="login-subtitle">Create your account with email and password</p>',
        unsafe_allow_html=True,
    )

    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input("Full Name", placeholder="Your name")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters")
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
        )
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
            return

        success, message = register_user(name, email, password)
        if success:
            st.success(message)
            st.info("Switch to the Login tab to sign in.")
        else:
            st.error(message)


def show_logout_button():
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.pop("user_email", None)
        st.session_state.pop("user_name", None)
        st.rerun()
