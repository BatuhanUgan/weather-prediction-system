# İzmir Akıllı Hava Durumu Tahmin ve Uyarı Sistemi 

## Proje Özeti
Sıcaklık, yağış ihtimali, rüzgar hızı ve hava kalitesi (PM10 ve PM2.5) parametrelerini yüksek doğrulukla öngörmek amacıyla geliştirilmiş güçlü bir makine öğrenmesi modelidir. Sistem, isabetli tahminler sunmak için 2024-2026 yıllarına ait tarihsel hava durumu verilerini analiz etmektedir.

## Metodoloji ve Sistem Mimarisi
* **Yazılım Yaşam Döngüsü:** Yapılandırılmış ve planlı bir geliştirme süreci sağlamak amacıyla uçtan uca Şelale (Waterfall) mimarisi uygulanmıştır.
* **Modelleme Yaklaşımı:** Model tekrarlarının önüne geçmek ve zaman içindeki kararlılığı artırmak amacıyla, çekirdek sistem mimarisi kesin bir şekilde **Zaman Serisi Trend Analizi** kullanılarak optimize edilmiştir.

## Hedefe Özel Performans ve Metrikler
* **Maksimum Sıcaklık**
  * R² Skoru: 0.95 | MAE: 1.51 | RMSE: 2.0
* **Minimum Sıcaklık**
  * R² Skoru: 0.95 | MAE: 1.28 | RMSE: 1.65
* **PM10 Hava Kalitesi**
  * R² Skoru: 0.90 | MAE: 3.62 | RMSE: 4.45

## Görselleştirmeler
Proje deposu, temel veri analizi ve performans grafiklerini içermektedir:
* `1_korelasyon_heatmap.jpg`: Özellik korelasyon analizi.
* `PM10_model_ogrenmesi.jpg`: Model öğrenme eğrisi ve tahmin doğruluğu.

## Kullanılan Teknolojiler
* **Dil:** Python
* **Kütüphaneler:** Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn, XGboost, Joblib, Streamlit

## Dokümantasyon
Bu projenin daha detaylı metrikleri, teorik arka planı ve mimari dökümü için [Proje Raporu](./Weather%20Prediction%20Raporu.pdf) dosyasının tam sürümünü inceleyebilirsiniz.

## Kurulum ve Çalıştırma
1. Proje deposunu yerel makinenize klonlayın.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt

streamlit run Main.py

## Demo
![Uygulama Demosu](./Demo.gif)
