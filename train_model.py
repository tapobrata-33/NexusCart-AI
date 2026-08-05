import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


# Load dataset
df = pd.read_csv("retail_sales.csv")

print("Dataset Loaded")
print(df.head())


# Convert text columns into numbers
encoder = LabelEncoder()

for col in df.select_dtypes(include="object").columns:
    df[col] = encoder.fit_transform(df[col].astype(str))


# Select input and target

# Change target column automatically
target = "Total Amount"

X = df.drop(target, axis=1)
y = df[target]


# Split data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train AI model

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# Test model

prediction = model.predict(X_test)

print(
    "Accuracy:",
    r2_score(y_test, prediction)
)

print(
    "Error:",
    mean_absolute_error(y_test, prediction)
)


# Save AI model

joblib.dump(
    model,
    "NexusAI_Model.pkl"
)


print("AI Training Completed Successfully")
print("Model saved: NexusAI_Model.pkl")