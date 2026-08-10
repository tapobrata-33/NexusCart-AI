# ==========================================================
# NEXUS CART AI
# REAL MACHINE LEARNING MODEL TRAINING
# ==========================================================


import pandas as pd
import numpy as np

import joblib


from sklearn.model_selection import train_test_split


from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder


from sklearn.ensemble import RandomForestRegressor


from sklearn.metrics import (

    r2_score,

    mean_absolute_error,

    mean_squared_error

)



# ==========================================================
# LOAD DATA
# ==========================================================


print("Loading Dataset...")


df = pd.read_csv(

    "retail_sales.csv"

)



print(df.head())



# ==========================================================
# DATA CLEANING
# ==========================================================


df.dropna(

    inplace=True

)



# ==========================================================
# DEFINE FEATURES AND TARGET
# ==========================================================



X = df.drop(

    "Total Amount",

    axis=1

)



y = df["Total Amount"]





# ==========================================================
# REMOVE ID / DATE COLUMNS
# ==========================================================


X = X.drop(

    columns=[

        "Transaction ID",

        "Customer ID",

        "Date"

    ],

    errors="ignore"

)





# ==========================================================
# FIND DATA TYPES
# ==========================================================



categorical_features = X.select_dtypes(

    include=["object"]

).columns



numeric_features = X.select_dtypes(

    exclude=["object"]

).columns





print(

    "Categorical Columns:",

    list(categorical_features)

)



print(

    "Numeric Columns:",

    list(numeric_features)

)






# ==========================================================
# PREPROCESSING
# ==========================================================


preprocessor = ColumnTransformer(

    transformers=[


        (

            "categorical",

            OneHotEncoder(

                handle_unknown="ignore"

            ),

            categorical_features

        )



    ],


    remainder="passthrough"

)





# ==========================================================
# MACHINE LEARNING MODEL
# ==========================================================


rf_model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)






# ==========================================================
# COMPLETE ML PIPELINE
# ==========================================================


pipeline = Pipeline(

    steps=[


        (

            "preprocessor",

            preprocessor

        ),



        (

            "model",

            rf_model

        )



    ]

)






# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)







# ==========================================================
# TRAIN MODEL
# ==========================================================


print("\nTraining Model...")


pipeline.fit(

    X_train,

    y_train

)






# ==========================================================
# MODEL TESTING
# ==========================================================


prediction = pipeline.predict(

    X_test

)




r2 = r2_score(

    y_test,

    prediction

)


mae = mean_absolute_error(

    y_test,

    prediction

)


rmse = np.sqrt(

    mean_squared_error(

        y_test,

        prediction

    )

)






print("\n============================")

print("MODEL PERFORMANCE")

print("============================")


print(

"Accuracy (R2 Score):",

round(r2*100,2),

"%"

)


print(

"MAE:",

round(mae,2)

)


print(

"RMSE:",

round(rmse,2)

)





# ==========================================================
# SAVE MODEL
# ==========================================================



joblib.dump(

    pipeline,

    "NexusAI_Model.pkl"

)




print("\n============================")

print("AI MODEL SAVED SUCCESSFULLY")

print("============================")