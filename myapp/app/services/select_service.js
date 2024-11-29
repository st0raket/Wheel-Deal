class OptionsService {
    constructor() {
        this.url = "url"
         
        this.makeOptions = makeOptions;
        this.modelOptions = modelOptions;
        this.transmissionOptions = transmissionOptions;
        this.fuelTypeOptions = fuelTypeOptions
        this.bodyStyleOptions = bodyStyleOptions
        this.colorOptions = colorOptions
        this.carOptionOptions = carOptionOptions
        this.damageOptions = damageOptions

    }


    getOptionsBySelectId = (selectId) => {
        // insert prediction logic here in milestone 4
        return new Promise((resolve, reject) => {
            switch (selectId) {
                case "make-select":
                    resolve(this.makeOptions)
                case "model-select":
                    resolve(this.modelOptions)
                case "transmission-select":
                    resolve(this.transmissionOptions)
                case "fueltype-select":
                    resolve(this.fuelTypeOptions)
                case "bodystyle-select":
                    resolve(this.bodyStyleOptions)
                case "color-select":
                    resolve(this.colorOptions)
                case "option-select":
                    resolve(this.carOptionOptions)
                case "damage-select":
                    resolve(this.damageOptions)
            }
        })
    }
}

const optionsService = new OptionsService()