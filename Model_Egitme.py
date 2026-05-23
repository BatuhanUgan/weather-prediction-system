import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'izmir_havadurum.csv')
df = pd.read_csv(csv_path)

sutun_isimleri = ['Tarih', 'En_Yuksek_Derece', 'En_Dusuk_Derece', 'Yagis_Orani', 'Ruzgar_Hizi', 'Ay', 'Hafta_Sonu_Kontrol', '1_Gun_Onceki_En_Yuksek_Derece', '2_Gun_Onceki_En_Yuksek_Derece', '3_Gun_Onceki_En_Yuksek_Derece', 'Kalin_Partikul_Orani', 'Ince_Partikul_Orani', '1_Gun_Onceki_Kalin_Partikul_Orani', '1_Gun_Onceki_Ince_Partikul_Orani', '2_Gun_Onceki_Kalin_Partikul_Orani', '2_Gun_Onceki_Ince_Partikul_Orani', '3_Gun_Onceki_Kalin_Partikul_Orani', '3_Gun_Onceki_Ince_Partikul_Orani']

df.columns = sutun_isimleri

df['Tarih'] = pd.to_datetime(df['Tarih'])
df['Yil'] = df['Tarih'].dt.year
df['Ay'] = df['Tarih'].dt.month
df['Gun'] = df['Tarih'].dt.day
df['Yil_Gunu'] = df['Tarih'].dt.dayofyear
df = df.dropna()

aylik_max_ortalamalar = df.groupby('Ay')['En_Yuksek_Derece'].mean()
aylik_min_ortalamalar = df.groupby('Ay')['En_Dusuk_Derece'].mean()

df['Aylik_Max_Ortalama'] = df['Ay'].map(aylik_max_ortalamalar)
df['Aylik_Min_Ortalama'] = df['Ay'].map(aylik_min_ortalamalar)

# HEATMAP 
# Değişkenlerin birbirini nasıl etkilediğini gösterir.
plt.figure(figsize=(10, 8))
korelasyon_sutunlari = ['En_Yuksek_Derece', 'En_Dusuk_Derece', 'Yagis_Orani', 'Ruzgar_Hizi', 'Kalin_Partikul_Orani', 'Ince_Partikul_Orani']
corr = df[korelasyon_sutunlari].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=1)
plt.title("İzmir Hava Durumu: Değişkenler Arası Korelasyon (Heatmap)")
plt.tight_layout()
plt.savefig("1_korelasyon_heatmap.png", dpi=300)
plt.show()

# SCATTER PLOT 
# Doğadaki mevsimsel döngüyü görsel olarak gösterir.
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='En_Dusuk_Derece', y='En_Yuksek_Derece', hue='Ay', palette='twilight_shifted', s=70, alpha=0.8)
plt.title("Aylara Göre İzmir Min. ve Max. Sıcaklık Dağılımı (Scatter Plot)")
plt.xlabel("Minimum Sıcaklık (°C)")
plt.ylabel("Maksimum Sıcaklık (°C)")
plt.legend(title="Aylar", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("2_sicaklik_scatter.png", dpi=300)
plt.show()

# 3. BAR & LINE PLOT (Aylık Ortalama Sıcaklık ve Yağış İlişkisi)
# Aynı grafik üzerinde hem çubuk hem çizgi grafik kullanarak bir görntü çıkartır.
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx() 

# Yağış için Bar Grafiği 
sns.barplot(x='Ay', y='Yagis_Orani', data=df, ax=ax1, color='skyblue', alpha=0.6, errorbar=None)

# Sıcaklık için Çizgi Grafiği
sns.lineplot(x=df['Ay']-1, y='En_Yuksek_Derece', data=df, ax=ax2, color='crimson', marker='o', linewidth=2.5, errorbar=None)

ax1.set_ylabel('Ortalama Yağış Oranı', color='teal', fontweight='bold')
ax2.set_ylabel('Ortalama Maksimum Sıcaklık (°C)', color='crimson', fontweight='bold')
plt.title("İzmir: Aylara Göre Ortalama Sıcaklık ve Yağış Trendi")
plt.tight_layout()
plt.savefig("3_aylik_trend.png", dpi=300)
plt.show()

df = df.dropna()


## Egitme ve Metrik Değerlerlendirme Fonksiyonu

def model_secimi(X, y, hedef_isim):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modeller = {
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Linear Regression": LinearRegression(),
        "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
        "SVR": SVR(kernel='rbf'),
        "KNN": KNeighborsRegressor(n_neighbors=5)
    }

    skorlar = []

    for isim, model in modeller.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # 4 Metrik
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        skorlar.append({
            "Model": isim,
            "R2_Score": r2,
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse
        })

    sonuc_df = pd.DataFrame(skorlar).sort_values(by="R2_Score", ascending=False)
    print(f"\n--- {hedef_isim} Sonuçları ---")
    print("\n EN ÜSTEKI MODELIMIZ EN BASIRLISIDIR!")
    print(sonuc_df.to_string(index=False))
    
    # En iyiyi kaydet
    en_iyi_isim = sonuc_df.iloc[0]['Model']
    en_iyi_model = modeller[en_iyi_isim]
    joblib.dump(en_iyi_model, f'{hedef_isim.lower()}_uzmani.pkl')
    
    
    # MODEL ÖĞRENME VE DEĞERLENDİRME GRAFİKLERİ
    # En kritik 2 hedef için (Max Sıcaklık ve PM10) grafik çizdiriyoruz:
    
    if hedef_isim in ["En Yüksek Sicaklik", "PM10"]:
        plt.figure(figsize=(14, 5))
        
        # 1. Grafik: Model Başarılarının (R2) Kıyaslanması
        plt.subplot(1, 2, 1)
        sns.barplot(x="R2_Score", y="Model", data=sonuc_df, palette="mako")
        plt.title(f"{hedef_isim} Tahmini: Algoritma Yarışı (R² Skorları)")
        plt.xlabel("Başarı Oranı (R² - 1'e ne kadar yakınsa o kadar iyi)")
        plt.ylabel("Algoritmalar")
        plt.xlim(0, 1.05) # R2 skoru genelde 0-1 arasıdır
        
        # 2. Grafik: Şampiyon Modelin Gerçek ve Tahmin Değerleri (Scatter)
        plt.subplot(1, 2, 2)
        y_pred_en_iyi = en_iyi_model.predict(X_test)
        sns.scatterplot(x=y_test, y=y_pred_en_iyi, alpha=0.6, color='darkorange', edgecolor=None)
        
        # İdeal Doğru Çizgisi
        # Noktalar bu çizgiye ne kadar yakınsa, model o kadar iyi tahmin yapmış demektir.
        min_val = min(y_test.min(), y_pred_en_iyi.min())
        max_val = max(y_test.max(), y_pred_en_iyi.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Kusursuz Tahmin Çizgisi')
        
        plt.title(f"Şampiyon Model ({en_iyi_isim}): Gerçek vs Tahmin")
        plt.xlabel("Verisetindeki Gerçek Değerler")
        plt.ylabel("Modelin Ürettiği Tahminler")
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{hedef_isim}_model_ogrenmesi.png", dpi=300)
        plt.show()
    
    return sonuc_df

## PM Tahmini

pm_features = ['Yil', 'Ay', 'Gun', 'Yil_Gunu', 'En_Yuksek_Derece', 'En_Dusuk_Derece', 'Ruzgar_Hizi', 'Yagis_Orani']
model_secimi(df[pm_features], df['Kalin_Partikul_Orani'], "PM10")
model_secimi(df[pm_features], df['Ince_Partikul_Orani'], "PM25")

## Max Sicaklik Tahmini

max_sicaklik_features = [
    'Yil', 'Ay', 'Gun', 'Yil_Gunu'
]

X_max_sicaklik = df[max_sicaklik_features]
y_max_sicaklik = df['En_Yuksek_Derece']

model_secimi(X_max_sicaklik, y_max_sicaklik, "En Yüksek Sicaklik")

## Min Sicaklik Tahmini

min_sicaklik_features = [
    'Yil', 'Ay', 'Gun', 'Yil_Gunu', 'En_Yuksek_Derece'
]

X_min_sicaklik = df[min_sicaklik_features]
y_min_sicaklik = df['En_Dusuk_Derece']

model_secimi(X_min_sicaklik, y_min_sicaklik, "En Dusuk Sicaklik")

## Yagis Tahmini

yagis_features = [
    'Yil', 'Ay', 'Gun', 'Yil_Gunu', 'En_Yuksek_Derece', 'En_Dusuk_Derece', 'Ruzgar_Hizi'
]

X_yagis = df[yagis_features]
y_yagis = df['Yagis_Orani']

model_secimi(X_yagis, y_yagis, "Yagis")

## Rüzgar Hizi Tahmini

ruzgar_features = [
    'Yil', 'Ay', 'Gun', 'Yil_Gunu', 'En_Yuksek_Derece', 'En_Dusuk_Derece'
]

X_ruzgar = df[ruzgar_features]
y_ruzgar = df['Ruzgar_Hizi']

model_secimi(X_ruzgar, y_ruzgar, "Ruzgar_Hizi")
