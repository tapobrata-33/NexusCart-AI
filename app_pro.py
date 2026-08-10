
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# NEXUSCART AI PRO — COMPLETE SINGLE-FILE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="NexusCart AI Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------- CSS -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1020;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11182d 0%, #0b1020 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] * {
    color: #e8edf7;
}

.hero {
    padding: 24px 28px;
    border-radius: 22px;
    background: linear-gradient(135deg, #151f3d, #0f172d);
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 12px 40px rgba(0,0,0,.22);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    margin: 0;
    color: #ffffff;
}

.hero-sub {
    color: #aeb9d1;
    margin-top: 7px;
    font-size: 14px;
}

.badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: rgba(99,102,241,.16);
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
}

.kpi {
    padding: 19px;
    border-radius: 18px;
    background: linear-gradient(145deg, #151d35, #10172a);
    border: 1px solid rgba(255,255,255,.07);
    min-height: 128px;
    box-shadow: 0 10px 30px rgba(0,0,0,.18);
}

.kpi-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.kpi-value {
    color: white;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-delta {
    color: #34d399;
    font-size: 12px;
    margin-top: 7px;
}

.panel {
    padding: 18px;
    border-radius: 18px;
    background: #11182d;
    border: 1px solid rgba(255,255,255,.07);
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: white;
    margin: 6px 0 14px 0;
}

.small-muted {
    color: #8f9bb3;
    font-size: 12px;
}

div[data-testid="stMetric"] {
    background: #11182d;
    padding: 15px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.07);
}

button[kind="primary"] {
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    background-color: #11182d;
}

.stDownloadButton button {
    width: 100%;
}

@media (max-width: 800px) {
    .hero-title { font-size: 25px; }
    .hero { padding: 18px; }
}
</style>
""", unsafe_allow_html=True)


# ------------------------- Helpers ----------------------------

@st.cache_data
def load_data():
    candidates = [
        "retail_sales.csv",
        "retail_sales(1).csv",
        "clean_retail_sales.csv",
        "clean_amazon.csv"
    ]

    for file in candidates:
        try:
            df = pd.read_csv(file)
            if len(df) > 0:
                return df, file
        except Exception:
            pass

    # Safe fallback so the UI can still open.
    rng = np.random.default_rng(42)
    n = 800
    dates = pd.date_range("2025-01-01", periods=365, freq="D")
    categories = ["Electronics", "Clothing", "Beauty", "Home", "Sports"]
    genders = ["Male", "Female"]
    customer_types = ["New", "Returning", "VIP"]

    df = pd.DataFrame({
        "Transaction ID": [f"T{i:05d}" for i in range(1, n + 1)],
        "Date": rng.choice(dates, n),
        "Customer ID": [f"C{rng.integers(1, 300):04d}" for _ in range(n)],
        "Gender": rng.choice(genders, n),
        "Age": rng.integers(18, 65, n),
        "Product Category": rng.choice(categories, n),
        "Quantity": rng.integers(1, 6, n),
        "Price per Unit": rng.uniform(50, 2500, n).round(2),
        "Customer Type": rng.choice(customer_types, n, p=[.45, .4, .15])
    })
    df["Total Amount"] = (df["Quantity"] * df["Price per Unit"]).round(2)
    return df, "built-in demo data"


def prepare_data(df):
    df = df.copy()

    # Normalize common column names
    aliases = {
        "Total Sales": "Total Amount",
        "Sales": "Total Amount",
        "Revenue": "Total Amount",
        "Price": "Price per Unit",
        "Product": "Product Category"
    }
    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df.rename(columns={old: new}, inplace=True)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        df["Date"] = pd.Timestamp.today()

    for col in ["Age", "Quantity", "Price per Unit", "Total Amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Total Amount" not in df.columns:
        if {"Quantity", "Price per Unit"}.issubset(df.columns):
            df["Total Amount"] = df["Quantity"] * df["Price per Unit"]
        else:
            df["Total Amount"] = 0.0

    if "Quantity" not in df.columns:
        df["Quantity"] = 1

    if "Price per Unit" not in df.columns:
        df["Price per Unit"] = df["Total Amount"] / df["Quantity"].replace(0, 1)

    if "Gender" not in df.columns:
        df["Gender"] = "Unknown"
    if "Product Category" not in df.columns:
        df["Product Category"] = "Unknown"
    if "Customer Type" not in df.columns:
        df["Customer Type"] = "Unknown"
    if "Customer ID" not in df.columns:
        df["Customer ID"] = np.arange(len(df)).astype(str)

    if "Age" not in df.columns:
        df["Age"] = 30

    df["Age Group"] = pd.cut(
        df["Age"],
        bins=[0, 17, 25, 35, 50, 100],
        labels=["<18", "18-25", "26-35", "36-50", "50+"],
        include_lowest=True
    ).astype(str)

    df["Order Size"] = pd.cut(
        df["Quantity"],
        bins=[-1, 1, 3, 6, np.inf],
        labels=["Small", "Medium", "Large", "Bulk"]
    ).astype(str)

    df["Revenue Category"] = pd.cut(
        df["Total Amount"],
        bins=[-np.inf, 500, 2000, 5000, np.inf],
        labels=["Low", "Medium", "High", "Premium"]
    ).astype(str)

    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Day"] = df["Date"].dt.date
    df["Total Amount"] = df["Total Amount"].fillna(0)
    df["Quantity"] = df["Quantity"].fillna(0)

    return df


def money(x):
    if x is None or pd.isna(x):
        return "₹0"
    x = float(x)
    if abs(x) >= 1e7:
        return f"₹{x/1e7:.2f}Cr"
    if abs(x) >= 1e5:
        return f"₹{x/1e5:.2f}L"
    if abs(x) >= 1e3:
        return f"₹{x/1e3:.1f}K"
    return f"₹{x:,.0f}"


def make_kpi(label, value, delta="Live dataset"):
    return f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">● {delta}</div>
    </div>
    """


def chart_layout(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe4f0"),
        margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.06)")
    return fig


# ---------------------------- Data ----------------------------

raw_df, source_file = load_data()
df = prepare_data(raw_df)

# --------------------------- Sidebar --------------------------

with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 18px 0;">
        <div style="font-size:25px;font-weight:800;color:white;">🛒 NexusCart</div>
        <div style="color:#8f9bb3;font-size:12px;">AI Retail Intelligence Pro</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📊 Sales Analysis",
            "👥 Customer AI",
            "⚠️ Churn Prediction",
            "🤖 AI Assistant",
            "📈 Sales Forecast",
            "🧠 AI Prediction",
            "🎯 Recommendation",
            "📦 Data Explorer",
            "⚙️ Model Center"
        ]
    )

    st.divider()

    st.caption(f"Data source: {source_file}")
    st.caption(f"Rows: {len(df):,}")
    st.caption("NexusCart AI Pro • 2026")


# -------------------------- Filters ---------------------------

with st.expander("🔎 Global Filters", expanded=False):
    f1, f2, f3, f4 = st.columns(4)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    with f1:
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    with f2:
        cats = ["All"] + sorted(df["Product Category"].dropna().astype(str).unique().tolist())
        selected_cat = st.selectbox("Product Category", cats)

    with f3:
        genders = ["All"] + sorted(df["Gender"].dropna().astype(str).unique().tolist())
        selected_gender = st.selectbox("Gender", genders)

    with f4:
        ctypes = ["All"] + sorted(df["Customer Type"].dropna().astype(str).unique().tolist())
        selected_type = st.selectbox("Customer Type", ctypes)


filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        (filtered["Date"].dt.date >= date_range[0]) &
        (filtered["Date"].dt.date <= date_range[1])
    ]

if selected_cat != "All":
    filtered = filtered[filtered["Product Category"].astype(str) == selected_cat]

if selected_gender != "All":
    filtered = filtered[filtered["Gender"].astype(str) == selected_gender]

if selected_type != "All":
    filtered = filtered[filtered["Customer Type"].astype(str) == selected_type]


# ========================== DASHBOARD =========================

if menu == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="badge">AI-POWERED RETAIL COMMAND CENTER</div>
        <div class="hero-title">NexusCart AI Pro</div>
        <div class="hero-sub">
            Real-time sales intelligence, customer analytics, forecasting,
            prediction and recommendation in one dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

    revenue = filtered["Total Amount"].sum()
    orders = len(filtered)
    customers = filtered["Customer ID"].nunique()
    avg_order = revenue / orders if orders else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(make_kpi("Total Revenue", money(revenue), "Filtered"), unsafe_allow_html=True)
    with k2:
        st.markdown(make_kpi("Total Orders", f"{orders:,}", "Transactions"), unsafe_allow_html=True)
    with k3:
        st.markdown(make_kpi("Customers", f"{customers:,}", "Unique"), unsafe_allow_html=True)
    with k4:
        st.markdown(make_kpi("Average Order", money(avg_order), "Per order"), unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns([1.6, 1])

    with c1:
        st.markdown('<div class="section-title">Revenue Trend</div>', unsafe_allow_html=True)
        trend = filtered.groupby("Month", as_index=False)["Total Amount"].sum()
        fig = px.area(trend, x="Month", y="Total Amount", title="")
        fig.update_traces(line_width=3)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
        cat = filtered.groupby("Product Category", as_index=False)["Total Amount"].sum()
        fig = px.pie(cat, names="Product Category", values="Total Amount", hole=.58)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-title">Gender Performance</div>', unsafe_allow_html=True)
        g = filtered.groupby("Gender", as_index=False)["Total Amount"].sum()
        fig = px.bar(g, x="Gender", y="Total Amount", text_auto=".2s")
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)

    with c4:
        st.markdown('<div class="section-title">Order Size Distribution</div>', unsafe_allow_html=True)
        o = filtered.groupby("Order Size", as_index=False)["Quantity"].sum()
        fig = px.bar(o, x="Order Size", y="Quantity", text_auto=True)
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)

    st.markdown('<div class="section-title">⚡ AI Business Snapshot</div>', unsafe_allow_html=True)

    best_cat = (
        filtered.groupby("Product Category")["Total Amount"].sum().idxmax()
        if len(filtered) else "N/A"
    )
    best_customer = (
        filtered.groupby("Customer Type")["Total Amount"].sum().idxmax()
        if len(filtered) else "N/A"
    )

    a1, a2, a3 = st.columns(3)
    a1.info(f"🏆 **Top category:** {best_cat}")
    a2.success(f"💎 **Best customer segment:** {best_customer}")
    a3.warning(f"💰 **Average order:** {money(avg_order)}")


# ======================= SALES ANALYSIS ========================

elif menu == "📊 Sales Analysis":
    st.markdown('<div class="section-title">📊 Sales Intelligence</div>', unsafe_allow_html=True)

    monthly = filtered.groupby("Month", as_index=False).agg(
        Revenue=("Total Amount", "sum"),
        Orders=("Transaction ID", "count") if "Transaction ID" in filtered.columns else ("Total Amount", "count")
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(monthly, x="Month", y="Revenue", markers=True, title="Monthly Revenue")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with c2:
        fig = px.bar(monthly, x="Month", y="Orders", title="Monthly Orders")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        category = filtered.groupby("Product Category", as_index=False).agg(
            Revenue=("Total Amount", "sum"),
            Quantity=("Quantity", "sum")
        ).sort_values("Revenue", ascending=False)

        fig = px.bar(category, x="Revenue", y="Product Category", orientation="h",
                     title="Category Revenue")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with c4:
        age = filtered.groupby("Age Group", as_index=False)["Total Amount"].sum()
        fig = px.bar(age, x="Age Group", y="Total Amount", title="Revenue by Age Group")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown('<div class="section-title">Product Performance</div>', unsafe_allow_html=True)

    product_table = filtered.groupby("Product Category").agg(
        Revenue=("Total Amount", "sum"),
        Orders=("Total Amount", "count"),
        Quantity=("Quantity", "sum"),
        Avg_Order=("Total Amount", "mean")
    ).reset_index()

    product_table["Revenue"] = product_table["Revenue"].round(2)
    product_table["Avg_Order"] = product_table["Avg_Order"].round(2)
    st.dataframe(product_table, use_container_width=True, hide_index=True)


# ======================== CUSTOMER AI ==========================

elif menu == "👥 Customer AI":
    st.markdown('<div class="section-title">👥 Customer Segmentation AI</div>', unsafe_allow_html=True)

    customer = filtered.groupby("Customer ID").agg(
        Revenue=("Total Amount", "sum"),
        Orders=("Total Amount", "count"),
        Quantity=("Quantity", "sum"),
        Avg_Order=("Total Amount", "mean")
    ).reset_index()

    if len(customer) >= 3:
        n_clusters = st.slider("Number of customer segments", 2, min(6, len(customer)), 4)

        X = customer[["Revenue", "Orders", "Quantity", "Avg_Order"]].fillna(0)
        X_scaled = StandardScaler().fit_transform(X)

        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        customer["Segment"] = km.fit_predict(X_scaled).astype(str)

        c1, c2 = st.columns(2)

        with c1:
            fig = px.scatter(
                customer,
                x="Orders",
                y="Revenue",
                size="Quantity",
                color="Segment",
                hover_data=["Customer ID", "Avg_Order"],
                title="Customer Segments"
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)

        with c2:
            seg = customer.groupby("Segment", as_index=False)["Revenue"].sum()
            fig = px.bar(seg, x="Segment", y="Revenue", text_auto=".2s",
                         title="Revenue by Segment")
            st.plotly_chart(chart_layout(fig), use_container_width=True)

        st.dataframe(customer.sort_values("Revenue", ascending=False),
                     use_container_width=True, hide_index=True)
    else:
        st.warning("Not enough customers for segmentation.")


# ======================= CHURN PREDICTION ======================

elif menu == "⚠️ Churn Prediction":
    st.markdown('<div class="section-title">⚠️ Customer Churn Intelligence</div>', unsafe_allow_html=True)

    customer = filtered.groupby("Customer ID").agg(
        Revenue=("Total Amount", "sum"),
        Orders=("Total Amount", "count"),
        Quantity=("Quantity", "sum"),
        Last_Purchase=("Date", "max")
    ).reset_index()

    reference_date = filtered["Date"].max() if len(filtered) else pd.Timestamp.today()
    customer["Recency"] = (reference_date - customer["Last_Purchase"]).dt.days.clip(lower=0)

    # Heuristic churn score: transparent and robust when no labelled churn dataset exists.
    customer["Churn Score"] = (
        customer["Recency"].rank(pct=True) * 0.60 +
        (1 - customer["Orders"].rank(pct=True)) * 0.25 +
        (1 - customer["Revenue"].rank(pct=True)) * 0.15
    ) * 100

    customer["Risk"] = pd.cut(
        customer["Churn Score"],
        bins=[-1, 35, 65, 101],
        labels=["Low", "Medium", "High"]
    )

    high = (customer["Risk"] == "High").sum()
    medium = (customer["Risk"] == "Medium").sum()

    a, b, c = st.columns(3)
    a.metric("High Risk", high)
    b.metric("Medium Risk", medium)
    c.metric("Customers", len(customer))

    fig = px.scatter(
        customer,
        x="Recency",
        y="Churn Score",
        size="Revenue",
        color="Risk",
        hover_data=["Customer ID", "Orders", "Revenue"]
    )
    st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown("### 🚨 Customers requiring attention")
    st.dataframe(
        customer.sort_values("Churn Score", ascending=False).head(50),
        use_container_width=True,
        hide_index=True
    )


# ========================= AI ASSISTANT ========================

elif menu == "🤖 AI Assistant":
    st.markdown("""
    <div class="hero">
        <div class="badge">BUSINESS COPILOT</div>
        <div class="hero-title">🤖 Nexus AI Assistant</div>
        <div class="hero-sub">Ask questions about your retail dataset.</div>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "Ask a business question",
        placeholder="Example: Which category generates the most revenue?"
    )

    if question:
        q = question.lower()

        revenue = filtered["Total Amount"].sum()
        orders = len(filtered)
        avg = revenue / orders if orders else 0

        if "top" in q and ("categor" in q or "product" in q):
            data = filtered.groupby("Product Category")["Total Amount"].sum().sort_values(ascending=False)
            if len(data):
                st.success(f"🏆 Top category is **{data.index[0]}** with revenue of **{money(data.iloc[0])}**.")

        elif "revenue" in q or "sales" in q:
            st.info(f"💰 Total filtered revenue is **{money(revenue)}** across **{orders:,} orders**.")

        elif "average" in q or "avg" in q:
            st.info(f"📦 Average order value is **{money(avg)}**.")

        elif "customer" in q and ("type" in q or "segment" in q):
            data = filtered.groupby("Customer Type")["Total Amount"].sum().sort_values(ascending=False)
            if len(data):
                st.success(f"💎 **{data.index[0]}** customers contribute the most revenue: **{money(data.iloc[0])}**.")

        elif "gender" in q:
            data = filtered.groupby("Gender")["Total Amount"].sum().sort_values(ascending=False)
            if len(data):
                st.info(f"👤 Highest-revenue gender group is **{data.index[0]}** with **{money(data.iloc[0])}**.")

        elif "quantity" in q or "units" in q:
            st.info(f"📦 Total units sold: **{filtered['Quantity'].sum():,.0f}**.")

        else:
            st.warning(
                "Try questions containing **sales, revenue, category, product, "
                "customer, segment, gender, average, quantity, or units**."
            )

    st.markdown("### 💡 Quick questions")
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("Top category"):
        data = filtered.groupby("Product Category")["Total Amount"].sum().sort_values(ascending=False)
        if len(data):
            st.success(f"{data.index[0]} — {money(data.iloc[0])}")
    if q2.button("Total revenue"):
        st.success(money(filtered["Total Amount"].sum()))
    if q3.button("Avg order"):
        st.success(money(filtered["Total Amount"].mean()))
    if q4.button("Top customer type"):
        data = filtered.groupby("Customer Type")["Total Amount"].sum().sort_values(ascending=False)
        if len(data):
            st.success(data.index[0])


# ======================== FORECASTING ==========================

elif menu == "📈 Sales Forecast":
    st.markdown('<div class="section-title">📈 AI Sales Forecast</div>', unsafe_allow_html=True)

    monthly = filtered.groupby("Month")["Total Amount"].sum().reset_index()
    monthly["MonthDate"] = pd.to_datetime(monthly["Month"] + "-01", errors="coerce")
    monthly = monthly.sort_values("MonthDate").dropna()

    if len(monthly) >= 3:
        monthly["Index"] = np.arange(len(monthly))

        model = RandomForestRegressor(
            n_estimators=250,
            random_state=42,
            max_depth=8
        )
        X = monthly[["Index"]]
        y = monthly["Total Amount"]
        model.fit(X, y)

        future_n = st.slider("Months to forecast", 1, 12, 3)
        future_idx = np.arange(len(monthly), len(monthly) + future_n)

        predictions = model.predict(pd.DataFrame({"Index": future_idx}))

        last_date = monthly["MonthDate"].max()
        future_dates = [
            last_date + pd.DateOffset(months=i)
            for i in range(1, future_n + 1)
        ]

        history = monthly[["MonthDate", "Total Amount"]].rename(
            columns={"MonthDate": "Date", "Total Amount": "Revenue"}
        )

        forecast = pd.DataFrame({
            "Date": future_dates,
            "Revenue": predictions
        })
        forecast["Type"] = "Forecast"
        history["Type"] = "Actual"

        combined = pd.concat([history.assign(Type="Actual"), forecast], ignore_index=True)

        fig = px.line(
            combined,
            x="Date",
            y="Revenue",
            color="Type",
            markers=True,
            title="Actual vs Forecast"
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

        st.markdown("### 🔮 Forecast values")
        forecast["Revenue"] = forecast["Revenue"].round(2)
        st.dataframe(forecast, use_container_width=True, hide_index=True)
    else:
        st.warning("At least 3 months of data are needed for forecasting.")


# ======================== AI PREDICTION ========================

elif menu == "🧠 AI Prediction":
    st.markdown('<div class="section-title">🧠 Purchase Amount Predictor</div>', unsafe_allow_html=True)

    st.info(
        "This predictor uses only numeric features, so it avoids the previous "
        "feature-name/categorical encoding errors."
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        age = st.number_input("Customer Age", 10, 100, 30)

    with p2:
        quantity = st.number_input("Quantity", 1, 100, 2)

    with p3:
        price = st.number_input("Price per Unit (₹)", 1.0, 100000.0, 1000.0)

    if st.button("🚀 Predict Purchase Amount", type="primary"):
        # Train a clean model directly from the current dataset.
        train_df = filtered[["Age", "Quantity", "Price per Unit", "Total Amount"]].dropna()

        if len(train_df) >= 10:
            X = train_df[["Age", "Quantity", "Price per Unit"]]
            y = train_df["Total Amount"]

            model = RandomForestRegressor(
                n_estimators=250,
                random_state=42,
                max_depth=10
            )
            model.fit(X, y)

            prediction = model.predict(
                pd.DataFrame({
                    "Age": [age],
                    "Quantity": [quantity],
                    "Price per Unit": [price]
                })
            )[0]

            st.success(f"### Predicted Purchase Amount: {money(prediction)}")

            actual_estimate = quantity * price
            st.caption(
                f"Reference basket value: {money(actual_estimate)} • "
                f"Prediction based on learned retail patterns."
            )
        else:
            st.warning("Not enough clean records to train the prediction model.")


# ======================= RECOMMENDATION ========================

elif menu == "🎯 Recommendation":
    st.markdown('<div class="section-title">🎯 Smart Product Recommendation</div>', unsafe_allow_html=True)

    category_sales = filtered.groupby("Product Category").agg(
        Revenue=("Total Amount", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Total Amount", "count")
    ).reset_index()

    category_sales["Score"] = (
        category_sales["Revenue"].rank(pct=True) * .55 +
        category_sales["Quantity"].rank(pct=True) * .30 +
        category_sales["Orders"].rank(pct=True) * .15
    )

    category_sales = category_sales.sort_values("Score", ascending=False)

    if len(category_sales):
        top = category_sales.head(5)

        st.markdown("### ⭐ Top 5 recommended categories")
        cols = st.columns(min(5, len(top)))

        for i, (_, row) in enumerate(top.iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="kpi">
                        <div class="kpi-label">Recommendation #{i+1}</div>
                        <div class="kpi-value" style="font-size:18px;">
                            {row['Product Category']}
                        </div>
                        <div class="kpi-delta">
                            Revenue {money(row['Revenue'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        fig = px.bar(
            top.sort_values("Score"),
            x="Score",
            y="Product Category",
            orientation="h",
            title="Recommendation Score"
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

        st.dataframe(category_sales, use_container_width=True, hide_index=True)


# ======================== DATA EXPLORER =========================

elif menu == "📦 Data Explorer":
    st.markdown('<div class="section-title">📦 Data Explorer</div>', unsafe_allow_html=True)

    st.write(f"Showing **{len(filtered):,}** filtered records.")

    search = st.text_input("Search table", placeholder="Type a customer ID, category, transaction ID...")

    display_df = filtered.copy()

    if search:
        mask = display_df.astype(str).apply(
            lambda col: col.str.contains(search, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]

    st.dataframe(display_df, use_container_width=True, height=550, hide_index=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download filtered CSV",
        data=csv,
        file_name="nexuscart_filtered_data.csv",
        mime="text/csv"
    )


# ========================= MODEL CENTER =========================

elif menu == "⚙️ Model Center":
    st.markdown('<div class="section-title">⚙️ AI Model Center</div>', unsafe_allow_html=True)

    st.write("NexusCart AI models are trained from the currently filtered dataset.")

    # Regression evaluation
    reg_df = filtered[["Age", "Quantity", "Price per Unit", "Total Amount"]].dropna()

    if len(reg_df) >= 20:
        X = reg_df[["Age", "Quantity", "Price per Unit"]]
        y = reg_df["Total Amount"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=.2, random_state=42
        )

        reg = RandomForestRegressor(
            n_estimators=250,
            random_state=42,
            max_depth=10
        )
        reg.fit(X_train, y_train)
        pred = reg.predict(X_test)

        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)

        a, b, c = st.columns(3)
        a.metric("R² Score", f"{r2:.3f}")
        b.metric("MAE", money(mae))
        c.metric("Training Rows", f"{len(X_train):,}")

        importance = pd.DataFrame({
            "Feature": X.columns,
            "Importance": reg.feature_importances_
        }).sort_values("Importance", ascending=False)

        fig = px.bar(
            importance,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

        st.dataframe(importance, use_container_width=True, hide_index=True)
    else:
        st.warning("At least 20 rows are recommended for model evaluation.")


# --------------------------- Footer ----------------------------

st.divider()
st.caption(
    "🛒 NexusCart AI Pro • Retail Intelligence Platform • "
    "Python + Streamlit + Plotly + Machine Learning"
)