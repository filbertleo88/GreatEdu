import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import pearsonr, kendalltau

# Lib to create maps
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import folium_static
import geopandas as gpd


def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def app():
    # Judul dan Informasi mengenai Menu EDA
    st.title('Dasboard Kualitas Udara dari 25 Daerah di Seoul (2017 - 2019) ')
    
    # Load data
    df = load_data('datasets/df_final.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    pollutant_parameters = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM2.5', 'AQI']

    # Dictionary to map categories to their respective colors
    category_colors = {
        "Good": "#00ABF0",         # Blue
        "Moderate": "#00FF00",     # Green
        "Unhealthy": "#FFFF00",    # Yellow
        "Very unhealthy": "#FF0000" # Red
    }

#====================================================================

    # Sidebar untuk filter
    with st.sidebar:

        st.header('Filters')

        # district filter with multiselect
        selected_districts = st.multiselect('Pilih Daerah', ['Overall District'] + list(df['District'].unique()))

        selected_category = st.selectbox('Pilih Kategori AQI',
                                        ['Overall Category'] + list(df['AQI Category'].unique()), index=0)
        
        start_date = st.date_input('Tanggal Mulai', min(df['Date']).date(),
                                        min_value=pd.to_datetime('2017-01-01').date(),
                                        max_value=pd.to_datetime('2019-12-31').date())
        end_date = st.date_input('Tanggal Berakhir', max(df['Date']).date(),
                                        min_value=pd.to_datetime('2017-01-01').date(),
                                        max_value=pd.to_datetime('2019-12-31').date())
     
    # Filter data based on selected districts
    if 'Overall district' in selected_districts:
        selected_districts.remove('Overall district')

    start_datetime = pd.to_datetime(start_date).date()
    end_datetime = pd.to_datetime(end_date).date()
    df['Date'] = df['Date'].dt.date

#============================================================================================
    
    # Opsi Kategori
    if selected_category == 'Overall Category' and not selected_districts:
        # If no specific districts are selected, use all districts
        filtered_data = df[(df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    elif not selected_districts:
        filtered_data = df[(df['AQI Category'] == selected_category) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    elif selected_category == 'Overall Category':
        filtered_data = df[(df['District'].isin(selected_districts)) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
    else:
        filtered_data = df[(df['District'].isin(selected_districts)) & (df['AQI Category'] == selected_category) &
                            (df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]

## Total Days of AQI Category
    # Opsi Daerah
    selected_district_str = ', '.join(selected_districts) if selected_districts else 'Semua Daerah'
    st.write(f"**Metrik Utama untuk {selected_district_str} - {selected_category}**")
    category_counts = filtered_data.groupby('AQI Category')['Date'].nunique()
    cols = st.columns(4)
    for index, (category, count) in enumerate(category_counts.items()):
        formatted_count = "{:,}".format(count)  # Format count with commas for thousands
        col = cols[index % 4]  # Cycle through the columns (4 columns)
        
        # Get the color for the current category
        color = category_colors[category]
        
        # Display the metric with custom color
        col.markdown(f"""
            <div style="color:{color};">
                <h3>{category}</h3>
                <p>{formatted_count} Hari</p>
            </div>
        """, unsafe_allow_html=True)

## Distribution of AQI Category
    # Calculate counts for each category and set the custom order
    custom_category_order = ["Good", "Moderate", "Unhealthy", "Very unhealthy"]
    category_counts = filtered_data['AQI Category'].value_counts().reset_index()
    category_counts.columns = ['AQI Category', 'Count']
    category_counts['AQI Category'] = pd.Categorical(category_counts['AQI Category'], categories=custom_category_order, ordered=True)
    category_counts = category_counts.sort_values('AQI Category')

    # Create a pie chart with custom colors
    fig = px.pie(
        category_counts, 
        values='Count', 
        names='AQI Category', 
        title='Persentase Kategori Kualitas Udara',
        color='AQI Category',
        color_discrete_map=category_colors
    )

    st.plotly_chart(fig, use_container_width=True)

## Top 5 Best and Worse District AQI
    # Calculate the average AQI for each district
    avg_aqi_per_district = filtered_data.groupby('District')['AQI'].mean().reset_index()
    avg_aqi_per_district.columns = ['District', 'Average AQI']

    # Get the top 5 districts with the best and worst average AQI
    top_5_best = avg_aqi_per_district.nsmallest(5, 'Average AQI')
    top_5_worst = avg_aqi_per_district.nlargest(5, 'Average AQI')

    # Define custom color scales
    color_scale_best = px.colors.sequential.Blues
    color_scale_worst = px.colors.sequential.Reds

    # Create bar plots
    fig_best = px.bar(top_5_best, x='District', y='Average AQI', 
                    title='5 Daerah dengan Rata-rata AQI Terbaik', 
                    color='Average AQI', color_continuous_scale=color_scale_best)
    fig_worst = px.bar(top_5_worst, x='District', y='Average AQI', 
                    title='5 Daerah dengan Rata-rata AQI Terburuk', 
                    color='Average AQI', color_continuous_scale=color_scale_worst)

    # Update layout for better visual appeal
    fig_best.update_layout(
        xaxis_title='District',
        yaxis_title='Average AQI',
        title_x=0.25,
        template='plotly_white',
        coloraxis_showscale=False
    )
    fig_worst.update_layout(
        xaxis_title='District',
        yaxis_title='Average AQI',
        title_x=0.25,
        template='plotly_white',
        coloraxis_showscale=False
    )

    # Display plots in Streamlit
    col1, col2 = st.columns(2)

    col1.plotly_chart(fig_best, use_container_width=True)
    col2.plotly_chart(fig_worst, use_container_width=True)

## AQI Map
    st.subheader("Peta AQI")
    with st.expander("Peta AQI"):
        # Load data
        df_map = filtered_data.copy()
        df_map = df_map[['AQI','Latitude','Longitude','District']]
        
        seoul_geojson = gpd.read_file('seoul_municipalities_geo_simple.json')

        # Calculate average AQI per district
        avg_aqi_district = df_map.groupby('District').agg({
            'AQI': 'mean', 
            'Latitude': 'mean', 
            'Longitude': 'mean'
        }).reset_index()
        avg_aqi_district.columns = ['District', 'Average AQI', 'Latitude', 'Longitude']
        
        # Merge GeoJSON with average AQI data
        seoul_geojson = seoul_geojson.merge(avg_aqi_district, left_on='name_eng', right_on='District', how='left')

        # Initialize the map centered around Seoul
        pollutant_map = folium.Map(location=[37.5665, 126.9780], tiles='cartodbpositron', zoom_start=11)

        # Add the choropleth layer
        Choropleth(
            geo_data=seoul_geojson,
            data=avg_aqi_district,
            columns=['District', 'Average AQI'],
            key_on='feature.properties.name_eng',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Average AQI by District',
            reset=True
        ).add_to(pollutant_map)

        # Add markers for the average AQI of each district
        for idx, row in avg_aqi_district.iterrows():
            latitude = row['Latitude']
            longitude = row['Longitude']
            district = row['District']
            average_aqi = row['Average AQI']
            station = f"{district} AQI={average_aqi:.2f}"

            if average_aqi > 151:
                pop_color = 'red'  # Red for very bad AQI
            elif average_aqi > 101:
                pop_color = 'orange'  # Orange for moderate AQI
            else:
                pop_color = 'green'  # Green for good AQI

            folium.Marker(
                location=[latitude, longitude],
                popup=station,
                icon=folium.Icon(color=pop_color)
            ).add_to(pollutant_map)
        
        # Display the map
        folium_static(pollutant_map, width=1000, height=600)

#==================================================================
## Time Series of Air Pollutant

    col1, col2 = st.columns(2)
    with col1:
        selected_parameter = st.selectbox('Pilih Parameter Polutan Udara', pollutant_parameters)
    with col2:
        frequency_options = {
            'Harian': 'D',
            'Mingguan': 'W',
            'Bulanan': 'M',
            'Tahunan': 'Y'
        }
        selected_frequency_label = st.selectbox('Pilih Frekuensi Waktu', list(frequency_options.keys()))
        selected_frequency = frequency_options[selected_frequency_label]

    # Set 'Date' column as the index
    datetime_data = filtered_data.copy()
    datetime_data['Date'] = pd.to_datetime(datetime_data['Date'])
    datetime_data.set_index('Date', inplace=True)
    datetime_data = datetime_data.drop(columns=['AQI Category','Station code','Latitude','Longitude'],axis=1)

    # Resample the data based on the selected frequency
    datetime_data_resampled = datetime_data.groupby('District').resample(selected_frequency).mean().reset_index()

    # Plot the chart for the selected districts
    fig = px.line(datetime_data_resampled, x='Date', y=selected_parameter, color='District',
                title=f'Tingkat {selected_parameter} {selected_frequency_label} Berdasarkan Daerah Selama Periode Waktu Tertentu')

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
#==================================================================
## Correlation of Air Pollutant

    
    # Display Scatter Plot
    col1, col2 = st.columns(2)
    with col1:
        selected_parameter1 = st.selectbox('Pilih Parameter 1', pollutant_parameters)
    with col2:
        selected_parameter2 = st.selectbox('Pilih Parameter 2', pollutant_parameters)

    st.subheader("Korelasi Antar Partikel Udara")
    col1, col2 = st.columns([3, 1])
    with col1:
        # Display Scatter Plot with color mapping
        fig_scatter = px.scatter(filtered_data, x=selected_parameter1, y=selected_parameter2,
                                color='AQI Category', color_discrete_map=category_colors,
                                title=f'{selected_parameter1} vs. {selected_parameter2} Correlation')

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption('Korelasi Antar Partikel Udara dengan *Pearson Correlation Coefficient*')
    
    with col2:
        # Calculate Pearson correlation coefficient
        corr_part = pearsonr(filtered_data[selected_parameter1], filtered_data[selected_parameter2])
        percent = round(corr_part[0] * 100, 2)

        if percent > 50:
            percent_status = 'Korelasi Tinggi'
        elif percent > 30:
            percent_status = 'Korelasi Menengah'
        else:
            percent_status = 'Korelasi Rendah'

        st.markdown(f'##### Korelasi antara {selected_parameter1} dengan {selected_parameter2}')
        st.subheader(f'{percent}%')
        st.markdown(f'##### ***{percent_status}***')
        
#==================================================================
# Air Particle Correlation with AQI Category

    filtered_data['AQI Category'] = filtered_data['AQI Category'].map({
        'Good':0,
        'Moderate':1,
        'Unhealthy':2,
        'Very unhealthy':3
    })

    pollutants = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM2.5']

    particle = []
    score = []

    df_score = pd.DataFrame()

    for feat in pollutants:
        tau, p_value = kendalltau(filtered_data[feat], filtered_data['AQI Category'])
        particle.append(feat)
        score.append(abs(tau))

    df_score['Particle'] = particle
    df_score['Score'] = score

    st.subheader('Jenis Partikel Udara yang Mempengaruhi Kategori Kualitas Udara')
    col1, col2 = st.columns([3, 1])

    with col1:
        fig = go.Figure(data=[go.Pie(labels=particle, 
                                    values=score, 
                                    textinfo='label+percent', 
                                    pull=[0, 0, 0, 0, 0, 0.1])])
        fig.update_layout(
            title='Korelasi Partikel Udara terhadap Kategori AQI',
            title_font_size=20
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption('Korelasi Partikel Udara terhadap Kategori Kualitas Udara dengan *Kendall-tau Score*')

    with col2:
        st.write('''Partikel - partikel udara seperti *PM10, PM2.5, O3, NO2, CO*, dan *SO2* ini memang merupakan 
                 faktor terjadinya pencemaran udara di Seoul apabila volumenya yang melampaui batas, 
                 dan dari data yang ada, kita bisa mengetahui bahwa jenis partikel udara yang paling 
                 mempengaruhi terjadinya pencemaran udara di Seoul yaitu **PM2.5**''')
        
#==================================================================
## Average Pollution Levels
    # Aggregating pollution data
    agg_data = filtered_data.copy()
    agg_data = agg_data[['SO2','NO2','O3','CO','PM10','PM2.5','AQI','District']]
    agg_data = agg_data.groupby('District').mean().reset_index()

    fig = px.bar(agg_data, x='District', y=agg_data.columns[1:], barmode='group',
                title='Tingkat Rataan Polusi Berdasarkan Distrik',
                labels={'value': 'Average Pollution Level', 'variable': 'Pollutant'})
    st.plotly_chart(fig, use_container_width=True)

#===================================================================



