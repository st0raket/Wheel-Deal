class PredictionService {
    constructor() { }
    
    getPredictionResults = (carProperties) => {
        return new Promise((resolve, reject) => {
            // insert fetch logic here in milestone 4
            resolve({
                make: "Ford",
                model: "Focus",
                year: 2016,
                mileage: 200000,
                horsepower: 240,
                fueltype: "Petrol",
                bodystyle: "Convertible",
                color: "Blue",
                options: "BlueTooth Connectivity",
                damagelevel: "No Damage",
                price: 5000,
                time: 10
            })
        })
    }

 
}

const predictionService = new PredictionService();
