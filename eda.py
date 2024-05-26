import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def app():
    # Judul dan Informasi mengenai Menu EDA
    st.title('Air Quality Dashboard 2017 - 2019 in 25 Seoul Stations')
    
    # Load data
    df = load_data('dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    pollutant_parameters = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM2.5']

#====================================================================

    # Sidebar untuk filter dan tombol prediksi
    with st.sidebar:
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.write(' ')
        # with col2:
        #     st.image("https://cdn1.iconfinder.com/data/icons/air-pollution-21/62/Air-quality-mask-pollution-protection-256.png",
        #             width=100)
        # with col3:
        #     st.write(' ')
        st.header('Filters')

        # Station filter with multiselect
        selected_stations = st.multiselect('Select Stations', ['Overall Station'] + list(df['District'].unique()))

        selected_category = st.selectbox('Select Category',
                                        ['Overall Category'] + list(df['AQI_Category'].unique()), index=0)
        
        start_date = st.date_input('Start Date', min(df['Date']).date(),
                                        min_value=pd.to_datetime('2017-01-01').date(),
                                        max_value=pd.to_datetime('2019-12-31').date())
        end_date = st.date_input('End Date', max(df['Date']).date(),
                                        min_value=pd.to_datetime('2017-01-01').date(),
                                        max_value=pd.to_datetime('2019-12-31').date())
        # col4, col5, col6 = st.columns(3)
        # with col5:
        # # Tombol Prediksi dengan key unik
        #     if st.button('Filter', key='sidebar_prediksi'):
        #         st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

    # Filter data based on selected stations
    if 'Overall Station' in selected_stations:
        selected_stations.remove('Overall Station')

    start_datetime = pd.to_datetime(start_date).date()
    end_datetime = pd.to_datetime(end_date).date()
    df['Date'] = df['Date'].dt.date

#============================================================================================
    # Opsi Kategori
    if selected_category == 'Overall Category' and not selected_stations:
        # If no specific stations are selected, use all stations
        filtered_data = df[(df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    elif not selected_stations:
        filtered_data = df[(df['AQI_Category'] == selected_category) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    elif selected_category == 'Overall Category':
        filtered_data = df[(df['District'].isin(selected_stations)) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    else:
        filtered_data = df[(df['District'].isin(selected_stations)) & (df['AQI_Category'] == selected_category) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]

    # Opsi Stasiun
    selected_station_str = ', '.join(selected_stations) if selected_stations else 'All Stations'
    st.write(f"**Key Metrics for {selected_station_str} - {selected_category}**")
    category_counts = filtered_data.groupby('AQI_Category')['Date'].nunique()
    cols = st.columns(3)
    for index, (category, count) in enumerate(category_counts.items()):
        formatted_count = "{:,}".format(count)  # Format count with commas for thousands
        col = cols[index % 3]  # Cycle through the columns (3 columns)
        col.metric(category, f"{formatted_count} Days")

    # Calculate counts for each category and set the custom order
    custom_category_order = ["Good", "Moderate", "Unhealthy", "Very unhealthy"]
    category_counts = filtered_data['AQI_Category'].value_counts().reset_index()
    category_counts.columns = ['AQI_Category', 'Count']
    category_counts['AQI_Category'] = pd.Categorical(category_counts['AQI_Category'], categories=custom_category_order, ordered=True)
    category_counts = category_counts.sort_values('AQI_Category')

    # Create a pie chart
    fig = px.pie(category_counts, values='Count', names='AQI_Category', title='Air Quality Categories Percentage')
    st.plotly_chart(fig, use_container_width=True)

#==================================================================
    # Aggregating pollution data
    df['District'] = df['Address'].apply(lambda x: x.split(', Seoul')[0].split(',')[-1].strip())
    agg_data = df.groupby('District')[['PM10', 'PM2.5']].sum().reset_index()

    # Display EDA visualization
    st.write("Total PM10 and PM2.5 by District")
    # Bar chart for total PM10 and PM2.5 by district
    st.bar_chart(agg_data.set_index('District'))

#===================================================================
    # Menambahkan kolom untuk tahun dan bulan
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')

    # Mengelompokkan data berdasarkan bulan dan menghitung rata-rata AQI
    monthly_data = df.groupby('Month')['AQI'].mean().reset_index()

    # Mengubah kolom 'Month' kembali ke format datetime untuk plotting
    monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()

    # Menampilkan judul aplikasi
    st.write("Line Chart AQI per Month")

    # Membuat line chart dengan warna RGB menggunakan Plotly
    fig = px.line(monthly_data, x='Month', y='AQI', title='AQI per Month')
    fig.update_traces(line=dict(color='rgb(110,60,150)'))  # Mengatur warna garis menjadi RGB (110, 60, 150)

    # Menampilkan line chart di Streamlit
    st.plotly_chart(fig, use_container_width=True)

#===========================================================================

    



