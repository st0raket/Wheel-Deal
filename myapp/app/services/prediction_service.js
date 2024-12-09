class PredictionService {
    constructor() { 
        this.url = "http://localhost:8008/"
    }
    
    getPredictionResults = (carProperties) => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "predict", {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(carProperties)
            }).then(resp => {
                if(resp.status == "422") return reject("Please fill all the data")
                else return resp.json()
            }).then(data => resolve(data)).catch(err => console.err(err))
        })
    } 
}

const predictionService = new PredictionService();
