# Austin 311 Service Demand: Statistical Analysis & Prediction

**Analyzing historical service requests, calendar patterns, and weather to understand and predict daily 311 demand in Austin, Texas.**

## Project Overview

Can historical service demand, calendar patterns, and weather conditions help explain and predict the number of 311 service requests Austin receives each day?

This project explores that question using more than 2 million Austin 311 service records combined with historical weather data from NOAA.

The analysis examines daily demand patterns, investigates relationships between service requests and potential predictors, and compares three regression-based prediction approaches using chronological training and testing periods.

The objective is not just to build a predictive model, but to evaluate whether its predictions generalize to unseen data and whether they are reliable enough to inform operational planning.

## Business Problem

Municipal service teams need to understand how service demand changes over time to support resource planning and operational decisions.

Understanding daily request patterns can help identify periods of higher demand and assess whether historical trends provide useful information for anticipating future service volumes.

This project investigates whether historical demand, calendar features, and weather variables can support one-day-ahead predictions of Austin 311 service requests.

## Data Sources

**1. Austin 311 Public Data**

- Source: City of Austin Open Data Portal
- Dataset: [Austin 311 Public Data](https://data.austintexas.gov/City-Government/Austin-311-Public-Data/xwdj-i9he)
- Dataset ID: `xwdj-i9he`
- Original dataset: More than 2 million service request records.
- Used to calculate daily service request volumes.

**2. Historical Weather Data**

- Source: NOAA National Centers for Environmental Information
- Dataset: GHCN-Daily
- Weather station: Austin Camp Mabry, Texas (`USW00013958`)
- Used weather variables: average, maximum and minimum temperature, precipitation, and average wind speed.

## Tools & Technologies

- **Programming:** Python
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib
- **Statistical Modeling:** Statsmodels
- **Machine Learning:** Scikit-learn
- **Environment:** Jupyter Notebook, Anaconda
- **Data Sources:** City of Austin Open Data Portal, NOAA

## Project Workflow

### 1. Data Collection and Preparation

- Retrieved more than 2 million Austin 311 service records.
- Parsed service request timestamps and aggregated records into daily request counts.
- Retrieved historical daily weather observations from NOAA.
- Cleaned and prepared weather variables, handled missing observations, and merged demand and weather data by date.
- Created calendar and historical demand features for analysis and prediction.

### 2. Exploratory Data Analysis

Investigated daily, weekly, and monthly demand patterns and explored relationships between service request volumes and weather conditions.

Key observations:

- Average weekday demand was approximately 720 requests per day, compared with approximately 424 on weekends.
- Weekday demand was approximately 41% higher than weekend demand.
- Daily request volumes varied substantially across years.
- Temperature showed a modest positive correlation with daily demand, while precipitation and wind had very weak linear correlations.

### 3. Feature Engineering

Created features to capture historical demand patterns and calendar effects:

- Previous day's request volume (`lag_1`)
- Request volume seven days earlier (`lag_7`)
- Seven-day rolling average of historical demand (`rolling_7`)
- Day of week, month, and year
- Daily temperature, precipitation, and wind speed

Lag and rolling features were shifted to ensure that only information available before the prediction date was used.

### 4. Predictive Modeling

Compared three approaches:

1. **Persistence Baseline:** Uses the previous day's actual request volume as the prediction.
2. **Simple Linear Regression:** Uses previous day's request volume as the predictor.
3. **Multiple Linear Regression:** Incorporates historical demand, calendar, and weather features.

Models were trained on data from 2018–2024 and evaluated on the unseen 2025 test period.

The selected candidate was subsequently evaluated on a separate 2026 holdout period.

### 5. Model Evaluation

Used the following metrics:

- **MAE (Mean Absolute Error):** Average absolute difference between actual and predicted request counts.
- **RMSE (Root Mean Squared Error):** Measures prediction error while penalizing larger errors more heavily.
- **R² (Coefficient of Determination):** Measures how much variation in the target is explained by the model relative to a mean-based prediction.

## Results

### 2025 Model Comparison

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Persistence Baseline | 180.71 | 245.56 | -0.083 |
| Simple Linear Regression | **172.37** | **229.28** | **0.056** |
| Multiple Linear Regression | 262.54 | 288.07 | -0.491 |

Simple Linear Regression was selected as the best-performing candidate based on the 2025 comparison.

### 2026 Final Holdout Evaluation

The selected Simple Linear Regression model was evaluated on January 1 through September 17, 2026.

| Metric | Result |
|---|---:|
| MAE | 167.59 |
| RMSE | 233.20 |
| R² | -0.095 |

Although the average absolute error was similar to the 2025 test period, the negative R² indicates that the model did not outperform a simple prediction based on average demand for the 2026 holdout period.

## Key Findings and Business Takeaways

- Historical service demand and calendar patterns reveal meaningful differences in daily service volumes.
- Weekday and weekend demand differences provide useful context for operational planning.
- The more complex multiple regression model performed substantially worse on unseen data despite strong training performance.
- The relationship between consecutive days' demand varied across years, suggesting temporal instability and the possibility of concept drift.
- Historical demand and weather alone were not sufficient to produce consistently reliable daily forecasts with the approaches evaluated.

**Business recommendation:** The evaluated models are not recommended for operational forecasting in their current form. Historical demand patterns can still inform service-demand monitoring, while future predictive work should incorporate additional operational information and demonstrate consistent out-of-sample performance.

## Limitations and Future Work

This project is observational and does not establish causal relationships between weather, calendar patterns, and service demand.

Additional limitations include:

- Predictions use the previous day's actual request volume, making this a one-day-ahead forecasting exercise rather than a long-range planning model.
- Demand patterns changed across evaluation periods.
- The 2026 holdout covers only January 1 through September 17, 2026.
- Available predictors may not capture all operational factors affecting service demand.

Potential future improvements:

- Incorporate service request categories and unresolved request backlogs.
- Explore holidays, major events, and staffing information.
- Evaluate rolling-window model retraining to adapt to changing demand patterns.
- Monitor temporal stability and model performance across future evaluation periods.

## Repository Structure

```text
Austin_311_Demand_Project/
│
├── data/
│   ├── austin_311.csv
│   ├── austin_311_daily.csv
│   ├── austin_weather.csv
│   └── austin_311_model.csv
│
├── notebooks/
│   └── Austin_311_Demand_Analysis.ipynb
│
├── README.md
└── requirements.txt
```

## How to Run the Project

1. Clone this repository:

   ```bash
   git clone <your-github-repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd Austin_311_Demand_Project
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure the required datasets are available in the `data/` directory.

5. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

6. Open `notebooks/Austin_311_Demand_Analysis.ipynb` and run the analysis.

*Note: If raw or processed datasets are not included in the repository, obtain them from the sources listed above and place the required files in the `data/` directory.*

## Disclaimer

This is an independent portfolio project using publicly available City of Austin and NOAA datasets. It is not an official City of Austin project, commissioned analysis, or deployed forecasting system.
