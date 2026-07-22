import streamlit as st
import joblib
import numpy as np
import pandas as pd


# ============================
# PAGE CONFIG
# ============================

st.set_page_config(
    page_title="NexusCart AI",
    page_icon="🚀",
    layout="wide"
)


# ============================
# LOGIN SYSTEM
# ============================

def login():

    st.title("🔐 NexusCart AI Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        if username == "admin" and password == "nexus123":

            st.session_state.logged_in = True

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if not st.session_state.logged_in:

    login()

    st.stop()



# ============================
# LOAD MODEL
# ============================

model = joblib.load(
    "sales_prediction_model.pkl"
)



# ============================
# LOAD CSV DATA
# ============================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "retail_sales.csv"
    )

    return df


df = load_data()



# ============================
# HEADER
# ============================

st.title("🚀 NexusCart AI")

st.write(
"""
AI Powered Retail Intelligence Platform

Excel → SQL → Python → Machine Learning → Power BI → Web
"""
)



# ============================
# SIDEBAR
# ============================

page = st.sidebar.selectbox(

    "Navigation",

    [
        "Dashboard",
        "AI Sales Prediction",
        "Dataset"
    ]
)



# ============================
# DASHBOARD
# ============================

if page == "Dashboard":


    revenue = df["Total Amount"].sum()

    orders = len(df)

    customers = df["Customer ID"].nunique()

    avg_order = df["Total Amount"].mean()



    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "Total Revenue",
        f"₹ {round(revenue,2)}"
    )


    col2.metric(
        "Total Orders",
        orders
    )


    col3.metric(
        "Total Customers",
        customers
    )


    col4.metric(
        "Average Order Value",
        f"₹ {round(avg_order,2)}"
    )


    st.divider()


    st.subheader(
        "Revenue By Product Category"
    )


    category = df.groupby(
        "Product Category"
    )["Total Amount"].sum()


    st.bar_chart(
        category
    )



# ============================
# AI PREDICTION
# ============================

elif page == "AI Sales Prediction":


    st.subheader(
        "🤖 AI Sales Forecast"
    )


    quantity = st.number_input(
        "Quantity",
        min_value=1
    )


    price = st.number_input(
        "Price Per Unit",
        min_value=1
    )


    age = st.number_input(
        "Customer Age",
        min_value=18,
        max_value=100
    )


    if st.button(
        "Generate Prediction"
    ):


        input_data = np.array(
            [
                [
                    quantity,
                    price,
                    age
                ]
            ]
        )


        prediction = model.predict(
            input_data
        )


        st.success(
            f"Predicted Revenue: ₹ {round(prediction[0],2)}"
        )



# ============================
# DATASET
# ============================

elif page == "Dataset":


    st.subheader(
        "Retail Sales Dataset"
    )


    st.dataframe(
        df,
        use_container_width=True
    )



# ============================
# FOOTER
# ============================

st.divider()

st.caption(
"NexusCart AI | Business Intelligence & Sales Prediction Platform"
)