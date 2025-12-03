import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Səhifə tənzimləmələri
st.set_page_config(page_title=" HSE Reporter", page_icon="🦺", layout="wide")

# Başlıq
st.title("🦺  SƏTƏM İdarəetmə Paneli")
st.markdown("---")

# Yan panel menyusu
menu = st.sidebar.selectbox("Rejim Seçin", ["👷 İşçi: Hadisə Bildir", "📊 Admin: Monitorinq Paneli"])

# Demo data (Database əvəzi)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Tarix': ['2025-12-01', '2025-12-02'],
        'Lokasiya': ['Qazma Sahəsi 1', 'Emal Zavodu'],
        'Kateqoriya': ['Texniki Nasazlıq', 'Yanğın Riski'],
        'Risk_Səviyyəsi': ['Orta', 'Yüksək'],
        'Status': ['Həll Olundu', 'Açıq']
    })

if menu == "👷 İşçi: Hadisə Bildir":
    st.subheader("⚠️ Təhlükəsizlik İnsidenti Bildir")
    
    with st.form("hse_form"):
        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("Lokasiya", ["Neft Daşları", "Qazma Sahəsi 1", "Emal Zavodu", "Ofis Binası"])
            category = st.selectbox("Hadisə Növü", ["Texniki Nasazlıq", "Sürüşmə/Yıxılma", "Yanğın Riski", "Kimyəvi Sızma"])
        with col2:
            risk = st.select_slider("Risk Səviyyəsi", options=["Aşağı", "Orta", "Yüksək", "Kritik"])
            photo = st.file_uploader("Şəkil Yüklə (Sübut)", type=['png', 'jpg'])
        
        description = st.text_area("Hadisənin Təsviri", placeholder="Məsələn: 3-cü blokda boruda sızma müşahidə olundu...")
        
        submitted = st.form_submit_button("🚀 Hesabatı Göndər")
        
        if submitted:
            new_data = {
                'Tarix': datetime.date.today(),
                'Lokasiya': location,
                'Kateqoriya': category,
                'Risk_Səviyyəsi': risk,
                'Status': 'Açıq'
            }
            # Dataya əlavə et
            st.session_state.data = pd.concat([pd.DataFrame([new_data]), st.session_state.data], ignore_index=True)
            st.success("Hesabat uğurla göndərildi! Məsul şəxslər məlumatlandırıldı.")

elif menu == "📊 Admin: Monitorinq Paneli":
    st.subheader("📈 SƏTƏM Statistikası (Canlı)")
    
    # Metriklər
    df = st.session_state.data
    total = len(df)
    critical = len(df[df['Risk_Səviyyəsi'] == 'Kritik'])
    open_cases = len(df[df['Status'] == 'Açıq'])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Ümumi Hesabatlar", total)
    m2.metric("Kritik Risklər", critical, delta_color="inverse")
    m3.metric("Açıq Hadisələr", open_cases, delta="-2")
    
    # Qrafiklər
    c1, c2 = st.columns(2)
    with c1:
        st.write("Risk Səviyyəsi üzrə Paylanma")
        fig1 = px.pie(df, names='Risk_Səviyyəsi', hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.write("Lokasiyalar üzrə İnsidentlər")
        fig2 = px.bar(df, x='Lokasiya', color='Risk_Səviyyəsi')
        st.plotly_chart(fig2, use_container_width=True)
        
    st.write("📋 Son Daxil Olan Məlumatlar")
    st.dataframe(df)
