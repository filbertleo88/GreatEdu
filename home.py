import streamlit as st
import pandas as pd

def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def app():
    # Judul dan Informasi mengenai Menu EDA
    st.title('Air Quality Dashboard 2017 - 2019 in 25 Seoul Stations')

    st.image('pollution.jpg', caption='Polusi Udara', use_column_width=True)

    with st.expander("About Air Pollution"):
        st.write("""Air Pollution is contamination of the indoor or outdoor environment by any chemical,
             physical, or biological agent that modifies the natural characteristics of the atmosphere.""")
    
    with st.expander("About AQI"):
        st.write("""
        Kualitas udara adalah ukuran seberapa bersih atau tercemarnya udara di suatu daerah. 
        Kualitas udara dapat dipengaruhi oleh berbagai polutan yang berasal dari berbagai sumber, 
        seperti kendaraan bermotor, pabrik, dan aktivitas rumah tangga. Polusi udara dapat berdampak negatif 
        terhadap kesehatan manusia, hewan, dan lingkungan. Beberapa variabel yang sering digunakan untuk mengukur 
        kualitas udara antara lain PM2.5, PM10, O3, NO2, SO2, dan CO. Indeks Kualitas Udara (AQI) adalah salah satu 
        cara untuk mengkomunikasikan seberapa bersih atau tercemarnya udara berdasarkan konsentrasi polutan-polutan ini.
        """)

#=========================================================================================

    st.divider()
    # Dataset
    st.subheader('Dataset')

    # Membaca file CSV ke dalam DataFrame
    default_file_path = "df_daily_pollution_with_aqi.csv"
    df = load_data(default_file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Menampilkan data CSV dalam tabel jika ada data yang valid
    if df is not None:
        st.subheader("Data Polusi Udara di Seoul")
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Silakan download dataset terlebih dahulu.")

#=========================================================================================

    st.subheader("Deskripsi Variabel Polusi Udara 🏭")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["SO2", "NO2", "O3", "CO", "PM10", "PM2.5"])

    with tab1:
        st.info("""Sulfur dioksida, berasal dari pembakaran bahan bakar fosil 
                dan aktivitas vulkanik, dapat menyebabkan iritasi saluran pernapasan.""")
    with tab2:
        st.info("""Nitrogen dioksida, berasal dari emisi kendaraan bermotor dan 
                pembakaran bahan bakar fosil, dapat menyebabkan iritasi paru-paru.""")
    with tab3:
        st.info("""Ozon troposferik, terbentuk dari reaksi kimia antara polutan lain 
                di bawah sinar matahari, dapat menyebabkan masalah pernapasan.""")
    with tab4:
        st.info("""Karbon monoksida, gas tidak berwarna dan tidak berbau yang 
                berasal dari pembakaran tidak sempurna bahan bakar fosil, 
                berbahaya jika terhirup dalam jumlah besar.""")
    with tab5:
        st.info("""Partikulat kasar dengan diameter kurang dari 10 mikrometer, 
                berasal dari debu jalan, konstruksi, pembakaran bahan bakar fosil.""")
    with tab6:
        st.info("""Partikulat halus dengan diameter kurang dari 2.5 mikrometer, 
                berasal dari asap kendaraan, pabrik, pembakaran biomassa.""")

#===============================================================
    st.subheader('AQI Basics Particle Pollution')
    st.markdown("""
    <table>
        <tr>
            <th>Levels of Concern</th>
            <th>Values of Index</th>
            <th>Description of Air Quality</th>
        </tr>
        <tr style='background-color:#00ABF0; color:White'>
            <td>Good</td>
            <td>0 to 50</td>
            <td>A level that will not impact patients suffering from diseases related to air pollution</td>
        </tr>
        <tr style='background-color:#00FF00; color:Black'>
            <td>Moderate</td>
            <td>51 to 100</td>
            <td>A level which may have a meager impact on patients in case of chronic exposure</td>
        </tr>
        <tr style='background-color:#FFFF00; color:Black'>
            <td>Unhealthy</td>
            <td>101 to 250</td>
            <td>A level that may have harmful impacts on patients and members of sensitive groups (children, aged or weak people), and also cause the general public unpleasant feelings</td>
        </tr>
        <tr style='background-color:#FF0000; color:White'>
            <td rowspan=2>Very Unhealthy</td>
            <td>231 to 350</td>
            <td>A level which may have a serious impact on patients and members of sensitive groups in case of acute exposure, and that even the general public can be weakly affected</td>
        </tr>
        <tr style='background-color:#FF0000; color:White'>       
            <td>351 to 500</td>
            <td>A level which may need to take emergency measures for patients and members of sensitive groups and have harmful impacts on the general public</td>
        </tr>
    </table>

    """, unsafe_allow_html=True)

    url = "https://airkorea.or.kr/eng/khaiInfo?PMENU_NO=166"
    st.caption("Adapted from the AIRKOREA [Korea Air Quality Index (AQI)](%s)" % url)

        #     <td>Very Unhealthy</td>
