import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

# Load data
data = pd.read_csv('dataset.csv')
data['Date'] = pd.to_datetime(data['Date'])

pollutant_parameters = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM2.5']

# # Load the trained classifier model from the file
# pickle_in = open('rfc.pkl', 'rb')
# classifier = pickle.load(pickle_in)

# joblib_file = 'rfc.joblib'
# classifier = None # Initialize classifier to None

# if os.path.exists(joblib_file):
#     classifier = joblib.load(joblib_file)
#     except Exception as e:
#         print(f"An error occurred while loading the model: {e}")
# else:
#     print(f"File {joblib_file} does not exist.")

# To load the model back later
# pickle_file = 
# classifier = pickle.load(open('rfc.pkl','rb'))
# with open(pickle_file, 'rb') as file:
    # classifier = joblib.load(file)

# Load the model
model_path = 'rfc.pkl'

if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as file:
            classifier = pickle.load(file)
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        classifier = None
else:
    st.error("Model file not found.")
    classifier = None

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

# Define the custom category order
custom_category_order = [
    "Good",
    "Moderate",
    "Unhealthy",
    "Very unhealthy"
]

st.title('Air Quality Dashboard 2017 - 2019 in 25 Seoul Stations')

st.title("Tampilan Data CSV")

# Menampilkan DataFrame menggunakan Streamlit
st.write(data)

# Penjelasan Kualitas Udara
st.title('Penjelasan Mengenai Kualitas Udara')

# Paragraf Penjelasan Kualitas Udara
st.write("""
Kualitas udara adalah ukuran seberapa bersih atau tercemarnya udara di suatu daerah. 
Kualitas udara dapat dipengaruhi oleh berbagai polutan yang berasal dari berbagai sumber, 
seperti kendaraan bermotor, pabrik, dan aktivitas rumah tangga. Polusi udara dapat berdampak negatif 
terhadap kesehatan manusia, hewan, dan lingkungan. Beberapa variabel yang sering digunakan untuk mengukur 
kualitas udara antara lain PM2.5, PM10, O3, NO2, SO2, dan CO. Indeks Kualitas Udara (AQI) adalah salah satu 
cara untuk mengkomunikasikan seberapa bersih atau tercemarnya udara berdasarkan konsentrasi polutan-polutan ini.
""")

# Data dictionary
data_info = {
    'Variabel': ['PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO'],
    'Deskripsi': [
        'Partikulat halus dengan diameter kurang dari 2.5 mikrometer, berasal dari asap kendaraan, pabrik, pembakaran biomassa.',
        'Partikulat kasar dengan diameter kurang dari 10 mikrometer, berasal dari debu jalan, konstruksi, pembakaran bahan bakar fosil.',
        'Ozon troposferik, terbentuk dari reaksi kimia antara polutan lain di bawah sinar matahari, dapat menyebabkan masalah pernapasan.',
        'Nitrogen dioksida, berasal dari emisi kendaraan bermotor dan pembakaran bahan bakar fosil, dapat menyebabkan iritasi paru-paru.',
        'Sulfur dioksida, berasal dari pembakaran bahan bakar fosil dan aktivitas vulkanik, dapat menyebabkan iritasi saluran pernapasan.',
        'Karbon monoksida, gas tidak berwarna dan tidak berbau yang berasal dari pembakaran tidak sempurna bahan bakar fosil, berbahaya jika terhirup dalam jumlah besar.'
    ]
}

# Membuat DataFrame
df_info = pd.DataFrame(data_info)

# Menampilkan judul
st.title("Informasi Variabel dan Deskripsinya")

# Menampilkan DataFrame tanpa indeks baris
st.write(df_info.to_html(index=False), unsafe_allow_html=True)
st.write(' ')

# Sidebar untuk filter dan tombol prediksi
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://cdn1.iconfinder.com/data/icons/air-pollution-21/62/Air-quality-mask-pollution-protection-256.png",
                 width=100)
    with col3:
        st.write(' ')
    st.header('Filters')

    # Station filter with multiselect
    selected_stations = st.multiselect('Select Stations', ['Overall Station'] + list(data['District'].unique()))

    selected_category = st.selectbox('Select Category',
                                     ['Overall Category'] + list(data['AQI_Category'].unique()), index=0)
    start_date = st.date_input('Start Date', min(data['Date']).date(),
                                       min_value=pd.to_datetime('2017-01-01').date(),
                                       max_value=pd.to_datetime('2019-12-31').date())
    end_date = st.date_input('End Date', max(data['Date']).date(),
                                     min_value=pd.to_datetime('2017-01-01').date(),
                                     max_value=pd.to_datetime('2019-12-31').date())
    col4, col5, col6 = st.columns(3)
    with col5:
    # Tombol Prediksi dengan key unik
        if st.button('Filter', key='sidebar_prediksi'):
            st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

# Filter data based on selected stations
if 'Overall Station' in selected_stations:
    selected_stations.remove('Overall Station')

start_datetime = pd.to_datetime(start_date).date()
end_datetime = pd.to_datetime(end_date).date()
data['Date'] = data['Date'].dt.date

if selected_category == 'Overall Category' and not selected_stations:
    # If no specific stations are selected, use all stations
    filtered_data = data[(data['Date'] >= start_datetime) & (data['Date'] <= end_datetime)]
elif not selected_stations:
    filtered_data = data[(data['AQI_Category'] == selected_category) &
                         (data['Date'] >= start_datetime) & (data['Date'] <= end_datetime)]
elif selected_category == 'Overall Category':
    filtered_data = data[(data['District'].isin(selected_stations)) &
                         (data['Date'] >= start_datetime) & (data['Date'] <= end_datetime)]
else:
    filtered_data = data[(data['District'].isin(selected_stations)) & (data['AQI_Category'] == selected_category) &
                         (data['Date'] >= start_datetime) & (data['Date'] <= end_datetime)]

selected_station_str = ', '.join(selected_stations) if selected_stations else 'All Stations'
st.write(f"**Key Metrics for {selected_station_str} - {selected_category}**")
category_counts = filtered_data.groupby('AQI_Category')['Date'].nunique()
cols = st.columns(3)
for index, (category, count) in enumerate(category_counts.items()):
    formatted_count = "{:,}".format(count)  # Format count with commas for thousands
    col = cols[index % 3]  # Cycle through the columns (3 columns)
    col.metric(category, f"{formatted_count} Days")

# Calculate counts for each category and set the custom order
category_counts = data['AQI_Category'].value_counts().reset_index()
category_counts.columns = ['AQI_Category', 'Count']
category_counts['AQI_Category'] = pd.Categorical(category_counts['AQI_Category'], categories=custom_category_order, ordered=True)
category_counts = category_counts.sort_values('AQI_Category')

# Create a pie chart
fig = px.pie(category_counts, values='Count', names='AQI_Category', title='Air Quality Categories Percentage')
st.plotly_chart(fig)


# Aggregating pollution data
data['District'] = data['Address'].apply(lambda x: x.split(', Seoul')[0].split(',')[-1].strip())
agg_data = data.groupby('District')[['PM10', 'PM2.5']].sum().reset_index()

# Display EDA visualization
st.subheader("Total PM10 and PM2.5 by District")
# Bar chart for total PM10 and PM2.5 by district
st.bar_chart(agg_data.set_index('District'))


# Menambahkan kolom untuk tahun dan bulan
data['Month'] = pd.to_datetime(data['Date']).dt.to_period('M')

# Mengelompokkan data berdasarkan bulan dan menghitung rata-rata AQI
monthly_data = data.groupby('Month')['AQI'].mean().reset_index()

# Mengubah kolom 'Month' kembali ke format datetime untuk plotting
monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()

# Menampilkan judul aplikasi
st.title("Line Chart AQI per Month")

# Membuat line chart dengan warna RGB menggunakan Plotly
fig = px.line(monthly_data, x='Month', y='AQI', title='AQI per Month')
fig.update_traces(line=dict(color='rgb(110,60,150)'))  # Mengatur warna garis menjadi RGB (110, 60, 150)

# Menampilkan line chart di Streamlit
st.plotly_chart(fig)

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



