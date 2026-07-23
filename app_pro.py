# ==========================================
# NexusCart AI Pro
# PART 1/4
# Dashboard + Filters + Setup
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="NexusCart AI Pro",
    page_icon="🛒",
    layout="wide"
)



# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "retail_sales.csv"
    )

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

    return df



df = load_data()



# ==========================
# SIDEBAR
# ==========================

st.sidebar.title(
    "🛒 NexusCart AI Pro"
)


st.sidebar.write(
    "AI Powered Retail Intelligence Platform"
)



menu = st.sidebar.selectbox(
    "Navigation",
    [

        "Dashboard",

        "Sales Analysis",

        "Customer AI",

        "Churn Prediction",

        "AI Assistant",

        "Sales Forecast",

        "AI Prediction",

        "Recommendation"

    ]
)



# ==========================
# FILTER SYSTEM
# ==========================

st.sidebar.divider()

st.sidebar.subheader(
    "🔍 Smart Filters"
)


filtered_df = df.copy()



# Date Filter

if "Date" in df.columns:


    start_date = st.sidebar.date_input(
        "Start Date",
        df["Date"].min()
    )


    end_date = st.sidebar.date_input(
        "End Date",
        df["Date"].max()
    )


    filtered_df = filtered_df[
        (
            filtered_df["Date"]
            >= pd.to_datetime(start_date)
        )
        &
        (
            filtered_df["Date"]
            <= pd.to_datetime(end_date)
        )
    ]



# Category Filter

categories = st.sidebar.multiselect(

    "Product Category",

    df["Product Category"].unique(),

    default=df["Product Category"].unique()

)


filtered_df = filtered_df[
    filtered_df["Product Category"]
    .isin(categories)
]



# Gender Filter

genders = st.sidebar.multiselect(

    "Gender",

    df["Gender"].unique(),

    default=df["Gender"].unique()

)



filtered_df = filtered_df[
    filtered_df["Gender"]
    .isin(genders)
]



# Customer Type Filter

customers = st.sidebar.multiselect(

    "Customer Type",

    df["Customer Type"].unique(),

    default=df["Customer Type"].unique()

)



filtered_df = filtered_df[
    filtered_df["Customer Type"]
    .isin(customers)
]





# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":


    st.title(
        "🛒 NexusCart AI Pro"
    )


    st.subheader(
        "AI Powered Retail Business Intelligence"
    )


    st.write(
        "Analyze sales, customers and business performance."
    )


    st.divider()



    col1,col2,col3,col4 = st.columns(4)



    with col1:

        st.metric(

            "💰 Total Revenue",

            f"₹ {filtered_df['Total Amount'].sum():,.0f}"

        )


    with col2:

        st.metric(

            "📦 Total Orders",

            len(filtered_df)

        )


    with col3:

        st.metric(

            "👥 Customers",

            filtered_df["Customer ID"].nunique()

        )


    with col4:

        st.metric(

            "📈 Avg Order Value",

            f"₹ {filtered_df['Total Amount'].mean():,.0f}"

        )



    st.divider()



    category_sales = (

        filtered_df
        .groupby(
            "Product Category"
        )
        ["Total Amount"]
        .sum()
        .reset_index()

    )



    fig = px.bar(

        category_sales,

        x="Product Category",

        y="Total Amount",

        text_auto=True,

        title="Revenue By Category"

    )



    st.plotly_chart(

        fig,

        width="stretch"

    )



    st.subheader(
        "Data Preview"
    )


    st.dataframe(

        filtered_df.head(10),

        width="stretch"

    )# ==========================================
# PART 2/4
# Sales Analysis + Customer AI + Churn AI
# ==========================================


# ==========================
# SALES ANALYSIS
# ==========================

elif menu == "Sales Analysis":


    st.title(
        "📊 Advanced Sales Analysis"
    )


    col1,col2 = st.columns(2)



    with col1:


        category_sales = (

            filtered_df
            .groupby(
                "Product Category"
            )
            ["Total Amount"]
            .sum()
            .reset_index()

        )


        fig = px.pie(

            category_sales,

            names="Product Category",

            values="Total Amount",

            title="Revenue Share"

        )


        st.plotly_chart(

            fig,

            width="stretch"

        )



    with col2:


        gender_sales = (

            filtered_df
            .groupby(
                "Gender"
            )
            ["Total Amount"]
            .sum()
            .reset_index()

        )


        fig = px.bar(

            gender_sales,

            x="Gender",

            y="Total Amount",

            text_auto=True,

            title="Revenue By Gender"

        )


        st.plotly_chart(

            fig,

            width="stretch"

        )



    st.divider()



    if "Date" in filtered_df.columns:


        monthly_sales = (

            filtered_df
            .groupby(
                filtered_df["Date"].dt.month
            )
            ["Total Amount"]
            .sum()
            .reset_index()

        )


        monthly_sales.columns = [

            "Month",

            "Revenue"

        ]


        fig = px.line(

            monthly_sales,

            x="Month",

            y="Revenue",

            markers=True,

            title="Monthly Sales Trend"

        )


        st.plotly_chart(

            fig,

            width="stretch"

        )







# ==========================
# CUSTOMER AI SEGMENTATION
# ==========================

elif menu == "Customer AI":


    st.title(
        "👥 AI Customer Segmentation"
    )


    st.write(
        "Grouping customers using Machine Learning."
    )



    customer_data = (

        filtered_df
        .groupby(
            "Customer ID"
        )
        .agg(

            {

            "Total Amount":"sum",

            "Quantity":"sum",

            "Age":"mean"

            }

        )
        .reset_index()

    )



    if len(customer_data) >= 3:


        model = KMeans(

            n_clusters=3,

            random_state=42

        )


        customer_data["Segment"] = model.fit_predict(

            customer_data[

                [

                "Total Amount",

                "Quantity",

                "Age"

                ]

            ]

        )



        st.success(
            "Customer Segmentation Completed"
        )



        fig = px.scatter(

            customer_data,

            x="Total Amount",

            y="Quantity",

            color="Segment",

            size="Age",

            title="Customer Groups"

        )


        st.plotly_chart(

            fig,

            width="stretch"

        )


        st.dataframe(

            customer_data,

            width="stretch"

        )


    else:

        st.warning(
            "Not enough customer data."
        )







# ==========================
# CUSTOMER CHURN PREDICTION
# ==========================

elif menu == "Churn Prediction":


    st.title(
        "🚨 AI Customer Churn Prediction"
    )


    st.write(
        "Find customers who may stop purchasing."
    )



    customer_df = (

        filtered_df
        .groupby(
            "Customer ID"
        )
        .agg(

            {

            "Total Amount":"sum",

            "Quantity":"sum",

            "Age":"mean"

            }

        )
        .reset_index()

    )



    limit = customer_df["Total Amount"].median()



    customer_df["Churn"] = (

        customer_df["Total Amount"]
        < limit

    ).astype(int)



    X = customer_df[

        [

        "Total Amount",

        "Quantity",

        "Age"

        ]

    ]


    y = customer_df["Churn"]



    churn_model = RandomForestClassifier(

        random_state=42

    )


    churn_model.fit(

        X,

        y

    )


    st.success(
        "Churn AI Model Ready"
    )



    amount = st.number_input(

        "Customer Purchase Amount",

        0,

        100000,

        5000

    )


    quantity = st.number_input(

        "Quantity Purchased",

        1,

        1000,

        10

    )


    age = st.number_input(

        "Customer Age",

        10,

        100,

        30

    )



    if st.button(
        "Predict Churn Risk"
    ):



        prediction = churn_model.predict(

            [

                [

                amount,

                quantity,

                age

                ]

            ]

        )



        risk = churn_model.predict_proba(

            [

                [

                amount,

                quantity,

                age

                ]

            ]

        )[0][1]



        if prediction[0] == 1:


            st.error(

                f"""

                🔴 High Churn Risk


                Probability:

                {risk*100:.2f}%


                Action:

                Send discount offers.

                """

            )


        else:


            st.success(

                f"""

                🟢 Low Churn Risk


                Probability:

                {risk*100:.2f}%


                Customer is valuable.

                """

            )# ==========================================
# PART 3/4
# AI Assistant + Sales Forecast
# ==========================================



# ==========================
# AI BUSINESS ASSISTANT
# ==========================

elif menu == "AI Assistant":


    st.title(
        "🤖 NexusCart AI Business Assistant"
    )


    st.write(
        "AI generated business insights from your sales data."
    )



    total_revenue = (

        filtered_df["Total Amount"]
        .sum()

    )


    total_orders = len(
        filtered_df
    )


    best_category = (

        filtered_df
        .groupby(
            "Product Category"
        )
        ["Total Amount"]
        .sum()
        .idxmax()

    )


    best_customer = (

        filtered_df
        .groupby(
            "Customer Type"
        )
        ["Total Amount"]
        .sum()
        .idxmax()

    )



    col1,col2,col3 = st.columns(3)



    with col1:

        st.metric(

            "Total Revenue",

            f"₹ {total_revenue:,.0f}"

        )



    with col2:

        st.metric(

            "Best Category",

            best_category

        )



    with col3:

        st.metric(

            "Best Customer",

            best_customer

        )



    st.divider()



    st.subheader(
        "🧠 AI Business Report"
    )



    st.success(

f"""

Business Analysis:


💰 Revenue:

₹ {total_revenue:,.0f}


📦 Orders:

{total_orders}


🏆 Top Category:

{best_category}


👥 Best Customer Segment:

{best_customer}



AI Recommendation:


Increase marketing for {best_category}

Focus on {best_customer} customers.

"""

    )



    st.divider()



    st.subheader(
        "Ask AI Business Question"
    )


    question = st.text_input(

        "Example: Which category gives highest revenue?"

    )



    if st.button(
        "Generate Answer"
    ):


        q = question.lower()



        if "category" in q:


            st.info(

                f"Best category is {best_category}"

            )


        elif "revenue" in q:


            st.info(

                f"Total revenue is ₹{total_revenue:,.0f}"

            )


        elif "customer" in q:


            st.info(

                f"Best customer group is {best_customer}"

            )


        else:


            st.warning(

                "Ask about category, revenue or customer."

            )







# ==========================
# SALES FORECASTING AI
# ==========================

elif menu == "Sales Forecast":


    st.title(
        "📈 AI Sales Forecasting"
    )


    st.write(
        "Predict future sales using Machine Learning."
    )



    if "Date" in filtered_df.columns:



        sales_data = (

            filtered_df
            .groupby("Date")
            ["Total Amount"]
            .sum()
            .reset_index()

        )



        sales_data["Days"] = (

            sales_data["Date"]

            -

            sales_data["Date"].min()

        ).dt.days



        if len(sales_data) > 2:



            model = LinearRegression()



            model.fit(

                sales_data[["Days"]],

                sales_data["Total Amount"]

            )



            future = pd.DataFrame(

                {

                "Days":

                [

                sales_data["Days"].max()+30

                ]

                }

            )



            prediction = model.predict(
                future
            )



            st.metric(

                "Next Month Expected Revenue",

                f"₹ {prediction[0]:,.0f}"

            )



            fig = px.line(

                sales_data,

                x="Date",

                y="Total Amount",

                markers=True,

                title="Sales History"

            )



            st.plotly_chart(

                fig,

                width="stretch"

            )


        else:


            st.warning(
                "Need more sales data."
            )



    else:


        st.error(
            "Date column not available."
        )# ==========================================
# PART 4/4
# AI Prediction + Recommendation + Export
# ==========================================



# ==========================
# AI SALES PREDICTION
# ==========================

elif menu == "AI Prediction":


    st.title(
        "🤖 NexusCart AI Sales Prediction"
    )


    st.write(
        "Predict customer purchase amount using Machine Learning."
    )


    try:


        model = joblib.load(
            "NexusAI_Model.pkl"
        )


        col1,col2,col3 = st.columns(3)



        with col1:

            age = st.number_input(

                "Customer Age",

                10,

                100,

                30

            )


        with col2:

            quantity = st.number_input(

                "Quantity",

                1,

                100,

                1

            )


        with col3:

            price = st.number_input(

                "Price Per Unit",

                1,

                10000,

                500

            )



        if st.button(
            "🚀 Predict Sales"
        ):



            input_data = pd.DataFrame(

                {

                "Age":[age],

                "Quantity":[quantity],

                "Price per Unit":[price]

                }

            )



            result = model.predict(

                input_data

            )[0]



            st.success(

                f"Predicted Sales Amount: ₹ {result:,.2f}"

            )


    except Exception as e:


        st.error(

            "AI model not found. Train model first."

        )







# ==========================
# PRODUCT RECOMMENDATION
# ==========================

elif menu == "Recommendation":


    st.title(
        "🛒 AI Product Recommendation"
    )


    st.write(
        "Recommend high performing products."
    )



    product_data = (

        filtered_df
        .groupby(
            "Product Category"
        )
        .agg(

            {

            "Quantity":"sum",

            "Total Amount":"sum"

            }

        )
        .reset_index()

    )



    product_data = product_data.sort_values(

        by="Total Amount",

        ascending=False

    )



    st.subheader(
        "⭐ Recommended Categories"
    )



    for _,row in product_data.head(5).iterrows():


        st.success(

f"""

🛍️ Category:

{row['Product Category']}


💰 Revenue:

₹ {row['Total Amount']:,.0f}


📦 Quantity Sold:

{row['Quantity']}

"""

        )



    fig = px.bar(

        product_data,

        x="Product Category",

        y="Total Amount",

        title="Product Performance"

    )



    st.plotly_chart(

        fig,

        width="stretch"

    )







# ==========================
# EXPORT REPORT
# ==========================

st.sidebar.divider()


st.sidebar.subheader(
    "📥 Download Report"
)



csv = filtered_df.to_csv(

    index=False

)



st.sidebar.download_button(

    label="Download CSV",

    data=csv,

    file_name="NexusCart_Sales_Report.csv",

    mime="text/csv"

)






# ==========================
# FOOTER
# ==========================

st.sidebar.divider()


st.sidebar.info(

"""

🛒 NexusCart AI Pro


Features:


✅ Business Dashboard

✅ Sales Analytics

✅ Customer Segmentation

✅ Churn Prediction

✅ AI Assistant

✅ Sales Forecast

✅ AI Prediction

✅ Recommendation


Technology:


Python

Pandas

Streamlit

Plotly

Machine Learning

"""

)