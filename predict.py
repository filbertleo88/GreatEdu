import streamlit as st
import joblib
import pickle
import pandas as pd

# Load Model Machine Learning
def load_model(file_path):
    try:
        model_in = open(file_path, 'rb')
        model = pickle.load(model_in)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def app():
    # Judul dan Informasi mengenai Menu Prediksi
    st.title('Selamat Datang di Aplikasi Prediksi Kualitas Udara')

    # Load the trained classifier model from the file
    model_file_path = "models/rfc.pkl"  # Ganti dengan path model 
    classifier = load_model(model_file_path)

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
    
    # Halaman Prediksi
    st.subheader("Prediksi Kategori Kualitas Udara di Seoul Menggunakan Algoritma Random Forest Classifier")

    # Input parameters
    # Create input fields for user to enter pollution data
    col1, col2 = st.columns(2)
    with col1:
        so2 = st.number_input('SO2', min_value=0.0000, max_value=1.0, format="%.3f")
        no2 = st.number_input('NO2', min_value=0.0000, max_value=50.0, format="%.3f")
        o3 = st.number_input('O3', min_value=0.0000, max_value=0.6, format="%.3f")
    with col2:
        co = st.number_input('CO', min_value=0.0000, max_value=2.0, format="%.3f")
        pm10 = st.number_input('PM10', min_value=0.0000, max_value=600.0, format="%.3f")
        pm25 = st.number_input('PM2.5', min_value=0.0000, max_value=500.0, format="%.3f")

    # Button to trigger prediction dengan key unik
    if st.button('Prediksi'):
        prediction = predict_pollution(so2, no2, o3, co, pm10, pm25)
        pollution_level = map_pollution_level(prediction[0])
        st.success(f'Kategori kualitas udara yang diprediksi adalah: {pollution_level}')

#=============================================================
   