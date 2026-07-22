import streamlit as st
import joblib
import numpy as np
import mysql.connector
import pandas as pd
import streamlit as st

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="NexusCart AI",
    page_icon="🚀",
    layout="wide"
)


# =====================================
# LOAD AI MODEL
# =====================================

model = joblib.load(
    "sales_prediction_model.pkl"
)


# =====================================
# MYSQL CONNECTION
# =====================================

def get_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kanu@2006",
        database="nexuscart"
    )


    query = "SELECT * FROM retail_sales"


    df = pd.read_sql(
        query,
        connection
    )


    connection.close()

    return df



# =====================================
# HEADER
# =====================================

st.title("🚀 NexusCart AI")

st.markdown(
"""
### AI Powered Retail Intelligence Platform

**Excel → SQL → Python → Machine Learning → Power BI → Web Application**
"""
)



# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("NexusCart AI")

page = st.sidebar.selectbox(

    "Navigation",

    [
        "Dashboard",
        "AI Sales Prediction",
        "Database View"
    ]

)



# =====================================
# DASHBOARD PAGE
# =====================================

if page == "Dashboard":


    df = get_data()


    total_revenue = df["Total Amount"].sum()

    total_orders = df.shape[0]

    total_customers = df["Customer ID"].nunique()

    avg_order = df["Total Amount"].mean()



    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "Total Revenue",
        f"₹ {total_revenue}"
    )


    col2.metric(
        "Total Orders",
        total_orders
    )


    col3.metric(
        "Customers",
        total_customers
    )


    col4.metric(
        "Average Order Value",
        f"₹ {round(avg_order,2)}"
    )



    st.divider()



    st.subheader(
        "Revenue By Product Category"
    )


    category = (

        df.groupby(
            "Product Category"
        )["Total Amount"]
        .sum()

    )


    st.bar_chart(
        category
    )



# =====================================
# AI PREDICTION PAGE
# =====================================

elif page == "AI Sales Prediction":


    st.subheader(
        "🤖 AI Sales Forecast"
    )


    st.write(
        "Enter customer and product details"
    )



    col1,col2,col3 = st.columns(3)


    with col1:

        quantity = st.number_input(
            "Quantity",
            min_value=1
        )


    with col2:

        price = st.number_input(
            "Price Per Unit",
            min_value=1
        )


    with col3:

        age = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=100
        )



    if st.button(
        "Generate Prediction"
    ):


        input_data = np.array(
            [[
                quantity,
                price,
                age
            ]]
        )


        prediction = model.predict(
            input_data
        )


        st.success(

            f"Predicted Revenue: ₹ {round(prediction[0],2)}"

        )



# =====================================
# DATABASE PAGE
# =====================================

elif page == "Database View":


    st.subheader(
        "MySQL Retail Sales Database"
    )


    df = get_data()


    st.dataframe(
        df,
        use_container_width=True
    )



# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
"""
© 2026 NexusCart AI | Business Intelligence & Sales Prediction Platform
"""
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