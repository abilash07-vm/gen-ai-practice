# CreditScore	Geography	Gender	Age	Tenure	Balance	NumOfProducts	HasCrCard	IsActiveMember	EstimatedSalary

import pickle
import streamlit as st
import pandas as pd
from keras.models import load_model

model = load_model('./data/model.h5')

st.title('Bank Churn Prediction')

creditScore = st.number_input('Credit Score')
geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
gender = st.selectbox('Gender', ['Male', 'Female'])

age = st.slider('Age',18, 90)
tenure = st.slider('Tenure', 1, 10)
balance = st.number_input('Account Balance')

numOfProduct = st.number_input('Number of Product')
hasCreditCard = st.selectbox('Has Credit Card',[0, 1])
isActiveMember = st.selectbox('Is Active Member',[0, 1])
estimatedSalary = st.number_input('Estimated Salary')

input_pd = pd.DataFrame(
    {
        'CreditScore':  [creditScore],
        'Geography':  [geography],
        'Gender':  [gender],
        'Age':  [age],
        'Tenure':  [tenure],
        'Balance':  [balance],
        'NumOfProducts':  [numOfProduct],
        'HasCrCard':  [hasCreditCard],
        'IsActiveMember':  [isActiveMember],
        'EstimatedSalary' : [estimatedSalary]
    }
)

with open('./data/label_encoder_gender.pkl', 'rb') as data:
    label_encoder_gender = pickle.load(data)

with open('./data/onehot_encoder_geo.pkl', 'rb') as data:
    onehot_encoder_geo = pickle.load(data)

with open('./data/scalar.pkl', 'rb') as data:
    scalar = pickle.load(data)

input_pd['Gender'] = label_encoder_gender.transform(input_pd['Gender'])

geo_onehot_data = onehot_encoder_geo.transform(input_pd[['Geography']]).toarray()
geo_onehot_pd = pd.DataFrame(geo_onehot_data, columns=onehot_encoder_geo.get_feature_names_out())

input_pd = pd.concat([input_pd.drop(['Geography'], axis=1), geo_onehot_pd], axis=1)

scalar_data = scalar.transform(input_pd)

model_prediction_output = model.predict(scalar_data)

st.write(model_prediction_output)