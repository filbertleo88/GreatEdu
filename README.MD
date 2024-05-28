# Prediksi dan Analisis Kualitas Udara di Kota Seoul - GreatEdu
Selamat datang di repositori proyek akhir dari program SIB 6 Data Science yang saya ikuti bersama GreatEdu! Proyek ini adalah aplikasi 
Streamlit dashboard web yang berfokus pada analisis data, visualisasi data, dan prediksi tingkat kualitas udara di kota Seoul menggunakan model Machine Learning.

## Table of Contents
- [Tentang Aplikasi](#tentang_aplikasi)
- [Fitur Utama](#fitur_utama)
- [Struktur Proyek](#struktur_proyek)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Sumber Data](#sumber_data)
- [Exploratory Data Analysis](#exploratory_data_analysis)
- [Visualisasi](#visualisasi)

## Tentang Aplikasi
Aplikasi ini dirancang untuk memberikan wawasan mendalam mengenai metrik kualitas udara seperti AQI (Air Quality Index), SO2, NO2, CO, O3, PM2.5, dan PM10. Dengan menggunakan 
aplikasi ini, pengguna dapat memasukkan parameter polutan untuk memprediksi informasi kualitas udara di Seoul.

## Fitur Utama
* Analisis Data: Mengeksplorasi dan menganalisis data kualitas udara secara mendalam.
* Visualisasi Data: Menampilkan visualisasi yang intuitif dan informatif untuk memahami tren dan pola kualitas udara.
* Prediksi Kualitas Udara: Menggunakan model Machine Learning untuk memprediksi tingkat kualitas udara berdasarkan parameter polutan yang dimasukkan oleh pengguna.

Aplikasi ini bertujuan untuk membantu masyarakat, peneliti, dan pembuat kebijakan dalam memahami dan mengelola kualitas udara di kota Seoul, serta mengambil tindakan 
yang tepat untuk meningkatkan kesehatan dan kesejahteraan publik.

## Struktur Proyek
- `datasets/`: Direktori yang berisi file data hasil preprocessing dalam format CSV.
- `notebooks/Air_Pollution_Seoul.ipynb`: Skrip Python untuk pengolahan data, analisis data eksploratif, dan visualisasi data.
- `main.py`: Aplikasi dashboard Streamlit.
- `models/`: Direktori yang berisi model Machine Learning.
- `README.md`: File dokumentasi ini.

## Instalasi
1. Clone repositori ini ke komputer lokal Anda:
```
git clone https://github.com/filbertleo88/GreatEdu-Final-Project---Air-Quality-Seoul-Analysis-dan-Prediction
```
2. Install modul Python yang diperlukan dengan menjalankan:
```
pip install -r requirements.txt
```

## Penggunaan
1. **Pengolahan Data:** Skrip pengolahan data tersedia dalam file `Air_Pollution_Seoul.ipynb` untuk mempersiapkan dan membersihkan data.
2. **Analisis Data Eksploratif (EDA):** Eksplorasi dan analisis data menggunakan skrip Python yang disediakan. Insight dari EDA akan membantu Anda memahami pola kualitas udara.
3. **Visualisasi:** Jalankan dashboard Streamlit untuk eksplorasi data interaktif:
```
streamlit run main.py
```

## Sumber Data
Proyek ini menggunakan data polusi udara dari [Kaggle](https://www.kaggle.com/datasets/bappekim/air-pollution-in-seoul) yang mencakup data tiap jam dari berbagai polutan udara 
(SO2, NO2, CO, O3, PM2.5, dan PM10) di 25 stasiun kota Seoul dari tahun 2017 hingga 2019. Data ini memberikan gambaran komprehensif mengenai tingkat polusi udara di berbagai 
wilayah di Seoul. Selain itu, perhitungan indeks kualitas udara (AQI) didasarkan pada parameter polutan yang diperoleh dari [AirKorea](https://airkorea.or.kr/eng/khaiInfo?PMENU_NO=166), 
yang menyediakan informasi tentang standar dan metode perhitungan AQI untuk memastikan akurasi dan konsistensi dalam penilaian kualitas udara.

## Exploratory Data Analysis
Menyajikan temuan utama dan wawasan dari proses analisis data eksploratif (EDA).[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mQHPx1Z-horXgvc6vfRgpT9Vpxm8lAu_)

## Visualisasi
Menampilkan visualisasi yang dibuat oleh dashboard Streamlit.
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://greatedu-final-project---air-quality-seoul-analysis-dan-predic.streamlit.app/)

## Credits
Proyek ini merupakan hasil kolaborasi dalam Proyek Akhir Data Science GreatEdu dengan rekan-rekan dari kelompok 1. Saya sangat berterima kasih atas kerjasama yang solid dan kontribusi 
dari setiap anggota tim. Terima kasih juga kepada Kak Salsa, mentor kami, yang telah memberikan dukungan, arahan, dan bimbingan yang berharga dalam seluruh proses pengembangan proyek ini.