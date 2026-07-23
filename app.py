import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="NexusCart AI",
    page_icon="🛒",
    layout="wide"
)


# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    return pd.read_csv("retail_sales.csv")


df = load_data()



# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🛒 NexusCart AI")

st.sidebar.write(
    "AI Retail Analytics Platform"
)


menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Sales Analysis",
        "Customer Analysis",
        "AI Prediction",
        "AI Business Assistant"
    ]
)



# ==========================
# FILTERS
# ==========================

st.sidebar.divider()

st.sidebar.subheader("🔍 Filters")


filtered_df = df.copy()


# Category Filter

category = st.sidebar.multiselect(
    "Product Category",
    df["Product Category"].unique(),
    default=df["Product Category"].unique()
)


filtered_df = filtered_df[
    filtered_df["Product Category"].isin(category)
]



# Gender Filter

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)


filtered_df = filtered_df[
    filtered_df["Gender"].isin(gender)
]



# Customer Type Filter

customer = st.sidebar.multiselect(
    "Customer Type",
    df["Customer Type"].unique(),
    default=df["Customer Type"].unique()
)


filtered_df = filtered_df[
    filtered_df["Customer Type"].isin(customer)
]





# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":


    st.title("🛒 NexusCart AI")

    st.subheader(
        "AI Powered Retail Business Intelligence Platform"
    )


    st.write(
        "Analyze customer behavior, revenue trends and business performance."
    )


    # KPI CARDS

    col1,col2,col3,col4 = st.columns(4)


    with col1:

        st.metric(
            "💰 Total Revenue",
            f"₹ {filtered_df['Total Amount'].sum():,.0f}"
        )


    with col2:

        st.metric(
            "📦 Orders",
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



    # Revenue Chart

    category_sales = (
        filtered_df.groupby(
            "Product Category"
        )["Total Amount"]
        .sum()
        .reset_index()
    )


    fig = px.bar(
        category_sales,
        x="Product Category",
        y="Total Amount",
        title="Revenue By Category",
        text_auto=True
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )




# ==========================
# SALES ANALYSIS
# ==========================

elif menu == "Sales Analysis":


    st.title("📊 Sales Analysis")


    col1,col2 = st.columns(2)


    with col1:


        gender_sales = (
            filtered_df.groupby(
                "Gender"
            )["Total Amount"]
            .sum()
            .reset_index()
        )


        fig = px.pie(
            gender_sales,
            names="Gender",
            values="Total Amount",
            title="Revenue By Gender"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )



    with col2:


        fig = px.histogram(
            filtered_df,
            x="Total Amount",
            title="Sales Distribution"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )





# ==========================
# CUSTOMER ANALYSIS
# ==========================

elif menu == "Customer Analysis":


    st.title("👥 Customer Analysis")


    customer_sales = (
        filtered_df.groupby(
            "Customer Type"
        )["Total Amount"]
        .sum()
        .reset_index()
    )


    fig = px.pie(
        customer_sales,
        names="Customer Type",
        values="Total Amount",
        title="Customer Segments"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    st.subheader(
        "Top Customers"
    )


    top_customer = (
        filtered_df.groupby(
            "Customer ID"
        )["Total Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    st.dataframe(
        top_customer,
        width="stretch"
    )





# ==========================
# AI PREDICTION
# ==========================

elif menu == "AI Prediction":


    st.title("🤖 NexusCart AI Prediction")


    try:

        model = joblib.load(
            "NexusAI_Model.pkl"
        )


        age = st.number_input(
            "Customer Age",
            10,
            100,
            30
        )


        quantity = st.number_input(
            "Quantity",
            1,
            100,
            1
        )


        price = st.number_input(
            "Price Per Unit",
            1,
            10000,
            500
        )


        if st.button("🚀 Predict"):


            prediction = model.predict(
                [
                    [
                        age,
                        quantity,
                        price
                    ]
                ]
            )


            st.success(
                f"Predicted Sales Amount: ₹ {prediction[0]:,.2f}"
            )


    except:

        st.error(
            "AI Model file not found"
        )
# ==========================
# AI BUSINESS ASSISTANT
# ==========================

elif menu == "AI Business Assistant":


    st.title("🤖 NexusCart AI Business Assistant")


    st.write(
        "AI generated business insights from your retail data."
    )


    total_revenue = filtered_df["Total Amount"].sum()


    top_category = (
        filtered_df.groupby(
            "Product Category"
        )["Total Amount"]
        .sum()
        .idxmax()
    )


    top_customer_type = (
        filtered_df.groupby(
            "Customer Type"
        )["Total Amount"]
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
            top_category
        )


    with col3:

        st.metric(
            "Best Customer Segment",
            top_customer_type
        )



    st.divider()


    st.subheader(
        "🧠 AI Generated Insights"
    )


    st.success(
        f"""
        📌 {top_category} is currently the highest revenue generating category.

        📌 {top_customer_type} customers contribute the most business value.

        📌 Total business revenue analyzed:
        ₹ {total_revenue:,.0f}

        📌 Recommendation:
        Focus marketing campaigns on high-performing categories
        and customer segments.
        """
    )



    st.subheader(
        "Ask Business Questions"
    )


    question = st.text_input(
        "Example: Which category performs best?"
    )


    if st.button("Generate Answer"):


        question = question.lower()


        if "category" in question:

            st.info(
                f"Best performing category is {top_category}"
            )


        elif "customer" in question:

            st.info(
                f"Most valuable customer segment is {top_customer_type}"
            )


        elif "revenue" in question:

            st.info(
                f"Total revenue is ₹ {total_revenue:,.0f}"
            )


        else:

            st.warning(
                "Try asking about revenue, category or customers."
            )


# ==========================
# FOOTER
# ==========================

st.sidebar.divider()

st.sidebar.info(
"""
NexusCart AI

Built With:

Python
Pandas
Streamlit
Plotly
Machine Learning
"""
)