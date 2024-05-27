import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from keras.models import load_model as keras_model
from sklearn.preprocessing import MinMaxScaler

from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

import tensorflow as tf
from tensorflow.keras import optimizers
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional, Dense, RepeatVector, TimeDistributed, Dropout

from numpy import array

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

def app():
    st.title('Selamat Datang di Aplikasi Prediksi Kualitas Udara')
    st.subheader('''Prediksi Time Series Partikel Udara dan Kualitas Udara di Seoul Menggunakan Algoritma Long Short Term Memory''')

    # Load data
    filepath = 'datasets/df_final.csv'
    df = load_data(filepath)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  # Convert 'Date' to datetime
    df.set_index('Date', inplace=True)

    # Load model time series
    model = keras_model('models/my_model.h5')

    # Load the trained classifier model from the file
    model_file_path = "models/rfc.pkl"  # Ganti dengan path model 
    classifier = load_model(model_file_path)
    
#================================================================

    # Make sure 'District' column is available in df
    if 'District' in df.columns:
        # Function to get dataset based on selected District
        def get_dataset(df, district):
            df_filtered = df[df['District'] == district]
            df_filtered = df_filtered.drop(columns=['AQI', 'AQI Category', 'Station code', 'District', 'Latitude', 'Longitude'])
            return df_filtered

        # Extract unique districts
        districts = df['District'].unique()

        # Select Dataset
        choose_data = st.sidebar.selectbox("Pilih Daerah", options=districts)
        st.subheader(f"Dataframe {choose_data}")

        # Filter dataset based on the selected district
        df_filtered = get_dataset(df, choose_data)
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.error("The dataset does not contain a 'District' column.")

#==================================================

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
            fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name='Historikal'))
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[column], mode='lines', name='Prakiraan'))
            
            fig.update_layout(
                title=f'Historikal vs Prakiraan {column}',
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
        # Number input for forecast days
        n_forecast_days = st.number_input('Jumlah hari yang ingin diprediksi', min_value=1, max_value=365, value=30)

        # Add predict button
        if st.button('Prediksi'):
            # Prepare test data
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df_filtered)

            n_steps_in, n_steps_out = 1, 1  # Set your steps here
            df_sequences, _ = split_sequences(df_scaled, n_steps_in, n_steps_out)

            forecast = []

            for seq in df_sequences[:n_forecast_days]:
                input_data_reshaped = seq.reshape((1, n_steps_in, df_scaled.shape[1]))
                predicted = model.predict(input_data_reshaped)
                forecast.append(predicted[0])

            forecast_reshaped = np.array(forecast).reshape(-1, df_scaled.shape[1])
            forecast_inverse = scaler.inverse_transform(forecast_reshaped)

            forecast_df = pd.DataFrame(forecast_inverse, columns=df_filtered.columns)
            forecast_df = forecast_df.round(3)

            start_date = df_filtered.index[-1] + pd.DateOffset(days=1)
            date_range = pd.date_range(start=start_date, periods=len(forecast_df))
            forecast_df.index = date_range

            st.subheader("Data Prakiraan")

            # Plot the forecasted data
            plot_forecast(df_filtered, forecast_df)

#=====================================================================
            st.divider()
            # Prediksi Tingkat Kualitas Udara
            def predict_pollution(so2, no2, o3, co, pm10, pm25):
                if classifier is not None:
                    prediction = classifier.predict([[so2, no2, o3, co, pm10, pm25]])
                    return prediction
                else:
                    raise ValueError("The classifier model is not loaded.")

            def map_pollution_level(prediction):
                pollution_levels = {0: 'Good', 1: 'Moderate', 2: 'Unhealthy', 3: 'Very Unhealthy'}
                return pollution_levels[prediction]
            
            forecast_df['AQI Category'] = forecast_df.apply(lambda row: map_pollution_level(predict_pollution(row['SO2'], row['NO2'], row['O3'], row['CO'], row['PM10'], row['PM2.5'])[0]), axis=1)

            # Tambahkan kolom district
            forecast_df['District'] = choose_data
            
            st.subheader("Data Prakiraan dengan Kategori AQI")
            st.dataframe(forecast_df, use_container_width=True)
