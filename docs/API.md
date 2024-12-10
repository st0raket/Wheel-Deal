# API Documentation

This document provides an overview of the available API endpoints for the Wheel-Deal service, which estimates car sale prices and provides related functionality.

## Endpoints

### 1. `GET /make-options`
#### Description:
Retrieve a list of car makes available in the system.

#### Response:
- **200 OK**: A list of car makes.

#### Example Response:
A list of available car makes like BMW, Chevrolet, and Ford.

---

### 2. `GET /model-options/{makeId}`
#### Description:
Retrieve a list of car models for a specific car make.

#### Parameters:
- `makeId`: The ID of the car make (e.g., `1` for BMW).

#### Response:
- **200 OK**: A list of models for the specified make.

---

### 3. `GET /color-options`
#### Description:
Retrieve a list of available car colors.

#### Response:
- **200 OK**: A list of car colors such as Black, White, and Red.

---

### 4. `POST /predict-price`
#### Description:
Predict the sale price of a car based on various features provided by the user.

#### Request Body:
- `make_id`: The ID of the car make.
- `model_id`: The ID of the car model.
- `year`: The year the car was manufactured.
- `mileage`: The mileage of the car in kilometers.
- `color_id`: The ID of the car color.
- `condition`: The condition of the car (e.g., "good", "fair").
- `location`: The location where the car is being sold.

#### Response:
- **200 OK**: The predicted price of the car.

---

### 5. `POST /predict-days-to-sell`
#### Description:
Predict how many days it will take to sell a car based on various features.

#### Request Body:
- `make_id`: The ID of the car make.
- `model_id`: The ID of the car model.
- `year`: The year the car was manufactured.
- `mileage`: The mileage of the car in kilometers.
- `color_id`: The ID of the car color.
- `condition`: The condition of the car (e.g., "good", "fair").
- `location`: The location where the car is being sold.

#### Response:
- **200 OK**: The predicted number of days it will take to sell the car.

---

### 6. `GET /feature-options`
#### Description:
Retrieve available options for different car features such as transmission type and fuel type.

#### Response:
- **200 OK**: A list of feature options (e.g., transmission, fuel type).

---

## Error Responses

### 1. **400 Bad Request**
Occurs if the client sends invalid or incomplete data in the request.

#### Example Response:
A response indicating that the input data is invalid or missing.

### 2. **404 Not Found**
Occurs if a requested resource (e.g., car make, model, or color) is not found.

#### Example Response:
A response indicating that the resource was not found.

---

## Authentication

If your API requires authentication (e.g., API tokens or OAuth), include details about the authentication methods and how to obtain credentials.

## Rate Limits

If applicable, describe any rate limits for your API (e.g., number of requests per minute/hour).
