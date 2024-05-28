import streamlit as st
import pandas as pd

def load_data(file_path, index_col=None):
    # index_col akan diabaikan jika None
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def app():
    # Judul dan Informasi mengenai Menu EDA
    st.title('Analisis dan Prediksi Kualitas Udara di Seoul')
    st.write("""Selamat datang di aplikasi kami yang didedikasikan untuk menganalisis dan memprediksi 
             kualitas udara di Seoul. Aplikasi ini memberikan wawasan mendalam tentang kualitas udara 
             di berbagai distrik Seoul berdasarkan data historis. Kami menggunakan teknik 
             Exploratory Data Analysis (EDA) untuk mengidentifikasi pola, tren, dan anomali dalam 
             data kualitas udara. Dengan prediksi ini, kami berharap dapat membantu meningkatkan 
             kesadaran masyarakat dan mendukung keputusan untuk meningkatkan kualitas udara di masa depan.
            Jelajahi berbagai fitur yang tersedia untuk mendapatkan pemahaman yang lebih baik tentang 
             kualitas udara di kota Seoul.""")

    st.image('image/pollution.jpg', caption='Polusi Udara', use_column_width=True)

    with st.expander("Polusi Udara"):
        st.write("""
        Polusi udara adalah kontaminasi udara oleh zat-zat berbahaya yang menyebabkan dampak negatif 
        terhadap kesehatan manusia dan lingkungan. Zat-zat ini termasuk partikel (PM10 dan PM2.5), 
        gas-gas berbahaya seperti nitrogen dioksida (NO2), sulfur dioksida (SO2), karbon monoksida (CO),
        dan ozon (O3). Di Seoul, polusi udara menjadi perhatian utama karena tingginya tingkat urbanisasi 
        dan industrialisasi. Sumber polusi udara di kota ini bervariasi, termasuk emisi kendaraan bermotor,
        aktivitas industri, pembakaran bahan bakar fosil, dan bahkan polusi lintas batas dari negara 
        tetangga. Dampak polusi udara pada kesehatan manusia meliputi gangguan pernapasan, penyakit 
        kardiovaskular, dan peningkatan risiko kanker paru-paru. Selain itu, polusi udara juga dapat 
        merusak ekosistem, mengurangi visibilitas, dan menyebabkan kerusakan pada bangunan serta 
        infrastruktur. Melalui aplikasi ini, kami menyediakan data dan analisis terkini mengenai kualitas 
        udara di Seoul, membantu masyarakat untuk memahami tingkat polusi dan mengambil tindakan pencegahan
        yang diperlukan.
        """)
    
    with st.expander("Indeks Kualitas Udara (AQI)"):
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
    # Membaca file CSV ke dalam DataFrame
    file_path = "datasets/df_daily_pollution_with_aqi.csv" # Sebelum Handling Outlier
    # file_path = "datasets/df_final.csv" # Setelah Handling Outlier
    df = load_data(file_path)
    # df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Menampilkan data CSV dalam tabel jika ada data yang valid
    if df is not None:
        st.subheader("Data Polusi Udara di Seoul")
        st.write("""
                    Dataset ini mencakup data polusi udara di Seoul yang **telah diolah** secara komprehensif. Beberapa tahapan yang dilakukan dalam pengolahan dataset ini meliputi:
                    - **Perhitungan AQI (Air Quality Index)**: Indeks Kualitas Udara dihitung berdasarkan konsentrasi berbagai polutan seperti PM2.5, PM10, NO2, SO2, CO, dan O3. AQI memberikan gambaran tentang seberapa bersih atau tercemarnya udara di lokasi tertentu.
                    - **Pembersihan Data**: Tahap ini melibatkan penghapusan data yang hilang atau tidak valid, serta penanganan outlier untuk memastikan kualitas data yang lebih akurat.
                    - **Transformasi Data**: Data mentah diubah menjadi format yang lebih sesuai untuk analisis, termasuk agregasi data berdasarkan waktu atau lokasi.
                    Dengan data yang telah diolah ini, kami dapat melakukan berbagai analisis mendalam dan prediksi mengenai kualitas udara di Seoul. Data ini sangat penting untuk memahami tren polusi udara, mengidentifikasi faktor-faktor penyebab, dan membantu dalam pengambilan keputusan untuk perbaikan kualitas udara di masa depan.
                """)
        st.dataframe(df, use_container_width=True)
        url = "https://www.kaggle.com/datasets/bappekim/air-pollution-in-seoul"
        st.caption("Data mentah dapat diperoleh dari KAGGLE [Air Pollution in Seoul](%s)" % url)
    else:
        st.write("Silakan download dataset terlebih dahulu.")

#=========================================================================================

    st.subheader("Deskripsi Variabel Dataset")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs(["Date", "SO2", "NO2", "O3", "CO", "PM10", "PM2.5",
                                                  "AQI", "AQI Category", "Station code", "District",
                                                  "Longitude", "Latitude"])

    with tab1:
        st.info("""Tanggal dan waktu saat pengamatan dilakukan.""")
    with tab2:    
        st.info("""Sulfur dioksida, berasal dari pembakaran bahan bakar fosil 
                dan aktivitas vulkanik, dapat menyebabkan iritasi saluran pernapasan.""")
    with tab3:
        st.info("""Nitrogen dioksida, berasal dari emisi kendaraan bermotor dan 
                pembakaran bahan bakar fosil, dapat menyebabkan iritasi paru-paru.""")
    with tab4:
        st.info("""Ozon troposferik, terbentuk dari reaksi kimia antara polutan lain 
                di bawah sinar matahari, dapat menyebabkan masalah pernapasan.""")
    with tab5:
        st.info("""Karbon monoksida, gas tidak berwarna dan tidak berbau yang 
                berasal dari pembakaran tidak sempurna bahan bakar fosil, 
                berbahaya jika terhirup dalam jumlah besar.""")
    with tab6:
        st.info("""Partikulat kasar dengan diameter kurang dari 10 mikrometer, 
                berasal dari debu jalan, konstruksi, pembakaran bahan bakar fosil.""")
    with tab7:
        st.info("""Partikulat halus dengan diameter kurang dari 2.5 mikrometer, 
                berasal dari asap kendaraan, pabrik, pembakaran biomassa.""")
    with tab8:
        st.info("""Indeks yang digunakan untuk melaporkan kualitas udara harian.""")
    with tab9:    
        st.info("""Mengelompokkan kualitas udara ke dalam beberapa tingkat, 
                yang masing-masing memiliki implikasi kesehatan.""")
    with tab10:
        st.info("""Kode stasiun tempat pengamatan dilakukan.""")
    with tab11:
        st.info("""Sebelumnya merupakan kolom alamat namun diubah menjadi 
                nama daerah tempat pengamatan dilakukan.""")
    with tab12:
        st.info("""Bujur geografis tempat pengamatan dilakukan.""")
    with tab13:
        st.info("""Lintang geografis tempat pengamatan dilakukan.""")
#==============================================================
    st.divider()
    # HTML code for the table
    html_table = """
    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th>Good</th>
                <th>Moderate</th>
                <th>Unhealthy</th>
                <th>Very Unhealthy</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>I<sub>LO</sub></td>
                <td>0</td>
                <td>51</td>
                <td>101</td>
                <td>251</td>
            </tr>
            <tr>
                <td>I<sub>HI</sub></td>
                <td>50</td>
                <td>100</td>
                <td>250</td>
                <td>500</td>
            </tr>
            <tr>
                <td>Concentration</td>
                <td>BP<sub>LO</sub> - BP<sub>HI</sub></td>
                <td>BP<sub>LO</sub> - BP<sub>HI</sub></td>
                <td>BP<sub>LO</sub> - BP<sub>HI</sub></td>
                <td>BP<sub>LO</sub> - BP<sub>HI</sub></td>
            </tr>
            <tr>
                <td>SO₂(ppm) 1hr</td>
                <td>0 - 0.02</td>
                <td>0.021 - 0.05</td>
                <td>0.051 - 0.15</td>
                <td>0.151 - 1</td>
            </tr>
            <tr>
                <td>CO(ppm) 1hr</td>
                <td>0 - 2</td>
                <td>2.1 - 9</td>
                <td>9.1 - 15</td>
                <td>15.1 - 50</td>
            </tr>
            <tr>
                <td>O₃(ppm) 1hr</td>
                <td>0 - 0.03</td>
                <td>0.031 - 0.09</td>
                <td>0.091 - 0.15</td>
                <td>0.151 - 0.6</td>
            </tr>
            <tr>
                <td>NO₂(ppm) 1hr</td>
                <td>0 - 0.03</td>
                <td>0.031 - 0.06</td>
                <td>0.061 - 0.2</td>
                <td>0.201 - 2</td>
            </tr>
            <tr>
                <td>PM₁₀(µg/m³) 24hr</td>
                <td>0 - 30</td>
                <td>31 - 80</td>
                <td>81 - 150</td>
                <td>151 - 600</td>
            </tr>
            <tr>
                <td>PM₂.₅(µg/m³) 24hr</td>
                <td>0 - 15</td>
                <td>16 - 35</td>
                <td>36 - 75</td>
                <td>76 - 500</td>
            </tr>
        </tbody>
    </table>
    """

    # Displaying the table with st.markdown
    st.subheader("Kategori Indeks Kualitas Udara dan Konsentrasi Polutan")
    st.write("""
    Tabel di bawah ini menunjukkan kategori Indeks Kualitas Udara (AQI) berdasarkan konsentrasi berbagai polutan:
    """)
    st.markdown(html_table, unsafe_allow_html=True)

#===============================================================
    st.write("")
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
            <td>Tingkat yang tidak akan berdampak pada pasien yang menderita penyakit 
                yang berkaitan dengan polusi udara</td>
        </tr>
        <tr style='background-color:#00FF00; color:Black'>
            <td>Moderate</td>
            <td>51 to 100</td>
            <td>Tingkat yang mungkin memiliki dampak kecil pada pasien jika terjadi paparan kronis</td>
        </tr>
        <tr style='background-color:#FFFF00; color:Black'>
            <td>Unhealthy</td>
            <td>101 to 250</td>
            <td>Tingkat yang dapat menimbulkan dampak berbahaya bagi pasien dan anggota kelompok sensitif 
                (anak-anak, orang lanjut usia, atau orang lemah), serta menimbulkan perasaan tidak 
                menyenangkan bagi masyarakat umum</td>
        </tr>
        <tr style='background-color:#FF0000; color:White'>
            <td rowspan=2>Very Unhealthy</td>
            <td>231 to 350</td>
            <td>Tingkat yang dapat berdampak serius pada pasien dan anggota kelompok sensitif jika terjadi paparan 
                akut, dan bahkan masyarakat umum pun dapat terpengaruh secara lemah</td>
        </tr>
        <tr style='background-color:#FF0000; color:White'>       
            <td>351 to 500</td>
            <td>Tingkat yang mungkin perlu dilakukan tindakan darurat untuk pasien dan anggota kelompok sensitif 
                dan memiliki dampak berbahaya bagi masyarakat umum</td>
        </tr>
    </table>

    """, unsafe_allow_html=True)

    url = "https://airkorea.or.kr/eng/khaiInfo?PMENU_NO=166"
    st.caption("Dikutip dari AIRKOREA [Korea Comprehensive Air-quality Index (CAI)](%s)" % url)

