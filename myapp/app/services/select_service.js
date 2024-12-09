class OptionsService {
    constructor() {
        this.url = "http://localhost:8008/"
         
        this.makeOptions = makeOptions;
        this.modelOptions = modelOptions;
        this.transmissionOptions = transmissionOptions;
        this.fuelTypeOptions = fuelTypeOptions
        this.bodyStyleOptions = bodyStyleOptions
        this.colorOptions = colorOptions
        this.carOptionOptions = carOptionOptions
        this.damageOptions = damageOptions

    }

    getMakeOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "make-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getTransmissionOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "transmission-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getFuelTypeOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "fuel-type-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getBodyStyleOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "body-style-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getColorOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "color-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getCarOptionOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "car-option-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getDamageOptions = () => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "damage-options").then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }

    getModelOptions = (makeId) => {
        return new Promise((resolve, reject) => {
            fetch(this.url + "model-options/" + makeId).then(resp => resp.json()).then(data => {
                resolve(data)
            }).catch(err => {
                reject(err)
            })
        })
    }


}

const optionsService = new OptionsService()