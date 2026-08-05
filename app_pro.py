# ==========================================================
# NEXUS CART AI PRO
# PART 1 : SETUP + SIDEBAR + HEADER + KPI
# ==========================================================


import streamlit as st
import pandas as pd
import numpy as np


import plotly.express as px
import plotly.graph_objects as go

from streamlit_option_menu import option_menu

from datetime import datetime
import joblib
model = joblib.load("NexusAI_Model.pkl")


# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(

    page_title="NexusCart AI Pro",

    page_icon="🛒",

    layout="wide",

    initial_sidebar_state="expanded"

)



# ==========================================================
# LOAD CSS
# ==========================================================


def load_css():

    try:

        with open("style.css") as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )

    except:

        pass



load_css()



# ==========================================================
# DATA GENERATION
# Replace with retail_sales.csv later
# ==========================================================


np.random.seed(42)


categories = [

    "Electronics",

    "Fashion",

    "Beauty",

    "Furniture",

    "Groceries"

]


months = [

    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"

]



df = pd.DataFrame({

    "Month":months,

    "Sales":np.random.randint(

        30000,

        90000,

        12

    ),

    "Orders":np.random.randint(

        100,

        500,

        12

    )

})



# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================


with st.sidebar:


    st.markdown(

        """

        <h2 style="text-align:center">

        🛒 NexusCart AI

        </h2>

        """,

        unsafe_allow_html=True

    )


    st.write("")


    selected = option_menu(

        menu_title=None,


        options=[


            "Dashboard",

            "Sales",

            "Products",

            "Customers",

            "AI Prediction",

            "Forecast",

            "Recommendation",

            "Reports",

            "Settings"

        ],


        icons=[


            "speedometer2",

            "bar-chart",

            "box",

            "people",

            "cpu",

            "graph-up",

            "stars",

            "file-earmark",

            "gear"

        ],


        default_index=0

    )



    st.divider()



    st.success(

        "🟢 System Online"

    )


    st.caption(

        "AI Engine Active"

    )


    st.caption(

        "© 2026 NexusCart AI"

    )





# ==========================================================
# HEADER
# ==========================================================


left,right = st.columns([8,2])



with left:


    st.markdown(

        """

        <h1>

        Welcome Back 👋

        </h1>

        """,

        unsafe_allow_html=True

    )


    st.caption(

        "AI Powered Retail Intelligence Platform"

    )



with right:


    st.metric(

        "Today",

        datetime.now().strftime(

            "%d %b %Y"

        )

    )



st.write("")



# ==========================================================
# KPI CARDS
# ==========================================================


c1,c2,c3,c4 = st.columns(4)



with c1:


    st.metric(

        "💰 Revenue",

        "₹12,54,320",

        "+12.5%"

    )



with c2:


    st.metric(

        "📦 Orders",

        "8452",

        "+8.2%"

    )



with c3:


    st.metric(

        "👥 Customers",

        "3245",

        "+5.4%"

    )


with c4:


    st.metric(

        "📈 Profit",

        "₹4,32,510",

        "+15%"

    )



st.divider()



# ==========================================================
# DASHBOARD TITLE
# ==========================================================


if selected == "Dashboard":


    st.subheader(

        "📊 Executive Dashboard"

    )


    st.info(

        "Dashboard analytics will be added in Part 2."

    )
    # ==========================================================
# PART 2 : DASHBOARD ANALYTICS
# ==========================================================


if selected == "Dashboard":


    # ------------------------------------------------------
    # SALES ANALYTICS + DONUT
    # ------------------------------------------------------


    left_chart, right_chart = st.columns([3,1])



    with left_chart:


        sales_chart = go.Figure()



        sales_chart.add_trace(

            go.Scatter(

                x=df["Month"],

                y=df["Sales"],

                mode="lines+markers",

                name="Revenue",

                line=dict(

                    width=4

                ),

                marker=dict(

                    size=8

                )

            )

        )



        sales_chart.add_trace(

            go.Scatter(

                x=df["Month"],

                y=df["Orders"]*200,

                mode="lines",

                name="Orders",

                line=dict(

                    width=3,

                    dash="dot"

                )

            )

        )



        sales_chart.update_layout(

            title="📈 Sales Performance",

            height=400,

            template="plotly_white"

        )



        st.plotly_chart(

            sales_chart,

            use_container_width=True

        )





    # ------------------------------------------------------
    # DONUT CHART
    # ------------------------------------------------------


    with right_chart:



        revenue_source = pd.DataFrame({

            "Source":[

                "Online",

                "Offline",

                "Wholesale",

                "Other"

            ],


            "Value":[

                45,

                30,

                15,

                10

            ]

        })



        donut = px.pie(

            revenue_source,

            names="Source",

            values="Value",

            hole=0.6,

            title="Revenue Source"

        )



        st.plotly_chart(

            donut,

            use_container_width=True

        )





    st.divider()



    # ------------------------------------------------------
    # CATEGORY PERFORMANCE
    # ------------------------------------------------------


    st.subheader(

        "🏆 Top Categories"

    )



    category_df = pd.DataFrame({


        "Category":[

            "Electronics",

            "Fashion",

            "Furniture",

            "Beauty",

            "Groceries"

        ],


        "Sales":[

            450000,

            320000,

            270000,

            180000,

            150000

        ]

    })



    category_chart = px.bar(

        category_df,

        x="Category",

        y="Sales",

        text="Sales",

        title="Category Revenue"

    )



    st.plotly_chart(

        category_chart,

        use_container_width=True

    )





    # ------------------------------------------------------
    # SMALL KPI
    # ------------------------------------------------------


    st.write("")



    a,b,c,d = st.columns(4)



    with a:


        st.success(

            "⭐ Best Seller"

        )


        st.metric(

            "Laptop",

            "1245 Sold"

        )



    with b:


        st.info(

            "🛒 Avg Basket"

        )


        st.metric(

            "₹1540",

            "+8%"

        )



    with c:


        st.warning(

            "👥 Returning"

        )


        st.metric(

            "68%",

            "+4%"

        )



    with d:


        st.error(

            "📦 Pending"

        )


        st.metric(

            "53",

            "-9%"

        )





    st.divider()



    # ------------------------------------------------------
    # RECENT ORDERS
    # ------------------------------------------------------


    st.subheader(

        "📦 Recent Orders"

    )



    orders = pd.DataFrame({


        "Order ID":[

            "#1001",

            "#1002",

            "#1003",

            "#1004",

            "#1005"

        ],


        "Customer":[

            "Rahul",

            "Priya",

            "Amit",

            "Sneha",

            "Rohan"

        ],


        "Category":[

            "Electronics",

            "Fashion",

            "Beauty",

            "Furniture",

            "Groceries"

        ],


        "Amount":[

            1240,

            3400,

            875,

            9250,

            1420

        ],


        "Status":[

            "Completed",

            "Pending",

            "Completed",

            "Delivered",

            "Cancelled"

        ]

    })



    st.dataframe(

        orders,

        use_container_width=True,

        hide_index=True

    )





    # ------------------------------------------------------
    # PROFIT ANALYSIS
    # ------------------------------------------------------


    st.write("")



    profit = pd.DataFrame({

        "Month":months,

        "Profit":np.random.randint(

            5000,

            25000,

            12

        )

    })



    profit_chart = px.area(

        profit,

        x="Month",

        y="Profit",

        title="Monthly Profit Growth"

    )



    st.plotly_chart(

        profit_chart,

        use_container_width=True

    )
    # ==========================================================
# PART 3 : SALES + PRODUCTS + CUSTOMER AI
# ==========================================================


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



# ==========================================================
# SALES PAGE
# ==========================================================


if selected == "Sales":


    st.subheader(
        "📊 Sales Intelligence"
    )


    sales_data = pd.DataFrame({

        "Category":[
            "Electronics",
            "Fashion",
            "Beauty",
            "Furniture",
            "Groceries"
        ],

        "Revenue":[
            450000,
            320000,
            180000,
            270000,
            150000
        ],

        "Orders":[
            1200,
            950,
            600,
            450,
            800
        ]

    })


    col1,col2 = st.columns(2)



    with col1:


        fig = px.bar(

            sales_data,

            x="Category",

            y="Revenue",

            title="Revenue By Category",

            text="Revenue"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



    with col2:


        fig = px.pie(

            sales_data,

            names="Category",

            values="Revenue",

            hole=0.5,

            title="Revenue Distribution"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



    st.subheader(

        "📈 Sales Growth"

    )


    growth = pd.DataFrame({

        "Month":months,

        "Revenue":np.random.randint(

            30000,

            90000,

            12

        )

    })


    fig = px.line(

        growth,

        x="Month",

        y="Revenue",

        markers=True,

        title="Monthly Revenue"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )





# ==========================================================
# PRODUCTS PAGE
# ==========================================================


if selected == "Products":


    st.subheader(

        "📦 Product Analytics"

    )


    products = pd.DataFrame({

        "Product":[

            "Laptop",

            "Mobile",

            "Shoes",

            "Watch",

            "Furniture"

        ],

        "Sales":[

            1250,

            2100,

            950,

            780,

            430

        ],

        "Stock":[

            120,

            250,

            80,

            60,

            40

        ]

    })



    fig = px.bar(

        products,

        x="Product",

        y="Sales",

        title="Top Selling Products",

        text="Sales"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    st.subheader(

        "Inventory Status"

    )


    st.dataframe(

        products,

        use_container_width=True,

        hide_index=True

    )





# ==========================================================
# CUSTOMERS AI SEGMENTATION
# ==========================================================


if selected == "Customers":


    st.subheader(

        "🤖 AI Customer Segmentation"

    )


    st.write(

        """
        KMeans Machine Learning groups customers
        based on purchasing behaviour.
        """

    )


    customer_data = pd.DataFrame({

        "Age":np.random.randint(

            18,

            60,

            200

        ),

        "Purchase":np.random.randint(

            500,

            10000,

            200

        ),

        "Frequency":np.random.randint(

            1,

            20,

            200

        )

    })



    scaler = StandardScaler()



    scaled = scaler.fit_transform(

        customer_data

    )



    cluster_number = st.slider(

        "Select Customer Groups",

        2,

        6,

        3

    )



    model = KMeans(

        n_clusters=cluster_number,

        random_state=42,

        n_init=10

    )



    customer_data["Segment"] = model.fit_predict(

        scaled

    )



    st.success(

        "Customer Segmentation Completed"

    )



    fig = px.scatter(

        customer_data,

        x="Purchase",

        y="Frequency",

        color="Segment",

        title="Customer Groups"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.subheader(

        "Segment Data"

    )


    st.dataframe(

        customer_data,

        use_container_width=True

    )
    # ==========================================
# CUSTOMER FEEDBACK
# ==========================================

st.markdown("---")
st.subheader("⭐ Customer Feedback Analysis")

feedback_data = pd.DataFrame({
    "Rating": [5, 4, 5, 3, 4, 5, 2, 1, 4, 5],
    "Feedback": [
        "Excellent product quality",
        "Fast delivery",
        "Very satisfied",
        "Average experience",
        "Good customer service",
        "Highly recommended",
        "Late delivery",
        "Poor packaging",
        "Worth the price",
        "Amazing shopping experience"
    ],
    "Sentiment": [
        "Positive",
        "Positive",
        "Positive",
        "Neutral",
        "Positive",
        "Positive",
        "Negative",
        "Negative",
        "Positive",
        "Positive"
    ]
})

col1, col2 = st.columns([2, 1])

with col1:
    st.dataframe(
        feedback_data,
        use_container_width=True,
        hide_index=True
    )

with col2:
    avg_rating = feedback_data["Rating"].mean()
    st.metric(
        "Average Rating",
        f"{avg_rating:.1f} ⭐"
    )

st.markdown("### Sentiment Distribution")

sentiment_count = feedback_data["Sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Count"]

fig = px.pie(
    sentiment_count,
    values="Count",
    names="Sentiment",
    hole=0.45,
    title="Customer Sentiment"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Rating Distribution")

rating_count = feedback_data["Rating"].value_counts().sort_index().reset_index()
rating_count.columns = ["Rating", "Count"]

fig2 = px.bar(
    rating_count,
    x="Rating",
    y="Count",
    text="Count",
    title="Customer Ratings"
)

st.plotly_chart(fig2, use_container_width=True)

positive = (feedback_data["Sentiment"] == "Positive").sum()
negative = (feedback_data["Sentiment"] == "Negative").sum()
neutral = (feedback_data["Sentiment"] == "Neutral").sum()

c1, c2, c3 = st.columns(3)

c1.metric("😊 Positive", positive)
c2.metric("😐 Neutral", neutral)
c3.metric("😞 Negative", negative)

st.success("AI Insight: Most customers are satisfied with product quality and delivery. Improve packaging and delivery speed to reduce negative feedback.")
    # ==========================================================
# PART 4 : AI PREDICTION + SALES FORECAST
# ==========================================================


from sklearn.linear_model import LinearRegression



# ==========================================================
# AI PREDICTION PAGE
# ==========================================================
if selected == "AI Prediction":

    st.title("🤖 NexusCart AI Purchase Prediction")

    st.write(
        "Predict customer purchase amount using Machine Learning"
    )


    transaction_id = st.text_input(
        "Transaction ID",
        "T1001"
    )

    customer_id = st.text_input(
        "Customer ID",
        "C1001"
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=25
    )

    category = st.selectbox(
        "Product Category",
        [
            "Electronics",
            "Clothing",
            "Beauty",
            "Home"
        ]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    price = st.number_input(
        "Price per Unit",
        min_value=1.0,
        value=500.0
    )

    age_group = st.selectbox(
        "Age Group",
        ["Young", "Adult", "Senior"]
    )

    order_size = st.selectbox(
        "Order Size",
        ["Small", "Medium", "Large"]
    )

    revenue_category = st.selectbox(
        "Revenue Category",
        ["Low", "Medium", "High"]
    )

    customer_type = st.selectbox(
        "Customer Type",
        ["New", "Returning"]
    )

if st.button("Predict Purchase Amount"):

    input_data = pd.DataFrame(
        [[
            1001,   # Transaction ID
            20260101, # Date
            1001,   # Customer ID
            1,      # Gender (Male=1)
            age,
            1,      # Product Category
            quantity,
            price,
            1,      # Age Group
            1,      # Order Size
            1,      # Revenue Category
            1       # Customer Type
        ]],
        columns=[
            "Transaction ID",
            "Date",
            "Customer ID",
            "Gender",
            "Age",
            "Product Category",
            "Quantity",
            "Price per Unit",
            "Age Group",
            "Order Size",
            "Revenue Category",
            "Customer Type"
        ]
    )


    prediction = model.predict(input_data)


    st.success(
        f"Predicted Purchase Amount: ₹ {prediction[0]:,.2f}"
    )
    
         


# ==========================================================
# FORECAST PAGE
# ==========================================================


if selected == "Forecast":


    st.subheader(

        "📈 AI Sales Forecast"

    )


    st.write(

        """
        Predict future sales using Linear Regression.
        """

    )



    forecast_data = pd.DataFrame({

        "Month_Number":range(1,13),


        "Sales":np.random.randint(

            30000,

            90000,

            12

        )

    })



    X = forecast_data[

        ["Month_Number"]

    ]


    y = forecast_data["Sales"]



    forecast_model = LinearRegression()



    forecast_model.fit(

        X,

        y

    )



    next_month = 13



    future_sales = forecast_model.predict(

        [[next_month]]

    )[0]



    col1,col2 = st.columns(2)



    with col1:


        st.metric(

            "Next Month Prediction",

            f"₹ {future_sales:,.0f}"

        )



    with col2:


        st.metric(

            "Average Sales",

            f"₹ {y.mean():,.0f}"

        )




    st.divider()



    fig = px.line(

        forecast_data,

        x="Month_Number",

        y="Sales",

        markers=True,

        title="Sales Forecast Trend"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.subheader(

        "Forecast Table"

    )


    st.dataframe(

        forecast_data,

        use_container_width=True

    )
    # ==========================================================
# PART 5 : RECOMMENDATION + REPORTS + SETTINGS + FOOTER
# ==========================================================



# ==========================================================
# RECOMMENDATION PAGE
# ==========================================================


if selected == "Recommendation":


    st.subheader(

        "⭐ AI Recommendation Engine"

    )


    st.write(

        """
        AI recommends popular products based on
        sales performance.
        """

    )


    recommendation_data = pd.DataFrame({


        "Product":[

            "Laptop",

            "Smartphone",

            "Headphone",

            "Shoes",

            "Smart Watch",

            "Furniture"

        ],


        "Demand":[

            95,

            90,

            85,

            70,

            65,

            50

        ]

    })



    top_product = recommendation_data.loc[

        recommendation_data["Demand"].idxmax(),

        "Product"

    ]



    st.success(

        f"🔥 Recommended Product : {top_product}"

    )



    fig = px.bar(

        recommendation_data,

        x="Product",

        y="Demand",

        title="Product Demand Analysis",

        text="Demand"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.dataframe(

        recommendation_data,

        use_container_width=True,

        hide_index=True

    )






# ==========================================================
# REPORTS PAGE
# ==========================================================


if selected == "Reports":


    st.subheader(

        "📑 Business Reports"

    )


    report_data = pd.DataFrame({


        "Metric":[

            "Total Revenue",

            "Total Orders",

            "Customers",

            "Profit"

        ],


        "Value":[

            "₹12,54,320",

            "8452",

            "3245",

            "₹4,32,510"

        ]

    })



    st.dataframe(

        report_data,

        use_container_width=True,

        hide_index=True

    )



    csv = report_data.to_csv(

        index=False

    )



    st.download_button(

        label="📥 Download Report",

        data=csv,

        file_name="NexusCart_Report.csv",

        mime="text/csv"

    )





# ==========================================================
# SETTINGS PAGE
# ==========================================================


if selected == "Settings":


    st.subheader(

        "⚙️ System Settings"

    )


    st.toggle(

        "Enable AI Suggestions",

        value=True

    )


    st.toggle(

        "Enable Forecast Model",

        value=True

    )


    st.toggle(

        "Enable Customer Analytics",

        value=True

    )



    st.info(

        """
        NexusCart AI Pro System

        Version : 1.0

        Status : Active

        AI Engine : Running

        """

    )





# ==========================================================
# FOOTER
# ==========================================================


st.divider()



st.markdown(

    """

    <center>

    🛒 <b>NexusCart AI Pro</b>

    <br>

    AI Powered Retail Intelligence Platform

    <br>

    Built with Python • Streamlit • Machine Learning

    <br>

    © 2026 All Rights Reserved

    </center>

    """,

    unsafe_allow_html=True

)