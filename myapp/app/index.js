const makeSelect = document.getElementById("make-select");
const modelSelect = document.getElementById("model-select");
const transmissionSelect = document.getElementById("transmission-select");
const fueltypeSelect = document.getElementById("fueltype-select");
const bodyStyleSelect = document.getElementById("bodystyle-select");
const colorSelect = document.getElementById("color-select");
const optionSelect = document.getElementById("option-select");
const damageSelect = document.getElementById("damage-select");
const yearInput = document.getElementById("year-input");
const mileageInput = document.getElementById("mileage-input");
const horsepowerInput = document.getElementById("horsepower-input");
const numberOfPreviousOwnersInput = document.getElementById("num-prev-owners")

const carMetricsForm = document.getElementById("car-metrics-form");
const evaluateButton = document.getElementById("evaluate-button");

const noResultText = document.getElementById("no-results-title");
const resultsDiv = document.getElementById("results");

const resultsCarMake = document.getElementById("results-car-make");
const resultsCarModel = document.getElementById("results-car-model");
const resultsCarYear = document.getElementById("results-car-year");
const resultsCarMileage = document.getElementById("results-car-mileage");
const resultsCarHorsepower = document.getElementById("results-car-horsepower");
const resultsCarPrevOwners = document.getElementById("results-car-prevowners");
const resultsCarFueltype = document.getElementById("results-car-fueltype");
const resultsCarBodystyle = document.getElementById("results-car-bodystyle");
const resultsCarColor = document.getElementById("results-car-color");
const resultsCarOptions = document.getElementById("results-car-options");
const resultsCarDamagelevel = document.getElementById("results-car-damagelevel");

const resultsPredictedPrice = document.getElementById("results-predicted-price");
const resultsPredictedTime = document.getElementById("results-predicted-time");

const populateSelect = (select, options) => {
    for (let option of options) {
        const optionElement = document.createElement("option");
        optionElement.value = option.id;
        optionElement.innerText = option.name;
        select.append(optionElement);
    }
}

const populateAllPossibleSelects = async () => {
    const makeOptions = await optionsService.getMakeOptions();
    populateSelect(makeSelect, makeOptions)

    const transmissionOptions = await optionsService.getTransmissionOptions();
    populateSelect(transmissionSelect, transmissionOptions)

    const fuelTypeOptions = await optionsService.getFuelTypeOptions();
    populateSelect(fueltypeSelect, fuelTypeOptions)

    const bodyStyleOptions = await optionsService.getBodyStyleOptions();
    populateSelect(bodyStyleSelect, bodyStyleOptions)

    const colorOptions = await optionsService.getColorOptions();
    populateSelect(colorSelect, colorOptions)

    const carOptionOptions = await optionsService.getCarOptionOptions();
    populateSelect(optionSelect, carOptionOptions)

    const damageOptions = await optionsService.getDamageOptions();
    populateSelect(damageSelect, damageOptions)
}


const showPredictionResults = (predictionResults) => {
    noResultText.classList.add("hidden");
    resultsDiv.classList.remove("hidden");
    resultsDiv.classList.add("shown");

    resultsCarMake.innerText = predictionResults.make;
    resultsCarModel.innerText = predictionResults.model;
    resultsCarYear.innerText = predictionResults.year;
    resultsCarMileage.innerText = predictionResults.mileage;
    resultsCarHorsepower.innerText = predictionResults.horsepower;
    resultsCarFueltype.innerText = predictionResults.fueltype;
    resultsCarBodystyle.innerText = predictionResults.bodyStyle;
    resultsCarColor.innerText = predictionResults.color;
    resultsCarOptions.innerText = predictionResults.option;
    resultsCarDamagelevel.innerText = predictionResults.damage;
    resultsCarPrevOwners.innerText = predictionResults.numPrevOwners;

    resultsPredictedPrice.innerText = parseInt(predictionResults.price).toLocaleString();
    resultsPredictedTime.innerText = parseInt(predictionResults.time).toLocaleString();

}

const clearInvalid = () => {
    yearInput.value = yearInput.value.replace(/[^0-9]/g, '');
    mileageInput.value = mileageInput.value.replace(/[^0-9]/g, '');
    horsepowerInput.value = horsepowerInput.value.replace(/[^0-9]/g, '');

}

const collectFormData = () => {
    return {
        makeId: makeSelect.value,
        modelId: modelSelect.value,
        transmissionId: transmissionSelect.value,
        fueltypeId: fueltypeSelect.value,
        bodyStyleId: bodyStyleSelect.value,
        colorId: colorSelect.value,
        optionId: optionSelect.value,
        damageId: damageSelect.value,
        year: yearInput.value,
        mileage: mileageInput.value,
        horsepower: horsepowerInput.value,
        numPrevOwners: numberOfPreviousOwnersInput.value
    }
}

evaluateButton.addEventListener("click", async (e) => {
    try {
        const carProperties = collectFormData();
        e.preventDefault();
        carMetricsForm.reset();

        const predictionResults = await predictionService.getPredictionResults(carProperties);
        showPredictionResults(predictionResults);
    } catch (err) {
        alert(err)
    }
   
})

const handleMakeSelectChage = async () => {
    keepOnlyDefaulOption(modelSelect);

    makeId = makeSelect.value;
    const modelOptions = await optionsService.getModelOptions(makeId);
    populateSelect(modelSelect, modelOptions)
}


const keepOnlyDefaulOption = (selectObject) => {
    selectObject.innerHTML = "";
    const defaultOption = document.createElement("option");
    defaultOption.text = "Choose";
    defaultOption.value = "Choose"
    selectObject.append(defaultOption)
}


populateAllPossibleSelects()