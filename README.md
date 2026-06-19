# House-price-trend-analysis-using-real-estate-data-

## Authentication

Users can create their own account with **email and password**, then log in to access the dashboard.

### Create an account
1. Open the app and go to the **Create Account** tab
2. Enter your name, email, and password
3. Click **Create Account**

### Log in
1. Go to the **Login** tab
2. Enter your registered email and password
3. Click **Sign In**

### Welcome emails (optional)

To send a welcome email when someone signs up, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your SMTP details (e.g. Gmail app password).

## ML Algorithms

The app uses four algorithms for price prediction:
- Linear Regression
- Random Forest
- Gradient Boosting
- Decision Tree

## Run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```
