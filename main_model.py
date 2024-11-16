import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression

data = pd.read_csv("car_sales_augmented.csv")

data['Website_post_date'] = pd.to_datetime(data['Website_post_date'], format='%d.%m.%y', errors='coerce')
data['Sell_date'] = pd.to_datetime(data['Sell_date'], format='%d.%m.%y', errors='coerce')

data['Days_to_sell'] = (data['Sell_date'] - data['Website_post_date']).dt.days
data['Days_to_sell'] = data['Days_to_sell'].fillna(-1)

data['Month'] = data['Website_post_date'].dt.month
data['Quarter'] = data['Website_post_date'].dt.quarter

categorical_cols = ['Car_make', 'Model', 'Transmission', 'Options', 'Color', 'Damage', 'Body_style', 'Fuel_type']
data_dummified = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

price_features_dummified = [col for col in data_dummified.columns if col not in ['Estimated_price', 'Days_to_sell', 'Website_post_date', 'Sell_date']]
sell_time_features_dummified = price_features_dummified + ['Estimated_price']

X_price = data_dummified[price_features_dummified]
y_price = data_dummified['Estimated_price']
X_price_train, X_price_test, y_price_train, y_price_test = train_test_split(X_price, y_price, test_size=0.2, random_state=42)

X_sell_time = data_dummified[data_dummified['Days_to_sell'] >= 0][sell_time_features_dummified]
y_sell_time = data_dummified[data_dummified['Days_to_sell'] >= 0]['Days_to_sell']
X_sell_time_train, X_sell_time_test, y_sell_time_train, y_sell_time_test = train_test_split(X_sell_time, y_sell_time, test_size=0.2, random_state=42)

def train_and_evaluate_model(regressor, X_train, y_train, X_test, y_test):
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return {"MAE": mae, "MSE": mse, "R2": r2}

param_grid = {
    'alpha': [0.01, 0.1, 1.0, 10.0, 100.0],
    'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
}
elastic_net = ElasticNet(random_state=42)
grid_search = GridSearchCV(
    estimator=elastic_net,
    param_grid=param_grid,
    scoring='neg_mean_absolute_error',
    cv=5,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_price_train, y_price_train)

best_params = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = -grid_search.best_score_

test_predictions = best_model.predict(X_price_test)
mae = mean_absolute_error(y_price_test, test_predictions)
mse = mean_squared_error(y_price_test, test_predictions)
r2 = r2_score(y_price_test, test_predictions)

print("Best Parameters for ElasticNet:", best_params)
print("Best Cross-Validated MAE:", best_score)
print("ElasticNet Test Set Performance:")
print(f"MAE: {mae}, MSE: {mse}, R²: {r2}")

try:
    from catboost import CatBoostRegressor
    sell_time_model = CatBoostRegressor(random_state=42, verbose=0)
    sell_time_performance = train_and_evaluate_model(
        sell_time_model, X_sell_time_train, y_sell_time_train, X_sell_time_test, y_sell_time_test
    ) 
    print("\nCatBoost Sell Time Performance:", sell_time_performance)
except ImportError:
    print("CatBoost is not installed. Skipping Sell Time Prediction.")
