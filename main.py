from load_data import load_data

from data_cleaning import clean_data

from business_analysis import business_report

from visualization import category_sales_chart

from ai_model import train_ai

from export_powerbi import export_kpi



print("==============================")

print("      NEXUS AI STARTED")

print("==============================")


# Load Data

df = load_data()


print("Data Loaded")



# Cleaning

df = clean_data(df)


print("Data Cleaned")



# Business Analysis

report = business_report(df)



# Chart

category_sales_chart(df)



# AI

model = train_ai(df)



# Export

export_kpi(report)



print("==============================")

print(" NEXUS AI COMPLETED ")

print("==============================")