import streamlit as st
from Tahmin_Motoru import tum_tahminleri_uret
import datetime

st.set_page_config(page_title="İzmir Hava Tahmini", layout="wide", page_icon="🌤️")

st.title("🌤️ İzmir Akıllı Hava Tahmin Sistemi")


# Veri setinin bittiği tarih: 2026-04-26
son_veri_tarihi = datetime.date(2026, 4, 26)

# Sınırları belirliyoruz:
min_tarih = son_veri_tarihi - datetime.timedelta(days=365*2)
max_tarih = datetime.date(2026, 12, 31) 


secilen_tarih = st.date_input(
    "Tahmin istediğiniz günü seçin:", 
    value=son_veri_tarihi,
    min_value=min_tarih, 
    max_value=max_tarih
)

if st.button("Tahmini Göster"):
    yil = secilen_tarih.year
    ay = secilen_tarih.month
    gun = secilen_tarih.day
    yil_gunu = secilen_tarih.timetuple().tm_yday
    
    sonuc = tum_tahminleri_uret(yil, ay, gun, yil_gunu)
    
    # Sıcaklığa göre tema değişimi
    is_hot = sonuc['max_t'] > 24
    bg_style = "linear-gradient(135deg, #FFD700 0%, #FF8C00 100%)" if is_hot else "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"
    st.markdown(f"<style>.stApp {{ background: {bg_style}; color: white; transition: 0.5s; }} [data-testid='stMetricValue'] {{ color: white !important; }}</style>", unsafe_allow_html=True)

    st.subheader(f"📅 {secilen_tarih.strftime('%d %B %Y')} Raporu")
    # METRİK PANELİ
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Max Sıcaklık", f"{sonuc['max_t']:.1f} °C")
    c2.metric("Min Sıcaklık", f"{sonuc['min_t']:.1f} °C") # Yeni Eklendi
    c3.metric("Yağış Oranı", f"%{sonuc['yag']:.1f}")
    c4.metric("Rüzgar Hızı", f"{sonuc['ruz']:.1f} km/s")
    c5.metric("PM10 Değeri", f"{sonuc['p10']:.1f}")
    c6.metric("PM2.5 Değeri", f"{sonuc['p25']:.1f}") # Yeni Eklendi
    
    st.divider()
    st.info(f"**Genel Durum:** {sonuc['durum']}")
    
    # Bildirimler
    tavsiyeler = sonuc['tavsiye'].split(" | ")
    for tavsiye in tavsiyeler:
        if "maske" in tavsiye.lower():
            st.warning(tavsiye)
        else:
            st.success(tavsiye)