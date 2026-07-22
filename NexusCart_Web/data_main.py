# ==========================================
# NexusCart AI - Complete Single File Project
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# ==========================================
# 1. LOAD DATA
# ==========================================

def load_data():

    print("\nLoading Dataset...")

    try:

        df = pd.read_csv(
            "../assets/retail_sales.csv"
        )

        print("Dataset Loaded Successfully")

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nColumns:")
        print(df.columns)

        return df


    except Exception as e:

        print("Dataset Error:", e)

        return None



# ==========================================
# 2. DATA CLEANING
# ==========================================

def clean_data(df):

    print("\nCleaning Data...")


    # Remove duplicates

    print(
        "Duplicate Rows:",
        df.duplicated().sum()
    )


    df = df.drop_duplicates()



    # Convert numeric columns

    for col in df.columns:


        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )


        if converted.notna().sum() > 0:

            df[col] = converted



    # Fill missing values

    for col in df.columns:


        if pd.api.types.is_numeric_dtype(df[col]):


            df[col] = df[col].fillna(
                df[col].median()
            )


        else:


            df[col] = df[col].fillna(
                "Unknown"
            )



    print("Cleaning Completed")


    return df




# ==========================================
# 3. BUSINESS ANALYSIS
# ==========================================

def business_analysis(df):


    print("\n========== BUSINESS INSIGHTS ==========")


    print(
        "Total Orders:",
        len(df)
    )


    amount_column = None


    for col in df.columns:


        if (
            "amount" in col.lower()
            or
            "sales" in col.lower()
            or
            "revenue" in col.lower()
        ):

            amount_column = col

            break



    if amount_column:


        print(
            "Total Revenue:",
            df[amount_column].sum()
        )


        print(
            "Average Order Value:",
            round(
                df[amount_column].mean(),
                2
            )
        )



    customer_column = None


    for col in df.columns:


        if "customer" in col.lower():

            customer_column = col

            break



    if customer_column:


        print(
            "Total Customers:",
            df[customer_column].nunique()
        )



    category_column = None


    for col in df.columns:


        if "category" in col.lower():

            category_column = col

            break



    if category_column and amount_column:


        print("\nTop Categories:")


        print(

            df.groupby(category_column)[amount_column]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)

        )


    print(
        "======================================"
    )





# ==========================================
# 4. VISUALIZATION
# ==========================================

def create_charts(df):


    print("\nCreating Charts...")


    os.makedirs(
        "../charts",
        exist_ok=True
    )


    category_column = None
    amount_column = None



    for col in df.columns:


        if "category" in col.lower():

            category_column = col


        if (
            "amount" in col.lower()
            or
            "sales" in col.lower()
        ):

            amount_column = col




    if category_column and amount_column:


        chart_data = (

            df.groupby(category_column)[amount_column]
            .sum()

        )


        plt.figure(
            figsize=(8,5)
        )


        chart_data.plot(
            kind="bar"
        )


        plt.title(
            "Sales By Category"
        )


        plt.xlabel(
            category_column
        )


        plt.ylabel(
            amount_column
        )


        plt.tight_layout()


        plt.savefig(
            "../charts/sales_category.png"
        )


        plt.close()



    print(
        "Charts Created"
    )





# ==========================================
# 5. AI MODEL
# ==========================================

def train_ai(df):


    print("\nTraining AI Model...")


    target = None


    for col in df.columns:


        if (
            "amount" in col.lower()
            or
            "sales" in col.lower()
        ):

            target = col

            break



    if target is None:


        print(
            "Sales column not found"
        )

        return



    numeric_data = df.select_dtypes(
        include="number"
    )



    if target not in numeric_data.columns:


        print(
            "Target not numeric"
        )

        return



    X = numeric_data.drop(
        target,
        axis=1
    )


    y = numeric_data[target]



    if X.shape[1] == 0:


        print(
            "No training features"
        )

        return



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



    score = model.score(
        X_test,
        y_test
    )


    print(
        "Model Accuracy:",
        score
    )



    joblib.dump(
        model,
        "../sales_prediction_model.pkl"
    )


    print(
        "AI Model Saved"
    )





# ==========================================
# 6. POWER BI EXPORT
# ==========================================

def export_powerbi(df):


    print(
        "\nExporting Power BI Data..."
    )


    os.makedirs(
        "../exports",
        exist_ok=True
    )


    df.to_csv(

        "../exports/nexuscart_powerbi.csv",

        index=False

    )


    print(
        "Power BI File Created"
    )





# ==========================================
# MAIN FUNCTION
# ==========================================

def main():


    print("""
==================================
        NexusCart AI Started
==================================
""")


    df = load_data()


    if df is None:

        return



    df = clean_data(df)



    business_analysis(df)



    create_charts(df)



    train_ai(df)



    export_powerbi(df)



    print("""
==================================
       NexusCart AI Completed
==================================
""")





if __name__ == "__main__":

    main()