# İzmir Intelligent Weather Forecast and Warning System 🌤️📊

## Project Overview
A robust machine learning model developed to forecast temperature, precipitation chance, wind speed, and air quality (PM10 and PM2.5) with high accuracy. The system analyzes historical weather data from 2024 to 2026 to provide predictive insights.

## Methodology & Architecture
* **Development Life Cycle:** Waterfall Architecture was implemented end-to-end to ensure structured development.
* **Modeling Approach:** To prevent model repetition and increase stability over time, the core system architecture is strictly optimized using **Time Series Trend Analysis**.

## Target-Specific Performance & Metrics
* **Max Temperature**
  * R² Score: 0.95 | MAE: 1.51 | RMSE: 2.0
* **Min Temperature**
  * R² Score: 0.95 | MAE: 1.28 | RMSE: 1.65
* **PM10 Air Quality**
  * R² Score: 0.90 | MAE: 3.62 | RMSE: 4.45

## Visualizations
The repository includes key data analysis and performance plots:
* `1_korelasyon_heatmap.jpg`: Feature correlation analysis.
* `PM10_model_ogrenmesi.jpg`: Model learning curve and prediction accuracy.

## Tech Stack
* **Language:** Python
* **Libraries:** Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn, XGboost, Joblib, Streamlit

## Documentation
For more detailed metrics, theoretical background, and an architectural breakdown, you can review the full [Project Report](./Weather%20Prediction%20Raporu.pdf).

## How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

streamlit run Main.py

## Demo
![Application Demo](./Demo.gif)
