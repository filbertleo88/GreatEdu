import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from keras.models import load_model as keras_model
from sklearn.preprocessing import MinMaxScaler
import joblib

import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Dropout

from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

from numpy import array
from numpy import hstack

# Load Model Machine Learning
def load_model(file_path):
    try:
        model = joblib.load(file_path)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def app():
    st.title('Pollutant Forecasting Streamlit App')
    st.subheader('Forecasting Pollutant in Seoul')

    filepath = 'df_daily_pollution.csv'

    def load_data(pathfile):
        df = pd.read_csv(pathfile, sep=';')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  # Convert 'Date' to datetime
        df.set_index('Date', inplace=True)  # Set 'Date' as the index
        return df

    df_ISPU = load_data(filepath)

    # Load the trained classifier model from the file
    model_file_path = "models/lgbm.sav"  # Ganti dengan path model yang benar
    classifier = load_model(model_file_path)

    # Load model
    model_filename = 'models/my_model'  # Adjust filename if needed
    # model = tf.keras.models.load_model(model_filename)
    # model = keras_model('model_101.h5')
    # st.write(model)

    model = tf.keras.models.load_model('model_101.h5')
    # model = joblib.load("models/model_101.pkl")

    # Function to create new dataframes for each pollutant
    def makenewdf(df_ISPU):
        df_pm10 = df_ISPU[['PM10']]
        df_pm25 = df_ISPU[['PM2.5']]
        df_so2 = df_ISPU[['SO2']]
        df_co = df_ISPU[['CO']]
        df_o3 = df_ISPU[['O3']]
        df_no2 = df_ISPU[['NO2']]
        return df_pm10, df_pm25, df_so2, df_co, df_o3, df_no2

    df_pm10, df_pm25, df_so2, df_co, df_o3, df_no2 = makenewdf(df_ISPU)

    # Function to get dataset based on selected station code
    def get_dataset(df_ISPU, station_code):
        df_filtered = df_ISPU[df_ISPU['Station code'] == int(station_code)]
        df_filtered = df_filtered.drop(columns=['Station code', 'Latitude', 'Longitude','Address'])
        return df_filtered

    # Select Dataset
    choose_data = st.sidebar.selectbox("Choose a Dataset", options=['101', '102', '103'])
    st.header(f'Station Code: {choose_data}')
    st.subheader("Dataframe")

    df = get_dataset(df_ISPU, choose_data)
    st.write(df)

    # Split a multivariate sequence into samples
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
     # Function to plot original and forecasted data
    def plot_forecast(df, forecast_df):
        for column in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name='Original'))
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[column], mode='lines', name='Forecasted'))
            
            fig.update_layout(
                title=f'Original vs Forecasted {column}',
                xaxis_title='Date',
                yaxis_title=column,
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(visible=True),
                    type="date"
                )
            )
            st.plotly_chart(fig)

    if model:
        st.write("Model loaded and ready for predictions.")

        # Number input for forecast days
        n_forecast_days = st.number_input('Number of days to forecast', min_value=1, max_value=365, value=30)

        # Add predict button
        if st.button('Prediksi'):
            # Prepare test data
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df)

            n_steps_in, n_steps_out = 1, 1  # Set your steps here
            df_sequences, _ = split_sequences(df_scaled, n_steps_in, n_steps_out)

            forecast = []

            for seq in df_sequences[:n_forecast_days]:
                input_data_reshaped = seq.reshape((1, n_steps_in, df_scaled.shape[1]))
                predicted = model.predict(input_data_reshaped)
                forecast.append(predicted[0])

            forecast_reshaped = np.array(forecast).reshape(-1, df_scaled.shape[1])
            forecast_inverse = scaler.inverse_transform(forecast_reshaped)

            forecast_df = pd.DataFrame(forecast_inverse, columns=df.columns)
            forecast_df = forecast_df.round(3)

            start_date = df.index[-1] + pd.DateOffset(days=1)
            date_range = pd.date_range(start=start_date, periods=len(forecast_df))
            forecast_df.index = date_range

            st.subheader("Forecasted Data")
            # st.write(forecast_df)

            # Plot the forecasted data
            plot_forecast(df, forecast_df)

            def predict_pollution(so2, no2, o3, co, pm10, pm25):
                if classifier is not None:
                    prediction = classifier.predict([[so2, no2, o3, co, pm10, pm25]])
                    return prediction
                else:
                    raise ValueError("The classifier model is not loaded.")

            def map_pollution_level(prediction):
                pollution_levels = {0: 'Good', 1: 'Moderate', 2: 'Unhealthy', 3: 'Very Unhealthy'}
                return pollution_levels[prediction]
            
            forecast_df['Pollution Level'] = forecast_df.apply(lambda row: map_pollution_level(predict_pollution(row['SO2'], row['NO2'], row['O3'], row['CO'], row['PM10'], row['PM2.5'])[0]), axis=1)

            st.subheader("Forecasted Data with Pollution Levels")
            st.dataframe(forecast_df)
