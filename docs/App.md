# App Service Documentation

This section provides a high-level overview of the app service used in the WheelDeal project. It consists of the **index.js** file and two main services: **PredictionService** and **OptionsService**. These services manage the car evaluation process, including fetching car options for user selection and generating price predictions based on car properties.

## Services Overview

### 1. **PredictionService**

The `PredictionService` is responsible for providing car prediction results based on the properties provided by the user. This service sends a request to the backend, providing the car properties.

#### Methods:

- **getPredictionResults(carProperties)**
    - **Description**: Sends a POST request to the `/predict` endpoint with car properties.
    - **Parameters**: 
        - `carProperties`: An object containing the properties of the car, such as make, model, transmission, fuel type, etc.
    - **Returns**: A Promise that resolves to an object with the predicted car details.
    - **Error Handling**:
        - Rejects with a message if required data is missing or if the fetch operation fails.

    - **Example Response**:
    ```javascript
    {
        make: "Ford",
        model: "Focus",
        year: 2016,
        mileage: 200000,
        horsepower: 240,
        numOfPrevOwners: 3,
        fueltype: "Petrol",
        bodystyle: "Convertible",
        color: "Blue",
        options: "Bluetooth Connectivity",
        damagelevel: "No Damage",
        price: 5000,
        time: 10
    }
    ```

### 2. **OptionsService**

The `OptionsService` handles retrieving the available options for various car attributes, such as make, model, fuel type, transmission type, etc. These options are used to populate dropdown lists (select inputs) on the car evaluation form in the user interface.

#### Properties:

- **makeOptions**: Options for car makes.
- **modelOptions**: Options for car models (taking into account the selected car make).
- **transmissionOptions**: Options for car transmission types.
- **fuelTypeOptions**: Options for fuel types.
- **bodyStyleOptions**: Options for body styles.
- **colorOptions**: Options for car colors.
- **carOptionOptions**: Options for additional car features (e.g., Bluetooth, GPS).
- **damageOptions**: Options for car damage levels (e.g., No Damage, Minor Damage).

#### Methods:

- `getMakeOptions()`
- `getModelOptions(makeId`)
- `getTransmissionOptions()`
- `getFuelTypeOptions()`
- `getBodyStyleOptions()`
- `getColorOptions()`
- `getCarOptionOptions()`
- `getDamageOptions()`

#### Example usage: 
```javascript
const optionsService = new OptionsService();
optionsService.getMakeOptions()
    .then(makeOptions => console.log(makeOptions))
    .catch(err => console.error(err));
```

### 3. **index.js**
Handles DOM interactions and event listeners for the car evaluation platform.

##### Key functions

- `populateSelect(select, options)`
    - Populates the select HTML object by an array of HTMLOptionElement-s.
- `populateAllPossibleSelects()`
    - Populates all dropdowns (e.g., make, model, transmission) with options, except the model dropdown, because the model dropdown is populated when the make is selected.
- `showPredictionResults(predictionResults)`
    - Updates the UI with prediction results.
- `handleMakeSelectChange()`
    - Dynamically updates the model dropdown based on the selected make.
- `evaluateButton.addEventListener("click")`
    - Collects form data and fetches prediction results when the "Evaluate" button is clicked.