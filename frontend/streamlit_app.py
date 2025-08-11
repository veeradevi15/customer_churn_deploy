import streamlit as st
import requests

st.title("Bank Churn Prediction")
st.write("Enter customer details to predict churn probability:")

credit_score=st.number_input("Credit Score",min_value=300 ,max_value=900 ,value=600)
geography=st.selectbox("Geography",["France","Spain","Germany"])
gender=st.selectbox("Gender",["Male","Female"])
age=st.number_input("Age",min_value=18 ,max_value=100 ,value=30)
tenure=st.number_input("Tenure",min_value=0 ,max_value=10 ,value=1)
balance=st.number_input("Balance",min_value=0.0 ,max_value=100000.0 ,value=5000.0)
num_of_products=st.number_input("Number of Products",min_value=1 ,max_value=5 ,value=1)
has_cr_card=st.selectbox("Has Credit Card",["Yes","No"])
is_active_member=st.selectbox("Is Active Member",["Yes","No"])
estimated_salary=st.number_input("Estimated Salary",min_value=0.0 ,max_value=1000000.0 ,value=50000.0)

if st.button("Predict"):
    has_cr_card = 1 if has_cr_card == "Yes" else 0
    is_active_member = 1 if is_active_member == "Yes" else 0
    
    data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": has_cr_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary
    }

    response = requests.post("https://customer-churn-deploy-2mbo.onrender.com/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        st.write("Churn Probability:", result['churn_probability'])
        st.write("Churned:", result['churned'])
    else:
        st.write("Error:", response.text)
