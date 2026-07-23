import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


df = pd.read_csv("retail_sales.csv")


X = df[
    [
        "Age",
        "Quantity",
        "Price per Unit"
    ]
]


y = df["Total Amount"]


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


print(
    "Model Accuracy:",
    accuracy * 100,
    "%"
)


# Save model correctly

joblib.dump(
    model,
    "NexusAI_Model.pkl"
)


print(
    "Model Saved Successfully"
)