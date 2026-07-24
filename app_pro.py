# ==========================================
# NEXUSCART AI PRO
# PART 1/4
# BASE SETUP
# ==========================================


import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np



# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="NexusCart AI Pro",

    page_icon="🛒",

    layout="wide"

)



# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv("retail_sales.csv")


        # Convert amount

        if "Total Amount" in df.columns:

            df["Total Amount"] = pd.to_numeric(

                df["Total Amount"],

                errors="coerce"

            )


        # Convert date

        if "Date" in df.columns:

            df["Date"] = pd.to_datetime(

                df["Date"],

                errors="coerce"

            )


        return df


    except Exception as e:

        st.error(

            f"Dataset loading error: {e}"

        )

        return pd.DataFrame()



df = load_data()



# Stop if data not loaded

if df.empty:

    st.warning(

        "Dataset not found. Put retail_sales.csv in the same folder."

    )

    st.stop()



# ==========================================
# SIDEBAR NAVIGATION
# ==========================================


st.sidebar.title(

    "🛒 NexusCart AI Pro"

)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Sales Analysis",
        "Customer AI",
        "Churn Prediction",
        "AI Assistant",
        "Sales Forecast",
        "AI Prediction",
        "Recommendation",
        "Customer Support",
        "About"
    ]
)

# ==========================================
# SIDEBAR INFO
# ==========================================


st.sidebar.divider()


st.sidebar.success(

    "AI Powered Retail Intelligence"

)


st.sidebar.caption(

    "Python • ML • Analytics • AI"

)



# ==========================================
# GLOBAL HEADER
# ==========================================


st.title(

    "🛒 NexusCart AI Pro"

)


st.caption(

    "Enterprise AI Powered Retail Business Intelligence Platform"

)
# ==========================================
# PART 2/4
# DASHBOARD PAGE
# ==========================================


if menu == "Dashboard":


    st.header(

        "📊 Business Dashboard"

    )


    st.write(

        "Analyze sales, customers and business performance using Artificial Intelligence."

    )



    st.divider()



    # ==========================
    # KPI CALCULATION
    # ==========================


    total_revenue = df["Total Amount"].sum()

    total_orders = len(df)

    total_customers = df["Customer ID"].nunique()

    avg_order = df["Total Amount"].mean()



    # ==========================
    # KPI CARDS
    # ==========================


    col1, col2, col3, col4 = st.columns(4)



    with col1:

        st.metric(

            "💰 Total Revenue",

            f"₹ {total_revenue:,.0f}"

        )



    with col2:

        st.metric(

            "📦 Total Orders",

            f"{total_orders:,}"

        )



    with col3:

        st.metric(

            "👥 Customers",

            f"{total_customers:,}"

        )



    with col4:

        st.metric(

            "📈 Average Order",

            f"₹ {avg_order:,.0f}"

        )



    st.divider()



    # ==========================
    # CATEGORY REVENUE CHART
    # ==========================


    st.subheader(

        "📊 Revenue By Product Category"

    )



    category_sales = (

        df.groupby("Product Category")

        ["Total Amount"]

        .sum()

        .reset_index()

    )



    fig_category = px.bar(

        category_sales,

        x="Product Category",

        y="Total Amount",

        text_auto=True,

        title="Category Wise Revenue"

    )



    st.plotly_chart(

        fig_category,

        use_container_width=True

    )



    st.divider()



    # ==========================
    # TWO COLUMN CHARTS
    # ==========================


    col5, col6 = st.columns(2)



    with col5:


        gender_sales = (

            df.groupby("Gender")

            ["Total Amount"]

            .sum()

            .reset_index()

        )


        fig_gender = px.pie(

            gender_sales,

            names="Gender",

            values="Total Amount",

            title="Revenue By Gender"

        )


        st.plotly_chart(

            fig_gender,

            use_container_width=True

        )



    with col6:


        customer_sales = (

            df.groupby("Customer Type")

            ["Total Amount"]

            .sum()

            .reset_index()

        )


        fig_customer = px.bar(

            customer_sales,

            x="Customer Type",

            y="Total Amount",

            text_auto=True,

            title="Customer Type Performance"

        )


        st.plotly_chart(

            fig_customer,

            use_container_width=True

        )



    st.divider()



    # ==========================
    # RECENT SALES TABLE
    # ==========================


    st.subheader(

        "🧾 Recent Sales Data"

    )



    st.dataframe(

        df.head(10),

        use_container_width=True

    )
    # ==========================================
# PART 3/4
# SALES ANALYSIS
# CUSTOMER AI
# CHURN PREDICTION
# AI PREDICTION
# ==========================================



# ==========================================
# SALES ANALYSIS
# ==========================================


if menu == "Sales Analysis":


    st.header(

        "📊 Advanced Sales Analysis"

    )


    st.write(

        "Detailed business sales insights."

    )


    st.divider()



    # Category Sales


    category_sales = (

        df.groupby("Product Category")

        ["Total Amount"]

        .sum()

        .reset_index()

    )


    fig1 = px.pie(

        category_sales,

        names="Product Category",

        values="Total Amount",

        title="Revenue Share By Category"

    )


    st.plotly_chart(

        fig1,

        use_container_width=True

    )



    # Monthly Sales


    if "Date" in df.columns:


        monthly_sales = (

            df.groupby(

                df["Date"].dt.month

            )

            ["Total Amount"]

            .sum()

            .reset_index()

        )


        monthly_sales.columns = [

            "Month",

            "Revenue"

        ]



        fig2 = px.line(

            monthly_sales,

            x="Month",

            y="Revenue",

            markers=True,

            title="Monthly Sales Trend"

        )


        st.plotly_chart(

            fig2,

            use_container_width=True

        )





# ==========================================
# CUSTOMER AI
# ==========================================


if menu == "Customer AI":


    st.header(

        "🤖 Customer Intelligence AI"

    )


    st.write(

        "Analyze customer behaviour and value."

    )


    st.divider()



    total_customers = df["Customer ID"].nunique()



    avg_spend = df["Total Amount"].mean()



    col1,col2 = st.columns(2)



    with col1:

        st.metric(

            "👥 Total Customers",

            f"{total_customers:,}"

        )



    with col2:

        st.metric(

            "💰 Average Customer Spend",

            f"₹ {avg_spend:,.0f}"

        )



    customer_value = (

        df.groupby("Customer ID")

        ["Total Amount"]

        .sum()

        .reset_index()

        .sort_values(

            "Total Amount",

            ascending=False

        )

    )


    st.subheader(

        "⭐ Top Customers"

    )


    st.dataframe(

        customer_value.head(10),

        use_container_width=True

    )





# ==========================================
# CHURN PREDICTION
# ==========================================


if menu == "Churn Prediction":


    st.header(

        "🔮 Customer Churn Prediction"

    )


    st.write(

        "Identify customers who may stop purchasing."

    )


    st.info(

        "Machine Learning churn model can be connected here."

    )


    churn_threshold = st.slider(

        "Select spending risk level",

        0,

        10000,

        3000

    )



    risky_customers = df[

        df["Total Amount"] < churn_threshold

    ]



    st.metric(

        "⚠️ Possible Risk Customers",

        len(risky_customers)

    )


    st.dataframe(

        risky_customers.head(10),

        use_container_width=True

    )





# ==========================================
# AI PREDICTION
# ==========================================


if menu == "AI Prediction":


    st.header(
        "🧠 NexusCart AI Prediction Center"
    )


    st.caption(
        "AI powered business prediction and decision support system"
    )


    st.divider()



    # ==========================
    # PREDICTION SELECTOR
    # ==========================


    prediction_type = st.selectbox(

        "Select Prediction Type",

        [

            "Sales Prediction",

            "Customer Behaviour Prediction",

            "Product Demand Prediction",

            "Revenue Prediction"

        ]

    )



    st.divider()



    # ==========================
    # SALES PREDICTION
    # ==========================


    if prediction_type == "Sales Prediction":


        st.subheader(

            "📈 Future Sales Prediction"

        )


        current_sales = df["Total Amount"].sum()



        growth = st.slider(

            "Expected Growth (%)",

            0,

            100,

            20

        )



        predicted_sales = current_sales + (

            current_sales * growth / 100

        )



        col1, col2 = st.columns(2)



        with col1:

            st.metric(

                "Current Sales",

                f"₹ {current_sales:,.0f}"

            )



        with col2:

            st.metric(

                "Predicted Sales",

                f"₹ {predicted_sales:,.0f}",

                f"{growth}% Growth"

            )





    # ==========================
    # CUSTOMER BEHAVIOUR
    # ==========================


    elif prediction_type == "Customer Behaviour Prediction":


        st.subheader(

            "👥 Customer Behaviour Analysis"

        )


        avg_customer = (

            df.groupby("Customer ID")

            ["Total Amount"]

            .sum()

            .mean()

        )


        st.metric(

            "Average Customer Spending",

            f"₹ {avg_customer:,.0f}"

        )


        st.success(

            "AI predicts customer purchasing behaviour based on sales history."

        )





    # ==========================
    # PRODUCT DEMAND
    # ==========================


    elif prediction_type == "Product Demand Prediction":


        st.subheader(

            "📦 Product Demand Prediction"

        )


        demand = (

            df.groupby("Product Category")

            ["Total Amount"]

            .sum()

            .reset_index()

            .sort_values(

                "Total Amount",

                ascending=False

            )

        )


        st.write(

            "🔥 High Demand Categories"

        )


        st.dataframe(

            demand.head(5),

            use_container_width=True

        )





    # ==========================
    # REVENUE PREDICTION
    # ==========================


    else:


        st.subheader(

            "💰 Revenue Forecast"

        )


        monthly_avg = (

            df["Total Amount"].sum()

        ) / 12



        st.metric(

            "Expected Monthly Revenue",

            f"₹ {monthly_avg:,.0f}"

        )


        st.info(

            "Prediction generated using historical retail data."

        )



    st.divider()



    st.success(

        "🤖 AI Prediction Engine is Active"

    )




    # ==========================================
# PART 4/4
# AI ASSISTANT
# SALES FORECAST
# RECOMMENDATION
# CUSTOMER SUPPORT
# ==========================================

# ==========================================
# AI ASSISTANT
# ==========================================


if menu == "AI Assistant":


    st.header(
        "🤖 NexusCart AI Assistant"
    )


    st.caption(
        "Your intelligent retail business assistant"
    )


    st.divider()



    # ==========================
    # CHAT INPUT
    # ==========================


    st.subheader(
        "💬 Ask NexusCart AI"
    )


    user_question = st.text_input(

        "Enter your business question"

    )



    if user_question:


        question = user_question.lower()



        # Total Sales

        if "sales" in question or "revenue" in question:


            total_sales = df["Total Amount"].sum()


            st.success(

                f"💰 Total Revenue Generated: ₹ {total_sales:,.0f}"

            )



        # Orders

        elif "order" in question:


            total_orders = len(df)


            st.success(

                f"📦 Total Orders: {total_orders:,}"

            )



        # Customers

        elif "customer" in question:


            total_customers = df["Customer ID"].nunique()


            st.success(

                f"👥 Total Customers: {total_customers:,}"

            )



        # Best Category

        elif "best" in question or "top" in question or "product" in question:


            best_category = (

                df.groupby("Product Category")

                ["Total Amount"]

                .sum()

                .idxmax()

            )


            st.success(

                f"🏆 Highest Revenue Category: {best_category}"

            )



        # Average Order

        elif "average" in question or "avg" in question:


            average_order = df["Total Amount"].mean()


            st.success(

                f"📈 Average Order Value: ₹ {average_order:,.0f}"

            )



        # Unknown Question

        else:


            st.info(

                "I can help you with sales, customers, orders, products and revenue analysis."

            )



    st.divider()



    # ==========================
    # LIKELY QUESTIONS
    # ==========================


    st.subheader(

        "💡 Likely Questions"

    )


    likely_questions = [

        "What is total sales?",

        "How many customers do we have?",

        "What is the best product category?",

        "What is average order value?",

        "How many orders are completed?",

        "Which category generates highest revenue?"

    ]



    for question in likely_questions:


        st.info(

            "🤖 " + question

        )



    st.divider()



    # ==========================
    # AI STATUS
    # ==========================


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(

            "🧠 AI Status",

            "Active"

        )



    with col2:

        st.metric(

            "📊 Data Rows",

            f"{len(df):,}"

        )



    with col3:

        st.metric(

            "⚡ Response",

            "Instant"

        )



    st.success(

        "🚀 NexusCart AI Assistant is ready!"

    )

# ==========================================
# SALES FORECAST
# ==========================================


if menu == "Sales Forecast":


    st.header(

        "📈 AI Sales Forecast"

    )


    st.write(

        "Future sales estimation using AI models."

    )


    daily_sales = (

        df.groupby("Date")

        ["Total Amount"]

        .sum()

        .reset_index()

    )



    if "Date" in df.columns:


        fig_forecast = px.line(

            daily_sales,

            x="Date",

            y="Total Amount",

            title="Sales Trend"

        )


        st.plotly_chart(

            fig_forecast,

            use_container_width=True

        )


    st.success(

        "Forecast module is ready for ML integration."

    )





# ==========================================
# RECOMMENDATION SYSTEM
# ==========================================


if menu == "Recommendation":


    st.header(

        "⭐ AI Product Recommendation"

    )


    st.write(

        "Recommended products based on sales performance."

    )


    recommendation = (

        df.groupby("Product Category")

        ["Total Amount"]

        .sum()

        .reset_index()

        .sort_values(

            "Total Amount",

            ascending=False

        )

    )


    st.subheader(

        "🔥 Top Recommended Categories"

    )


    st.dataframe(

        recommendation.head(5),

        use_container_width=True

    )





# ==========================================
# CUSTOMER SUPPORT
# ==========================================


if menu == "Customer Support":


    st.header(
        "📞 NexusCart AI Customer Support"
    )


    st.caption(
        "AI Powered Retail Customer Assistance System"
    )


    st.divider()



    # ==========================
    # CONTACT DETAILS
    # ==========================


    st.subheader(
        "📇 Contact Support"
    )


    col1, col2 = st.columns(2)



    with col1:

        st.info(
            """
            👤 Support Team

            NexusCart AI Support

            📧 Email:
            ta@gmail.com

            📱 Mobile:
            +91 8617546549
            """
        )



    with col2:

        st.success(
            """
            🕒 Support Hours

            Monday - Saturday

            9:00 AM - 6:00 PM

            ⚡ Response Time:
            Within 24 Hours
            """
        )



    st.divider()



    # ==========================
    # AI SUPPORT CHAT
    # ==========================


    st.subheader(
        "💬 Ask NexusCart AI"
    )


    query = st.text_input(
        "Enter your question"
    )



    if query:


        q = query.lower()



        if "refund" in q:

            st.warning(
                "Refund requests are processed within 5-7 working days."
            )


        elif "delivery" in q:

            st.info(
                "Please provide your order ID to check delivery status."
            )


        elif "order" in q:

            st.success(
                "Your order details can be checked using customer ID."
            )


        else:

            st.success(
                "Thank you for contacting NexusCart AI Support. Our team will assist you."
            )



    st.divider()



    # ==========================
    # SUPPORT FEATURES
    # ==========================


    st.subheader(
        "🛠 Support Services"
    )


    support_data = {

        "Service":[

            "Order Tracking",

            "Refund Support",

            "Product Information",

            "Complaint Handling",

            "Feedback"

        ],

        "Status":[

            "Active",

            "Active",

            "Active",

            "Active",

            "Active"

        ]

    }


    st.dataframe(

        pd.DataFrame(support_data),

        use_container_width=True

    )

# ==========================================
# ABOUT SECTION
# ==========================================


if menu == "About":


    st.header(
        "🛒 About NexusCart AI Pro"
    )


    st.caption(
        "AI Powered Retail Business Intelligence Platform"
    )


    st.divider()



    # ==========================
    # PROJECT INTRODUCTION
    # ==========================


    st.subheader(
        "🚀 Project Overview"
    )


    st.write(
        """
        NexusCart AI Pro is an Artificial Intelligence based
        Retail Business Intelligence Platform designed to analyze
        sales performance, customer behaviour, and business trends.

        The platform converts raw retail data into meaningful
        insights using Data Analytics, Machine Learning, and AI.

        It helps businesses understand revenue patterns,
        customer segments, product performance, and future
        sales opportunities.
        """
    )



    st.divider()



    # ==========================
    # DEVELOPER INFORMATION
    # ==========================


    col1, col2 = st.columns(2)



    with col1:


        st.subheader(
            "👨‍💻 Project Developer"
        )


        st.write(
            """
            **Tapobrata Deghuria**

            BCA Student

            Data Analytics & AI Enthusiast

            Developed:
            NexusCart AI Pro
            """
        )



    with col2:


        st.subheader(
            "🎯 Project Objective"
        )


        st.write(
            """
            • Analyze retail sales data

            • Understand customer behaviour

            • Predict business outcomes

            • Generate AI-based insights

            • Support data-driven decisions
            """
        )



    st.divider()



    # ==========================
    # TECHNOLOGIES USED
    # ==========================


    st.subheader(
        "🛠 Technologies & Tools Used"
    )


    st.write(
        """
        ### 🐍 Programming Language

        • Python — Used for data processing,
          analytics, automation, and AI development.


        ### 📊 Data Analysis

        • Pandas — Data cleaning and manipulation.

        • NumPy — Numerical calculations.


        ### 📈 Data Visualization

        • Plotly — Interactive business charts.

        • Streamlit — Web-based dashboard development.


        ### 🤖 Artificial Intelligence & Machine Learning

        • Scikit-Learn — Machine learning model implementation.

        • Predictive Analytics — Sales forecasting,
          churn prediction, and customer analysis.


        ### 🗄 Database Technology

        • SQL — Data storage, querying, and analysis.


        ### 📊 Business Intelligence

        • Power BI — Advanced dashboards and reporting.

        • Microsoft Excel — Data preparation and analysis.


        ### 🚀 Development Tools

        • Git & GitHub — Version control and project management.

        • VS Code — Application development environment.
        """
    )



    st.divider()



    # ==========================
    # KEY FEATURES
    # ==========================


    st.subheader(
        "✨ Key Features"
    )


    features = [

        "📊 Business Intelligence Dashboard",

        "📈 Sales Analysis",

        "👥 Customer Intelligence",

        "🔮 Churn Prediction",

        "🤖 AI Assistant",

        "📅 Sales Forecasting",

        "⭐ Product Recommendation",

        "🧠 AI Prediction System"

    ]


    for feature in features:

        st.success(feature)



    st.divider()



    st.info(
        "🛒 NexusCart AI Pro | Developed by Tapobrata Deghuria"
    )
    
# ==========================================
# FOOTER
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "🛒 NexusCart AI Pro"
)

st.sidebar.caption(
    "Developed by: Tapobrata Deghuria"
)

st.sidebar.caption(
    "Python | Streamlit | Machine Learning | AI"
)

st.sidebar.caption(
    "© 2026 All Rights Reserved"
)