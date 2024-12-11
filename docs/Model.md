# Model Documentation

This documentation provides an overview of the train.py script, which predicts:
1. The estimated price of a car based on various features using ElasticNet regression.
2. The days required to sell a car using CatBoost regression.

## Workflow
1. Data Preprocessing:
   - Load data from a CSV file3.
   - Convert date columns and create time-related features.
   - Perform log transformation for numerical stability and better model performance.
2. Feature Engineering:
   - One-hot encode categorical variables.
   - Create dummy variables to represent categorical data.
3. Model Training and Evaluation:
   - Train an ElasticNet model to predict car prices.
   - Train a CatBoost regressor to predict days to sell using features and predicted prices.
4. Model Saving:
   - Save trained models using pickle for future use.

---

## Dependencies
The following Python libraries are required:
- pandas
- numpy
- scikit-learn
- catboost
- dotenv
- sqlalchemy
- pickle

Install these libraries using:
pip install pandas numpy scikit-learn catboost python-dotenv sqlalchemy
...---

## Data Preprocessing

### Input Data
- Columns Required:
  - Website_post_date: The date the car listing was posted.
  - Sell_date: The date the car was sold.
  - Estimated_price: The price of the car.
  - Categorical features: Car_make, Model, Transmission, Options, Color, Damage, Body_style, Fuel_type.

### Steps:
1. Date Conversion: Convert Website_post_date and Sell_date to datetime format.
2. Feature Creation: Compute Days_to_sell as the difference between Sell_date and Website_post_date.
3. Log Transformation: Apply log transformation to Estimated_price for numerical stability.
4. One-Hot Encoding: Transform categorical features into dummy variables using pd.get_dummies.

---

## Models

### 1. Price Prediction Model (ElasticNet)

#### Description
Predicts the car's price based on input features using the ElasticNet regression algorithm.

#### Features
- Car attributes such as make, model, mileage, fuel type, etc.

#### Methods
- train_and_evaluate_model(regressor, X_train, y_train, X_test, y_test):
  - Trains a regression model and evaluates its performance.
  - Parameters: 
    - regressor: Regression model instance.
    - X_train: Training feature set.
    - y_train: Training target variable.
    - X_test: Testing feature set.
    - y_test: Testing target variable.
  - Returns: The trained model, performance metrics (MAE, MSE, R2), and predictions.

---

### 2. Days to Sell Prediction Model (CatBoost)

#### Description
Predicts the number of days it will take to sell a car based on input features and predicted price.

#### Features
- Car attributes and the predicted price from the price prediction model.

#### Methods
- train_and_evaluate_model(regressor, X_train, y_train, X_test, y_test):
  - Trains a regression model and evaluates its performance (used for CatBoost).
  - Parameters: 
    - regressor: Regression model instance.
    - X_train: Training feature set.
    - y_train: Training target variable.
    - X_test: Testing feature set.
    - y_test: Testing target variable.
  - Returns: The trained model, performance metrics (MAE, MSE, R2), and predictions.

---

## Prediction Workflow

1. Train the ElasticNet model using the historical data (train_and_evaluate_model function).
   - Use the resulting predicted prices as input for the CatBoost model.
2. Train the CatBoost model using the features and predicted prices from the ElasticNet model.

---

## Script Execution

### train.py

The script responsible for training the models.

#### Steps:
1. Load and preprocess the data.
2. Train the ElasticNet model for price prediction using the train_and_evaluate_model function.
3. Use predicted prices to train the CatBoost model for days-to-sell prediction using train_and_evaluate_model.
4. Save both models as .pkl files for future use.

#### Running the Script
Ensure all dependencies are installed and input data is available. Then execute:
python train.py
...---

## Model Saving
The trained models are saved as .pkl files for reuse:
1. ElasticNet Model: Saved as elastic_net_price_model.pkl.
2. CatBoost Model: Saved as catboost_sell_time_model.pkl.

These files are stored in the ./models/ directory.

