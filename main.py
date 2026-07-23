import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page Setup
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🤖",
    layout="wide"
)


# Title
st.title("🤖 NEXUS AI")
st.subheader("AI Business Intelligence Dashboard")


st.success("NEXUS AI Dashboard Loaded Successfully")


# Upload Dataset
st.sidebar.header("Upload Data")

file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


if file:

    df = pd.read_csv(file)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())


    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Total Columns",
            len(df.columns)
        )


    st.subheader("Data Summary")

    st.write(df.describe())


else:

    st.info(
        "Please upload your sales CSV dataset from the left sidebar"
    )
    import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NexusCart AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 NexusCart AI")
st.subheader("AI Powered Retail Business Intelligence Dashboard")


# Load Dataset
try:
    df = pd.read_csv("retail_sales.csv")
    st.success("Dataset Loaded Successfully")

except Exception as e:
    st.error(e)
    st.stop()


# KPI Cards

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"₹ {df['Total Amount'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Transactions",
        df.shape[0]
    )

with col3:
    st.metric(
        "Product Categories",
        df["Product Category"].nunique()
    )


st.divider()


# Data Preview

st.header("📋 Sales Data")

st.dataframe(df.head(20))


# Chart

st.header("📊 Revenue By Category")

category_sales = df.groupby(
    "Product Category"
)["Total Amount"].sum()

st.bar_chart(category_sales)


# Monthly Sales

st.header("📈 Monthly Sales Trend")

monthly = df.groupby(
    "Date"
)["Total Amount"].sum()

st.line_chart(monthly)
