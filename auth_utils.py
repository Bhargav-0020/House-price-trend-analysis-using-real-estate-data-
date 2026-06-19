import hashlib
import json
import re
import secrets
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

USERS_FILE = Path("data/users.json")
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def _ensure_data_dir():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")


def load_users():
    _ensure_data_dir()
    with USERS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    _ensure_data_dir()
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(email.strip().lower()))


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return salt, password_hash


def verify_password(password, salt, stored_hash):
    _, password_hash = hash_password(password, salt)
    return password_hash == stored_hash


def register_user(name, email, password):
    email = email.strip().lower()
    name = name.strip()

    if not name:
        return False, "Please enter your name."
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = load_users()
    if email in users:
        return False, "An account with this email already exists. Please log in."

    salt, password_hash = hash_password(password)
    users[email] = {
        "name": name,
        "email": email,
        "salt": salt,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_users(users)

    email_sent = send_welcome_email(name, email)
    if email_sent:
        return True, "Account created! A welcome email has been sent to your inbox."
    return True, "Account created! You can now log in with your email and password."


def authenticate_user(email, password):
    email = email.strip().lower()

    if not is_valid_email(email):
        return False, "Please enter a valid email address."

    users = load_users()
    user = users.get(email)
    if not user:
        return False, "No account found with this email. Please create an account first."

    if not verify_password(password, user["salt"], user["password_hash"]):
        return False, "Incorrect password. Please try again."

    return True, user


def send_welcome_email(name, email):
    try:
        import streamlit as st

        smtp_config = st.secrets.get("smtp", {})
    except Exception:
        return False

    host = smtp_config.get("host")
    port = smtp_config.get("port", 587)
    username = smtp_config.get("username")
    password = smtp_config.get("password")
    from_email = smtp_config.get("from_email", username)

    if not all([host, username, password, from_email]):
        return False

    subject = "Welcome to House Price Trend Analysis"
    body = f"""Hello {name},

Your account has been created successfully.

You can now log in to the House Price Trend Analysis dashboard using:
Email: {email}

Thank you for joining us!

— House Price Analysis Team
"""

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(host, int(port)) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(from_email, email, message.as_string())
        return True
    except Exception:
        return False
