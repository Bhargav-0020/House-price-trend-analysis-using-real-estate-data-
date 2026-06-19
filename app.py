import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu

from login_page import show_login_page, show_logout_button
from model_loader import get_ml_assets
from train_models import MODEL_LABELS

st.set_page_config(
    page_title="House Price Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #1f4e79;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}

.card h3 {
    margin-bottom: 5px;
    color: #2E86C1;
}

.card p {
    font-size: 22px;
    font-weight: bold;
}

.success-box {
    background-color: #e8f8f5;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #1abc9c;
    font-size: 22px;
    font-weight: bold;
}

.algo-card {
    background-color: white;
    padding: 14px 18px;
    border-radius: 10px;
    border-left: 4px solid #2E86C1;
    margin-bottom: 8px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

models, scaler, model_metrics = get_ml_assets()
df = pd.read_csv("dataset/housing.csv")

with st.sidebar:
    st.write(f"Welcome, **{st.session_state.get('user_name', 'User')}**")
    st.caption(st.session_state.get("user_email", ""))
    show_logout_button()

selected = option_menu(
    menu_title=None,
    options=["Home", "Data Analysis", "Trend Analysis", "Price Prediction"],
    icons=["house", "bar-chart", "graph-up", "currency-rupee"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.markdown(
        "<h1 style='text-align:center;'>🏠 House Price Trends Analysis Using Real Estate Data</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style='text-align:center; color:gray;'>Data-Driven Property Insights & Price Prediction System</h4>",
        unsafe_allow_html=True,
    )
    st.write("")

    st.subheader("📌 Project Overview")
    st.write("""
    This dashboard provides comprehensive analysis of real estate data and predicts
    property prices using **four Machine Learning algorithms**.

    It helps users understand:
    • Market price trends
    • Feature influence on house prices
    • Location-based pricing differences
    • Real-time property valuation
    """)

    st.write("")
    st.subheader("⚙️ How It Works")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Step 1 — Data Analysis**
        - Explore dataset statistics
        - Visualize correlations
        - Identify key price drivers
        """)
    with col2:
        st.markdown("""
        **Step 2 — Machine Learning**
        - Linear Regression, Random Forest, Gradient Boosting & Decision Tree
        - Feature scaling applied
        - Models trained & evaluated
        - Real-time multi-model price prediction
        """)

    st.write("")
    st.subheader("🤖 ML Algorithms")
    for key, label in MODEL_LABELS.items():
        scores = model_metrics.get(key, {})
        r2 = scores.get("r2", "—")
        mae = scores.get("mae", "—")
        if isinstance(mae, (int, float)):
            st.markdown(
                f'<div class="algo-card"><b>{label}</b> &nbsp;|&nbsp; R²: {r2} &nbsp;|&nbsp; MAE: ₹{mae:,.0f}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f'<div class="algo-card"><b>{label}</b></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("🛠 Technologies Used")
    st.markdown("""
    - Python
    - Pandas & NumPy
    - Matplotlib & Seaborn
    - Plotly
    - Scikit-learn
    - Streamlit
    """)

    st.write("")
    st.info("Use the navigation menu above to explore Data Analysis, Trends, and Price Prediction.")

    col1, col2, col3 = st.columns(3)
    avg_price = int(df["price"].mean())
    max_price = int(df["price"].max())
    total_houses = len(df)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>Average Price</h3>
            <p>₹ {avg_price:,}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>Highest Price</h3>
            <p>₹ {max_price:,}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card">
            <h3>Total Properties</h3>
            <p>{total_houses}</p>
        </div>
        """, unsafe_allow_html=True)

elif selected == "Data Analysis":
    st.title("📊 Data Analysis & Feature Relationships")

    st.subheader("Dataset Preview (First 5 Records)")
    st.dataframe(df.head())

    st.subheader("Statistical Summary")
    st.write(
        "This table shows mean, minimum, maximum and spread of numerical features in the housing dataset."
    )
    st.dataframe(df.describe())

    st.subheader("Feature Correlation Heatmap")
    st.write(
        "The heatmap shows how strongly each feature affects house price. "
        "Darker color means stronger relationship with price."
    )

    numeric_df = df.select_dtypes(include=["int64", "float64"])
    left, center, right = st.columns([1, 2, 1])
    with center:
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="coolwarm",
            linewidths=0.5,
            fmt=".2f",
            annot_kws={"size": 8},
            ax=ax,
        )
        ax.set_title("Correlation Matrix", fontsize=12)
        st.pyplot(fig)
        plt.close()

elif selected == "Trend Analysis":
    st.title("📈 Real Estate Market Trend Analysis")
    st.write("This section visualizes how different features influence house prices.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Area vs Price Relationship")
        st.caption("Larger houses generally have higher prices.")
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        sns.scatterplot(x="area", y="price", data=df, ax=ax1, color="#2E86C1")
        ax1.set_xlabel("Area (sqft)")
        ax1.set_ylabel("Price")
        st.pyplot(fig1)
        plt.close()

    with col2:
        st.subheader("Price Distribution")
        st.caption("Shows how property prices are distributed in the dataset.")
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        sns.histplot(df["price"], kde=True, ax=ax2, color="#1ABC9C")
        ax2.set_xlabel("House Price")
        st.pyplot(fig2)
        plt.close()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Bedrooms vs Price")
        st.caption("Houses with more bedrooms tend to cost more.")
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        sns.boxplot(x="bedrooms", y="price", data=df, ax=ax3)
        ax3.set_xlabel("Number of Bedrooms")
        ax3.set_ylabel("Price")
        st.pyplot(fig3)
        plt.close()

    with col4:
        st.subheader("Location vs Price")
        st.caption("Urban properties are generally more expensive.")
        fig4 = px.box(
            df,
            x="location",
            y="price",
            color="location",
            title="Property Price by Location",
        )
        fig4.update_layout(template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Year-wise Property Price Growth")
    st.caption("Shows how average property price changes over time.")

    if "year" in df.columns:
        yearly_price = df.groupby("year")["price"].mean().reset_index()
        fig5 = px.line(
            yearly_price,
            x="year",
            y="price",
            markers=True,
            title="Average Property Price Growth Over Years",
        )
        fig5.update_layout(
            template="plotly_white",
            xaxis_title="Year",
            yaxis_title="Average Price",
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("Year column not found in dataset. Year-wise trend cannot be displayed.")

elif selected == "Price Prediction":
    st.title("🏠 House Price Prediction")
    st.write("Enter property details and select algorithms to estimate the house price.")

    col_form, col_result = st.columns([1, 1])

    with col_form:
        area = st.number_input("Area (in square feet)", min_value=300, max_value=20000, value=1000)
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=2)
        stories = st.number_input("Stories", min_value=1, max_value=4, value=2)
        parking = st.number_input("Parking Spaces", min_value=0, max_value=5, value=1)

        mainroad = st.selectbox("Main Road Access", ["yes", "no"])
        guestroom = st.selectbox("Guest Room", ["yes", "no"])
        basement = st.selectbox("Basement", ["yes", "no"])
        hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
        airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
        location = st.selectbox("Location", ["Rural", "Semi-Urban", "Urban"])

        selected_models = st.multiselect(
            "Select Algorithms",
            options=list(MODEL_LABELS.keys()),
            default=list(MODEL_LABELS.keys()),
            format_func=lambda k: MODEL_LABELS[k],
        )

        predict_clicked = st.button("Predict Price", use_container_width=True)

    with col_result:
        yn = {"yes": 1, "no": 0}
        loc = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}

        input_df = pd.DataFrame([{
            "area": area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "stories": stories,
            "parking": parking,
            "mainroad": yn[mainroad],
            "guestroom": yn[guestroom],
            "basement": yn[basement],
            "hotwaterheating": yn[hotwaterheating],
            "airconditioning": yn[airconditioning],
            "location": loc[location],
        }])

        input_scaled = scaler.transform(input_df)

        if predict_clicked:
            if not selected_models:
                st.error("Please select at least one algorithm.")
            else:
                predictions = []
                for model_key in selected_models:
                    price = int(models[model_key].predict(input_scaled)[0])
                    predictions.append(price)
                    st.success(f"**{MODEL_LABELS[model_key]}**: ₹ {price:,}")

                if predictions:
                    avg_pred = int(sum(predictions) / len(predictions))
                    st.info(f"**Average Prediction**: ₹ {avg_pred:,}")

                    if avg_pred < 5000000:
                        st.info("Category: Budget House 🟢")
                    elif avg_pred < 9000000:
                        st.info("Category: Mid-Range House 🟡")
                    else:
                        st.info("Category: Premium House 🔴")
        else:
            st.write("Fill in the details and click **Predict Price** to see results.")
