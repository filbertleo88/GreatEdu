import streamlit as st
import joblib
import lightgbm


# Load Model Machine Learning
def load_model(file_path):
    try:
        model = joblib.load(file_path)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def app():
    # Judul dan Informasi mengenai Menu Prediksi
    st.title('Air Quality Prediction')

    # Load the trained classifier model from the file
    model_file_path = "models/lgbm.sav"  # Ganti dengan path model yang benar
    classifier = load_model(model_file_path)
    if classifier:
        st.write("Model berhasil dimuat.")
    else:
        st.write("Model tidak dapat dimuat.")

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
    st.subheader("Halaman Prediksi")

    # Input parameters
    # Create input fields for user to enter pollution data
    so2 = st.number_input('SO2', min_value=0.0000, max_value=1000.0)
    no2 = st.number_input('NO2', min_value=0.0000, max_value=1000.0)
    o3 = st.number_input('O3', min_value=0.0000, max_value=1000.0)
    co = st.number_input('CO', min_value=0.0000, max_value=1000.0)
    pm10 = st.number_input('PM10', min_value=0.0000, max_value=1000.0)
    pm25 = st.number_input('PM2.5', min_value=0.0000, max_value=1000.0)

    result = ""
    # Button to trigger prediction dengan key unik
    if st.button('Predict'):
        prediction = predict_pollution(so2, no2, o3, co, pm10, pm25)
        pollution_level = map_pollution_level(prediction[0])
        st.success(f'The predicted pollution level is: {pollution_level}')