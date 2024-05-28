import streamlit as st

def app():
    st.title("Tentang Kami")

    st.subheader("Deskripsi Projek")
    st.markdown("""
        Projek ini merupakan projek akhir dari Program SIB 6 Data Science bersama GreatEdu yang 
        dikerjakan oleh kelompok 1 (Kelas Mentoring 3 bersama Kak Salsa). Projek ini disusun semata-mata 
        untuk tujuan pendidikan dan pembelajaran.
        """)

    tab1, tab2, tab3, tab4 = st.tabs(["Latar Belakang", "Permasalahan", "Tujuan", "Manfaat"])

    with tab1:
        st.info("""Polusi udara merupakan masalah lingkungan yang terus berlanjut di Korea Selatan. Kadar polusi 
        udara seringkali mencapai tingkat yang membahayakan kesehatan, terutama bagi kelompok rentan 
        seperti lansia dan orang dengan kondisi kesehatan tertentu. Penelitian ini bertujuan membangun 
        model prediksi kualitas udara menggunakan kecerdasan buatan. Model ini diharapkan dapat membantu 
        memahami dan memprediksi tingkat kualitas udara di masa depan, sehingga dapat dibuat langkah-langkah
        yang tepat untuk melindungi kesehatan masyarakat dan membuat keputusan terkait lingkungan yang lebih baik.
        """)
    with tab2:
        st.info("""Fluktuasi tingkat kualitas udara di Korea Selatan akibat cuaca dan musim menyulitkan masyarakat 
        mengetahui kapan terpapar polusi berbahaya dan perlu waspada. Selain itu, keterbatasan data polusi 
        udara terkini membuat pemerintah dan lembaga lingkungan kesulitan mengambil tindakan cepat dan efektif 
        untuk mengendalikan polusi. Penelitian ini berupaya mengatasi tantangan tersebut dengan menciptakan 
        model prediksi yang tak hanya memahami pola polusi saat ini, tetapi juga memprediksi tingkat 
        kualitas udara ke depannya.
        """)
    with tab3:
        st.info("""Mengembangkan model Machine Learning untuk memprediksi tingkat kualitas udara di 
        Korea Selatan menggunakan data partikel udara (polutan) yang tersedia. 
        """)
    with tab4:
        st.info("""
        1. Memberi tahu masyrakat kapan mereka mungkin terpapar polusi berbahaya dan kapan mereka perlu melindungi diri.
        2. Membantu pemerintah dan lembaga lingkungan untuk bertindak cepat dan efektif dalam mengendalikan polusi.
        3. Membantu mengurangi dampak kesehatan dan ekonomi dari polusi udara.
        4. Meningkatkan kualitas hidup masyarakat di Korea Selatan.
        """)

    st.subheader("Evaluasi Model")
    tab5, tab6 = st.tabs(["Model Prediction", "Model Forecast (Perlu Pengembangan Kedepannya)"])
    
    with tab5:
        st.info("""
        Kami menggunakan model Random Forest Classifier untuk memprediksi tingkat kualitas udara di kota Seoul:
        - Accuracy Score = 0.984
        - Recall Score = 0.98
        - Precision Score = 0.98
        - F1 Score = 0.984
        """)
    with tab6:
        st.info("""
        Kami menggunakan model Long Short Term Memory untuk memperkirakan pollutan udara pada waktu kedepannya:
        - Variabel SO2: MAE = 0.00, RMSE = 0.00 , MAPE = 21.04
        - Variabel NO2: MAE = 0.01, RMSE = 0.00 , MAPE = 35.18
        - Variabel O3: MAE = 0.01, RMSE = 0.01, MAPE = 39.00
        - Variabel CO: MAE = 0.10, RMSE = 0.13, MAPE = 18.19
        - Variabel PM10: MAE = 9.59, RMSE = 13.02, MAPE = 34.52
        - Variabel PM2.5: MAE = 6.55, RMSE = 8.74, MAPE = 40.19
        """)

    st.subheader("Referensi Tambahan")
    st.markdown("""
        - **Proses Analisis:** [Link ke Colab](https://colab.research.google.com/drive/1mQHPx1Z-horXgvc6vfRgpT9Vpxm8lAu_?usp=sharing)
        - **GitHub Project:** [Link ke GitHub](https://github.com/filbertleo88/GreatEdu-Final-Project---Air-Quality-Seoul-Analysis-dan-Prediction)
        - **PowerPoint:** [Link ke PPT](https://docs.google.com/presentation/d/1THM8Yf-Bo8zogFtPtrq4pI9--QCEsqzgxOt4fbZc7Tw/edit?usp=sharing)
    """)

    st.subheader("Kontak")
    st.markdown("""
        Jika Anda memiliki pertanyaan atau umpan balik, silakan hubungi kami:
    """)
    
    col_1, col_2 = st.columns(2)
    
    with col_1:
        st.markdown("""
            - **Sitanggang Immanuel**
                - Email: [sitanggangimmanuel123@gmail.com](mailto:sitanggangimmanuel123@gmail.com) 
                - LinkedIn: [Sitanggang Immanuel](https://www.linkedin.com/in/sitanggang-immanuel-urat-mangido-tua/) 

            - **Filbert Leonardo**
                - Email: [filbertleo88@gmail.com](mailto:filbertleo88@gmail.com) 
                - LinkedIn: [Filbert Leonardo](https://www.linkedin.com/in/filbert-leonardo/)  
        """)
    with col_2:
        st.markdown("""
            - **Deri Rizky Nugraha**
                - Email: [drnugraha809@gmail.com](mailto:drnugraha809@gmail.com) 
                - LinkedIn: [Deri Rizky Nugraha](https://www.linkedin.com/in/deri-rizky-nugraha-18876b2a3/) 
 
           - **Anas Putra Agazy**
                - Email: [anasagazy99@gmail.com](mailto:anasagazy99@gmail.com) 
                - LinkedIn: [Anas Putra Agazy](https://www.linkedin.com/in/anas-putra-agazy-4192142a3/) 
        """)



   