import streamlit as st
import joblib
import numpy as np


# Load AI Model
model = joblib.load("sales_prediction_model.pkl")


# Website Title

st.title("🚀 NexusCart AI")

st.subheader("Sales Prediction System")


# User Input

quantity = st.number_input(
    "Enter Quantity",
    min_value=1
)


price = st.number_input(
    "Enter Price",
    min_value=1
)



# Prediction Button

if st.button("Predict Sales"):

    input_data = np.array(
        [[quantity, price]]
    )

    prediction = model.predict(
        input_data
    )


    st.success(
        f"Predicted Revenue: ₹ {round(prediction[0],2)}"
    )
    import streamlit as st

st.title("NexusCart AI")
st.write("Website is working!")