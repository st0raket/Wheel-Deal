# Model Service Documentation

## Overview

This service handles the prediction of car prices and the estimated days required to sell a car based on various car attributes. The model uses ElasticNet regression for predicting the car's price and CatBoost regression for estimating the number of days it will take to sell the car.

The model service includes two main components:

- **Price Prediction Model**: Predicts the car's price based on features like make, model, mileage, etc.
- **Days to Sell Prediction Model**: Predicts the number of days it will take to sell the car.

Both models are saved as pickle files for reuse after training.

## Features


 **Price Prediction Model**

   - **Description**: Predicts the price of a car based on various features.
   - **Algorithm**: ElasticNet regression.
   - **Inputs**: Car attributes like make, model, mileage, fuel type, etc.
   - **Outputs**: Predicted car price.

 **Days to Sell Prediction Model**
 
   - **Description**: Predicts the number of days it will take to sell a car based on features.
   - **Algorithm**: CatBoost regression.
   - **Inputs**: Car features and predicted price.
   - **Outputs**: Predicted days to sell the car.

## Models

### 1. **Price Prediction Model (ElasticNet)**

This model predicts the car's price based on input features using the ElasticNet regression algorithm.

#### Methods:
- **trainPriceModel(carData)**
    - **Description**: Trains the price prediction model using historical car sales data.
    - **Parameters**: `carData` (DataFrame containing car features and prices).
    - **Returns**: The trained model and performance metrics (MAE, MSE, R2).
    - **Example Usage**:
        ```javascript
        const trainedPriceModel = trainPriceModel(carData);
        ```

### 2. **Days to Sell Prediction Model (CatBoost)**

This model predicts the number of days it will take to sell a car based on input features and predicted price.

#### Methods:
- **trainSellTimeModel(carData, pricePredictions)**
    - **Description**: Trains the sell time prediction model based on car features and predicted prices.
    - **Parameters**: 
        - `carData` (DataFrame containing car features).
        - `pricePredictions` (Array of predicted car prices from the price model).
    - **Returns**: The trained model and performance metrics (MAE, MSE, R2).
    - **Example Usage**:
        ```javascript
        const trainedSellTimeModel = trainSellTimeModel(carData, pricePredictions);
        ```

### 3. **Prediction Service**

The `PredictionService` uses the trained models to make predictions based on user-provided car properties.

#### Methods:

- **getPredictionResults(carProperties)**
    - **Description**: Predicts car price and days to sell based on the provided car properties.
    - **Parameters**: 
        - `carProperties`: An object containing car features like make, model, mileage, etc.
    - **Returns**: A Promise that resolves to an object with predicted car details (price and days to sell).
    - **Example Usage**:
        ```javascript
        const predictionService = new PredictionService();
        predictionService.getPredictionResults(carProperties)
            .then(predictionResults => {
                console.log(predictionResults);
            });
        ```

    - **Example Response**:
    ```javascript
    {
        price: 10000,
        daysToSell: 14
    }
    ```

## Options Service

The `OptionsService` provides available options for car attributes such as make, model, transmission, and more. These options are used to populate dropdowns in the UI.

### Methods:

- **getOptionsBySelectId(selectId)**
    - **Description**: Fetches the available options for a specific car attribute based on the `selectId`.
    - **Parameters**:
        - `selectId`: The ID of the select input for which options need to be fetched.
    - **Returns**: A Promise that resolves to a list of options.
    - **Example Usage**:
        ```javascript
        const optionsService = new OptionsService();
        optionsService.getOptionsBySelectId("make-select")
            .then(options => {
                console.log(options);
            });
        ```

    - **Example Response**:
    ```javascript
    [
        { id: 1, name: "Ford" },
        { id: 2, name: "Toyota" },
        { id: 3, name: "BMW" }
    ]
    ```

## Main Interface

### index.js

The `index.js` file handles user interactions, collecting form data, calling the prediction service, and displaying the results.

#### Key Functions:

1. **populateSelect(selectId, options)**
    - Populates a dropdown with available options for a specific car attribute.

2. **collectFormData()**
    - Gathers selected values from the form to be passed to the prediction service.

3. **showPredictionResults(predictionResults)**
    - Displays the prediction results (price and days to sell).


