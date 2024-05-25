import streamlit as st
import pandas as pd

def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def app():
    # Judul dan Informasi mengenai Menu EDA
    st.title('Air Quality Dashboard 2017 - 2019 in 25 Seoul Stations')

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

    # Mengunggah file CSV
    uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

    # Opsi untuk menggunakan dataset default
    use_default = st.checkbox("Gunakan dataset default")

    # Jika file telah diunggah
    if uploaded_file is not None:
        # Membaca file CSV ke dalam DataFrame
        df = load_data(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    elif use_default:
        # Menggunakan dataset default
        default_file_path = "dataset.csv"  # Ganti dengan path sebenarnya
        df = load_data(default_file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    else:
        df = None

    # Menampilkan data CSV dalam tabel jika ada data yang valid
    if df is not None:
        st.subheader("Data Polusi Udara di Seoul")
        st.dataframe(df)
    else:
        st.write("Silakan unggah file CSV atau pilih untuk menggunakan dataset default.")

#=========================================================================================

    st.divider()
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