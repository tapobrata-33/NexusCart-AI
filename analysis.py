import mysql.connector
import pandas as pd


# ==============================
# CONNECT MYSQL DATABASE
# ==============================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kanu@2006",
    database="nexuscart"
)

print("Database Connected Successfully")


# ==============================
# LOAD DATA FROM MYSQL
# ==============================

query = "SELECT * FROM retail_sales"

df = pd.read_sql(
    query,
    connection
)

print("Data Loaded Successfully")


# ==============================
# BASIC DATA CHECK
# ==============================

print("\nFirst 5 Rows:")
print(df.head())


print("\nDataset Shape:")
print(df.shape)


print("\nColumn Names:")
print(df.columns)


print("\nDataset Information:")
df.info()


print("\nMissing Values:")
print(df.isnull().sum())


print("\nStatistical Summary:")
print(df.describe())


# ==============================
# DATA CLEANING
# ==============================

# Fix column name encoding problem

df.columns = df.columns.str.replace(
    'ï»¿',
    ''
)


# Convert Date column

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)


print("\nData Cleaning Completed")


# Check cleaned data

print("\nCleaned Columns:")
print(df.columns)



# ==============================
# BUSINESS ANALYSIS
# ==============================


# Total Revenue

total_sales = df["Total Amount"].sum()

print("\nTotal Revenue:")
print(total_sales)



# Average Order Value

average_order = df["Total Amount"].mean()

print("\nAverage Order Value:")
print(average_order)



# Category Wise Sales

category_sales = df.groupby(
    "Product Category"
)["Total Amount"].sum()


print("\nCategory Wise Sales:")
print(category_sales)



# Customer Type Analysis

customer_analysis = df.groupby(
    "Customer Type"
)["Total Amount"].sum()


print("\nCustomer Type Analysis:")
print(customer_analysis)



# Gender Wise Sales

gender_sales = df.groupby(
    "Gender"
)["Total Amount"].sum()


print("\nGender Wise Sales:")
print(gender_sales)



# Age Group Analysis

age_analysis = df.groupby(
    "Age Group"
)["Total Amount"].sum()


print("\nAge Group Analysis:")
print(age_analysis)


# ==============================
# CLOSE CONNECTION
# ==============================

connection.close()

print("\nMySQL Connection Closed")
# ==================================
# STEP 7: PROFESSIONAL DATA VISUALIZATION
# ==================================

import matplotlib.pyplot as plt
import seaborn as sns


# Category Wise Revenue Chart

category_sales = df.groupby(
    "Product Category"
)["Total Amount"].sum()


plt.figure(figsize=(8,5))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values
)

plt.title(
    "Revenue by Product Category"
)

plt.xlabel(
    "Product Category"
)

plt.ylabel(
    "Total Revenue"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()



# Customer Type Revenue Chart

customer_sales = df.groupby(
    "Customer Type"
)["Total Amount"].sum()


plt.figure(figsize=(7,7))

plt.pie(
    customer_sales.values,
    labels=customer_sales.index,
    autopct="%1.1f%%"
)

plt.title(
    "Revenue Contribution by Customer Type"
)

plt.show()



# Gender Sales Chart

gender_sales = df.groupby(
    "Gender"
)["Total Amount"].sum()


plt.figure(figsize=(7,5))

sns.barplot(
    x=gender_sales.index,
    y=gender_sales.values
)

plt.title(
    "Sales by Gender"
)

plt.xlabel(
    "Gender"
)

plt.ylabel(
    "Revenue"
)

plt.show()



# Age Group Sales Chart

age_sales = df.groupby(
    "Age Group"
)["Total Amount"].sum()


plt.figure(figsize=(8,5))

sns.barplot(
    x=age_sales.index,
    y=age_sales.values
)

plt.title(
    "Customer Spending by Age Group"
)

plt.xlabel(
    "Age Group"
)

plt.ylabel(
    "Revenue"
)

plt.show()
# ==================================
# STEP 8: AI SALES PREDICTION MODEL
# ==================================

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


# Select Features

X = df[
[
    "Age",
    "Quantity",
    "Price per Unit"
]
]


# Target Variable

y = df[
    "Total Amount"
]


# Split Data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Data Split Completed")


# Create AI Model

model = LinearRegression()


# Train Model

model.fit(
    X_train,
    y_train
)


print("AI Model Training Completed")


# Prediction

prediction = model.predict(
    X_test
)


# Model Evaluation

accuracy = r2_score(
    y_test,
    prediction
)


error = mean_absolute_error(
    y_test,
    prediction
)


print("\nModel Accuracy:")
print(accuracy*100,"%")

print("\nAverage Prediction Error:")
print(error)



# ==================================
# TEST NEW SALES PREDICTION
# ==================================

new_customer = [[35, 3, 500]]


future_sales = model.predict(
    new_customer
)


print("\nPredicted Sales:")
print(future_sales[0])
# ==================================
# STEP 9: EXPORT AI RESULTS FOR POWER BI
# ==================================

# Create prediction dataframe

results = pd.DataFrame({

    "Actual Sales": y_test.values,

    "Predicted Sales": prediction

})


# Calculate difference

results["Difference"] = (
    results["Actual Sales"] -
    results["Predicted Sales"]
)


# Export to Excel

results.to_excel(
    "NexusCart_AI_Predictions.xlsx",
    index=False
)


print("\nAI Prediction File Created Successfully")

print(results.head())
# ==========================================
# NEXUSCART AI - COMPLETE ANALYTICS PIPELINE
# ==========================================

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


# ==========================================
# 1. CONNECT MYSQL DATABASE
# ==========================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kanu@2006",
    database="nexuscart"
)

print("Database Connected Successfully")


# ==========================================
# 2. LOAD DATA
# ==========================================

query = "SELECT * FROM retail_sales"

df = pd.read_sql(
    query,
    connection
)

print("Data Loaded Successfully")


# ==========================================
# 3. DATA CLEANING
# ==========================================

# Remove unwanted character

df.columns = df.columns.str.replace(
    "ï»¿",
    "",
    regex=False
)


# Convert Date

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)


print("\nCleaning Completed")


# ==========================================
# 4. KPI CALCULATION
# ==========================================

total_revenue = df["Total Amount"].sum()

total_orders = df["Transaction ID"].count()

total_customers = df["Customer ID"].nunique()

average_order_value = df["Total Amount"].mean()


print("\n========== KPI ==========")

print("Total Revenue:", total_revenue)

print("Total Orders:", total_orders)

print("Total Customers:", total_customers)

print("Average Order Value:", average_order_value)



# ==========================================
# 5. BUSINESS ANALYSIS
# ==========================================


category_sales = df.groupby(
    "Product Category"
)["Total Amount"].sum()


customer_sales = df.groupby(
    "Customer Type"
)["Total Amount"].sum()


gender_sales = df.groupby(
    "Gender"
)["Total Amount"].sum()


age_sales = df.groupby(
    "Age Group"
)["Total Amount"].sum()



# ==========================================
# 6. CREATE CHARTS
# ==========================================


plt.figure(figsize=(8,5))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values
)

plt.title(
    "Revenue By Product Category"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "category_revenue.png"
)

plt.show()



plt.figure(figsize=(7,5))

sns.barplot(
    x=gender_sales.index,
    y=gender_sales.values
)

plt.title(
    "Revenue By Gender"
)

plt.savefig(
    "gender_revenue.png"
)

plt.show()



# ==========================================
# 7. AI SALES PREDICTION
# ==========================================


X = df[
[
    "Age",
    "Quantity",
    "Price per Unit"
]
]


y = df[
"Total Amount"
]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = LinearRegression()


model.fit(
    X_train,
    y_train
)


prediction = model.predict(
    X_test
)


accuracy = r2_score(
    y_test,
    prediction
)


error = mean_absolute_error(
    y_test,
    prediction
)



print("\n========== AI MODEL ==========")

print(
    "Model Accuracy:",
    accuracy*100,
    "%"
)

print(
    "Prediction Error:",
    error
)



# ==========================================
# 8. EXPORT POWER BI FILE
# ==========================================


dashboard_data = pd.DataFrame({

    "Actual Sales":
    y_test.values,

    "Predicted Sales":
    prediction

})


dashboard_data["Difference"] = (

dashboard_data["Actual Sales"]

-

dashboard_data["Predicted Sales"]

)



dashboard_data.to_csv(
    "NexusCart_AI_Predictions.csv",
    index=False
)



# Export KPI

kpi = pd.DataFrame({

"Metric":
[
"Total Revenue",
"Total Orders",
"Total Customers",
"Average Order Value"
],


"Value":
[
total_revenue,
total_orders,
total_customers,
average_order_value
]

})


kpi.to_csv(
"NexusCart_KPI.csv",
index=False
)



print("\n================================")

print("POWER BI FILES CREATED SUCCESSFULLY")

print("1. NexusCart_AI_Predictions.csv")

print("2. NexusCart_KPI.csv")

print("================================")
import joblib

joblib.dump(
    model,
    "sales_prediction_model.pkl"
)

print("Model Saved Successfully")
from flask import Flask, render_template, request
import joblib
import numpy as np


# Create Flask App
app = Flask(__name__)


# Load AI Model
model = joblib.load("sales_prediction_model.pkl")


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():

    # Get values from website
    quantity = float(request.form["quantity"])
    price = float(request.form["price"])

    # Prepare data for AI model
    input_data = np.array([[quantity, price]])

    # Prediction
    prediction = model.predict(input_data)

    result = round(prediction[0], 2)


    return render_template(
        "index.html",
        prediction=result
    )


# Run Website
if __name__ == "__main__":
    app.run(debug=True)