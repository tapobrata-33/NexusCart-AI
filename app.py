import streamlit as st
import joblib
import numpy as np
import pandas as pd


# ============================
# PAGE CONFIGURATION
# ============================

st.set_page_config(
    page_title="NexusCart AI",
    page_icon="🚀",
    layout="wide"
)

# ============================
# LOAD MODEL
# ============================

model = joblib.load(
    "sales_prediction_model.pkl"
)



# ============================
# LOAD DATASET
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

st.markdown(
"""
### AI Powered Retail Intelligence Platform

Excel → SQL → Python → Machine Learning → Power BI → Web Application
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


    total_revenue = df["Total Amount"].sum()

    total_orders = len(df)

    total_customer = df["Customer ID"].nunique()

    average_order = df["Total Amount"].mean()



    col1,col2,col3,col4 = st.columns(4)



    col1.metric(
        "Total Revenue",
        f"₹ {round(total_revenue,2)}"
    )


    col2.metric(
        "Total Orders",
        total_orders
    )


    col3.metric(
        "Customers",
        total_customer
    )


    col4.metric(
        "Average Order",
        f"₹ {round(average_order,2)}"
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
        min_value=1,
        value=1
    )


    price = st.number_input(
        "Price Per Unit",
        min_value=1,
        value=100
    )


    age = st.number_input(
        "Customer Age",
        min_value=18,
        max_value=100,
        value=25
    )



    if st.button(
        "Generate Prediction"
    ):


        required_features = model.n_features_in_



        if required_features == 1:

            input_data = np.array(
                [
                    [
                        quantity
                    ]
                ]
            )


        elif required_features == 2:

            input_data = np.array(
                [
                    [
                        quantity,
                        price
                    ]
                ]
            )


        elif required_features == 3:

            input_data = np.array(
                [
                    [
                        quantity,
                        price,
                        age
                    ]
                ]
            )


        else:

            st.error(
                "Your model has unsupported number of features"
            )

            st.stop()



        prediction = model.predict(
            input_data
        )


        st.success(
            f"Predicted Revenue: ₹ {round(prediction[0],2)}"
        )





# ============================
# DATASET VIEW
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
"""
© 2026 NexusCart AI |
Business Intelligence & Sales Prediction Platform
"""
)
