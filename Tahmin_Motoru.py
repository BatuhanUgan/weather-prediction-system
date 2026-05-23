import joblib
import pandas as pd
import os

def hava_durumu_yorumu(sicaklik, yagis_ihtimali, ruzgar, pm10):
    if yagis_ihtimali >= 40:
        durum = "🌧️ Yağmurlu"
    elif yagis_ihtimali >= 15:
        durum = "☁️ Kapalı / Çisenti"
    elif ruzgar > 22:
        durum = "💨 Rüzgarlı"
    elif sicaklik > 25:
        durum = "☀️ Güneşli"
    else:
        durum = "⛅ Parçalı Bulutlu"

    tavsiyeler = []
    if yagis_ihtimali >= 15:
        tavsiyeler.append("☔ Yağış ihtimali var, şemsiyeni yanına almayı unutma.")
    if ruzgar > 22:
        tavsiyeler.append("💨 Şiddetli rüzgara karşı dikkatli ol.")
    if pm10 > 45:
        tavsiyeler.append("😷 Hava kalitesi düşük (PM10 yüksek), dışarı çıkarken maske takman iyi olabilir.")
    if sicaklik > 30:
        tavsiyeler.append("🧴 Hava çok sıcak! Güneş kremi sür ve bol sıvı tüket.")
    elif sicaklik < 15:
        tavsiyeler.append("🧥 Hava soğuk, kalın giyinmelisin.")
        
    if not tavsiyeler:
        tavsiyeler.append("🌟 Hava harika, dışarıda vakit geçirmek için çok uygun!")
        
    tavsiye_metni = " | ".join(tavsiyeler)
    return durum, tavsiye_metni

def tum_tahminleri_uret(yil, ay, gun, yil_gunu):
    # Modelleri her tahmin anında diskten okuyoruz her seferinde yeniden eğitmemek için!
    dizin = os.path.dirname(os.path.abspath(__file__))
    modeller = {
        'pm10': joblib.load(os.path.join(dizin, 'pm10_uzmani.pkl')),
        'pm25': joblib.load(os.path.join(dizin, 'pm25_uzmani.pkl')),
        'max_sic': joblib.load(os.path.join(dizin, 'en yüksek sicaklik_uzmani.pkl')),
        'min_sic': joblib.load(os.path.join(dizin, 'en dusuk sicaklik_uzmani.pkl')),
        'yagis': joblib.load(os.path.join(dizin, 'yagis_uzmani.pkl')),
        'ruzgar': joblib.load(os.path.join(dizin, 'ruzgar_hizi_uzmani.pkl'))
    }
    
    max_t = modeller['max_sic'].predict([[yil, ay, gun, yil_gunu]])[0]
    
    min_t = modeller['min_sic'].predict([[yil, ay, gun, yil_gunu, max_t]])[0]
    
    ruz = modeller['ruzgar'].predict([[yil, ay, gun, yil_gunu, max_t, min_t]])[0]
    
    yag_mm = modeller['yagis'].predict([[yil, ay, gun, yil_gunu, max_t, min_t, ruz]])[0]
    
    p10 = modeller['pm10'].predict([[yil, ay, gun, yil_gunu, max_t, min_t, ruz, yag_mm]])[0]
    
    p25 = modeller['pm25'].predict([[yil, ay, gun, yil_gunu, max_t, min_t, ruz, yag_mm]])[0] 


    yag_ihtimali = min(yag_mm * 15, 100.0) 
    if yag_ihtimali < 3.0:
        yag_ihtimali = 0.0

    durum, tavsiye = hava_durumu_yorumu(max_t, yag_ihtimali, ruz, p10)
    

    return {
        'max_t': max_t,
        'min_t': min_t,
        'yag': yag_ihtimali, 
        'ruz': ruz,
        'p10': p10,
        'p25': p25,
        'durum': durum,
        'tavsiye': tavsiye
    }