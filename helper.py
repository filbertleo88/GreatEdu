import pickle
import pandas as pd
import numpy as np
import streamlit as st

def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

# Load Model Machine Learning
def load_model(file_path):
    try:
        model_in = open(file_path, 'rb')
        model = pickle.load(model_in)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def get_prediction(pollutants,classifier):
    # Define the prediction function
    def predict_pollution(so2, no2, o3, co, pm10, pm25):
        if classifier is not None:
            prediction = classifier.predict([[so2, no2, o3, co, pm10, pm25]])
            return prediction
        else:
            raise ValueError("The classifier model is not loaded.")

    def map_pollution_level(prediction):
        pollution_levels = {0: 'Good', 1: 'Moderate', 2: 'Unhealthy', 3: 'Very unhealthy'}
        return pollution_levels[prediction]