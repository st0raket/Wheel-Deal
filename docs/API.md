# API Documentation

This document provides an overview of the available API endpoints for the Wheel-Deal service, which estimates car sale prices and provides related functionality.

---

## Endpoints

### 1. `GET /make-options`
#### Description:
Retrieve a list of car makes available in the system.

#### Response:
- **200 OK**: A list of car makes.

#### Example Response:
```json
[
    {"id": 1, "name": "BMW"},
    {"id": 2, "name": "Chevrolet"},
    {"id": 3, "name": "Ford"}
]
```

### 2. `GET /model-options/{makeId}`
#### Description:
Retrieve a list of car models for a specific car make.

#### Parameters:
- `makeId` (path parameter): The ID of the car make (e.g., `1` for BMW).

#### Example Request:
```http
GET /model-options/1
```
#### Example Response:
```json
[
    {"id": 1, "name": "3 Series"},
    {"id": 2, "name": "5 Series"}
]
```

### 3. `GET /color-options`
#### Description:
Retrieve a list of available car colors.

#### Response:
- **200 OK**: A list of car colors.

#### Example Response:
```json
[
    {"id": 1, "name": "Black"},
    {"id": 2, "name": "White"},
    {"id": 3, "name": "Red"}
]
```

### 4. `GET /fuel-type-options`
#### Description:
Retrieve a list of available fuel types.

#### Response:
- **200 OK**: A list of fuel types.

#### Example Response:
```json
[
    {"id": 1, "name": "Electric"},
    {"id": 2, "name": "Gasoline"},
    {"id": 3, "name": "Hybrid"}
]
```

### 5. `GET /body-style-options`
#### Description:
Retrieve a list of available car body styles.

#### Response:
- **200 OK**: A list of car body styles.

#### Example Response:
```json
[
    {"id": 1, "name": "Sedan"},
    {"id": 2, "name": "SUV"},
    {"id": 3, "name": "Coupe"}
]
```

### 6. `GET /transmission-options`
#### Description:
Retrieve a list of available transmission types.

#### Response:
- **200 OK**: A list of transmission types.

#### Example Response:
```json
[
    {"id": 1, "name": "Manual"},
    {"id": 2, "name": "Automatic"}
]
```

### 7. `GET /car-option-options`
#### Description:
Retrieve a list of available car options.

#### Response:
- **200 OK**: A list of car options.

#### Example Response:
```json
[
    {"id": 1, "name": "Base"},
    {"id": 2, "name": "Full"},
    {"id": 3, "name": "Luxe"}
]
```

### 8. `GET /damage-options`
#### Description:
Retrieve a list of available damage levels for cars.

#### Response:
- **200 OK**: A list of damage levels.

#### Example Response:
```json
[
    {"id": 1, "name": "None"},
    {"id": 2, "name": "Medium"},
    {"id": 3, "name": "Total"}
]
```

### 9. `POST /predict`
#### Description:
Predict the sale price and the estimated time to sell a car based on various features provided by the user.

#### Request Body:
- **makeId** (int): ID of the car make (e.g., 1 for BMW).
- **modelId** (int): ID of the car model (e.g., 1 for 5 Series).
- **transmissionId** (int): ID of the car's transmission type.
- **fueltypeId** (int): ID of the car's fuel type.
- **bodyStyleId** (int): ID of the car's body style.
- **colorId** (int): ID of the car's color.
- **optionId** (int): ID of the car's additional options.
- **damageId** (int): ID representing the car's damage level.
- **year** (int): The year the car was manufactured.  
  **Validation**: Must be between 1886 and 2024 (inclusive).
- **mileage** (int): The car's mileage in kilometers.  
  **Validation**: Must be a positive integer up to 1,000,000.
- **horsepower** (int): The horsepower of the car.  
  **Validation**: Must be between 0 and 2000.
- **numPrevOwners** (int): Number of previous owners of the car.  
  **Validation**: Must be between 0 and 20.


#### Response:
- **200 OK**: The predicted price and related car details.



#### Example Response::
```json
{
    "price": 25000.0,
    "time": 15.0,
    "make": "BMW",
    "model": "5 Series",
    "transmission": "Automatic",
    "fueltype": "Gasoline",
    "bodyStyle": "Sedan",
    "color": "Black",
    "option": "Sunroof",
    "damage": "None",
    "year": 2020,
    "mileage": 30000,
    "horsepower": 150,
    "numPrevOwners": 1
}
```