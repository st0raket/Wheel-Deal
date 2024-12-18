"""
Car Sales Prediction Script
This script predicts two key metrics:
1. Estimated Price of a car based on various features using ElasticNet regression.
2. Days required to sell a car based on features and predicted price using CatBoost regression.

Workflow:
1. Data preprocessing: Load data, convert date columns, create time-related features, and perform log transformation.
2. Feature engineering: One-hot encoding of categorical variables and creation of dummy variables.
3. Model training and evaluation:
   - ElasticNet for price prediction.
   - CatBoost for days-to-sell prediction.
4. Model saving: Save trained models for future use.

Modules and Libraries:
- pandas, numpy: For data manipulation and transformations.
- scikit-learn: For model training, evaluation, and splitting data.
- catboost: For training the regression model for days-to-sell prediction.
- pickle: For saving trained models to disk.
- dotenv: For loading environment variables.
- sqlalchemy: For database connection and data retrieval.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet
from catboost import CatBoostRegressor
from dotenv import load_dotenv
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
import pickle

data = pd.read_csv("car_sales_augmented.csv")

# Convert dates and create time-related features
data['Website_post_date'] = pd.to_datetime(data['Website_post_date'], format='%d.%m.%y', errors='coerce')
data['Sell_date'] = pd.to_datetime(data['Sell_date'], format='%d.%m.%y', errors='coerce')
data['Days_to_sell'] = (data['Sell_date'] - data['Website_post_date']).dt.days
data['Days_to_sell'] = data['Days_to_sell'].fillna(-1)

# Log transformation for Estimated_price
data['Log_Estimated_price'] = np.log1p(data['Estimated_price'])

# One-hot encode categorical columns
categorical_cols = ['Car_make', 'Model', 'Transmission', 'Options', 'Color', 'Damage', 'Body_style', 'Fuel_type']
data_dummified = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Features for price prediction
price_features_dummified = [col for col in data_dummified.columns if col not in ['Estimated_price', 'Log_Estimated_price', 'Days_to_sell', 'Website_post_date', 'Sell_date']]
X_price = data_dummified[price_features_dummified]
y_price = data_dummified['Log_Estimated_price']
X_price_train, X_price_test, y_price_train, y_price_test = train_test_split(X_price, y_price, test_size=0.2, random_state=42)

def train_and_evaluate_model(regressor, X_train, y_train, X_test, y_test):
    """
    Train a regression model and evaluate its performance.

    Parameters:
    - regressor: A regression model instance.
    - X_train (pd.DataFrame): Training feature set.
    - y_train (pd.Series): Training target variable.
    - X_test (pd.DataFrame): Testing feature set.
    - y_test (pd.Series): Testing target variable.

    Returns:
    - regressor: Trained regression model.
    - dict: Model performance metrics (MAE, MSE, R2).
    - np.array: Predictions on the test set.
    """
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return regressor, {"MAE": mae, "MSE": mse, "R2": r2}, predictions

# Price Prediction Model
elastic_net = ElasticNet(random_state=42, alpha=0.1, l1_ratio=0.5)
price_model, elastic_net_performance, price_predictions = train_and_evaluate_model(elastic_net, X_price_train, y_price_train, X_price_test, y_price_test)

# Add predicted price as a feature for sell time prediction
data_dummified['Predicted_Log_Price'] = np.nan
data_dummified.loc[X_price_test.index, 'Predicted_Log_Price'] = price_predictions
data_dummified['Predicted_Log_Price'] = data_dummified['Predicted_Log_Price'].fillna(data_dummified['Log_Estimated_price'])

sell_time_features_dummified = price_features_dummified + ['Predicted_Log_Price']
X_sell_time = data_dummified[data_dummified['Days_to_sell'] >= 0][sell_time_features_dummified]
y_sell_time = data_dummified[data_dummified['Days_to_sell'] >= 0]['Days_to_sell']
X_sell_time_train, X_sell_time_test, y_sell_time_train, y_sell_time_test = train_test_split(X_sell_time, y_sell_time, test_size=0.2, random_state=42)

# Days to Sell Prediction Model
catboost_model = CatBoostRegressor(random_state=42, verbose=0)
sell_time_model, catboost_performance, sell_time_predictions = train_and_evaluate_model(catboost_model, X_sell_time_train, y_sell_time_train, X_sell_time_test, y_sell_time_test)

# Output Results
print("\n--- Price Prediction ---")
print("Elastic Net Performance:", elastic_net_performance)

print("\n--- Days to Sell Prediction ---")
print("CatBoost Performance:", catboost_performance)

try:
    # Save ElasticNet model for price prediction
    dir = "./models/"
    price_model_filename = dir + "elastic_net_price_model.pkl"
    with open(price_model_filename, "wb") as file:
        pickle.dump(price_model, file)

    # Save CatBoost model for days to sell prediction
    sell_time_model_filename = dir + "catboost_sell_time_model.pkl"
    with open(sell_time_model_filename, "wb") as file:
        pickle.dump(sell_time_model, file)

    print(f"Price prediction model saved as {price_model_filename}")
    print(f"Days to sell prediction model saved as {sell_time_model_filename}")

except NameError as e:
    print(f"Error: {e}. Ensure the models are defined before saving.")
