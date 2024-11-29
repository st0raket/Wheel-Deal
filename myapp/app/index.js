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

const carMetricsForm = document.getElementById("car-metrics-form");
const evaluateButton = document.getElementById("evaluate-button");

const noResultText = document.getElementById("no-results-title");
const resultsDiv = document.getElementById("results");

const resultsCarMake = document.getElementById("results-car-make");
const resultsCarModel = document.getElementById("results-car-model");
const resultsCarYear = document.getElementById("results-car-year");
const resultsCarMileage = document.getElementById("results-car-mileage");
const resultsCarHorsepower = document.getElementById("results-car-horsepower");
const resultsCarFueltype = document.getElementById("results-car-fueltype");
const resultsCarBodystyle = document.getElementById("results-car-bodystyle");
const resultsCarColor = document.getElementById("results-car-color");
const resultsCarOptions = document.getElementById("results-car-options");
const resultsCarDamagelevel = document.getElementById("results-car-damagelevel");

const resultsPredictedPrice = document.getElementById("results-predicted-price");
const resultsPredictedTime = document.getElementById("results-predicted-time");

const populateSelect = async (select) => {
    const options = await optionsService.getOptionsBySelectId(select.id);
    for (let option of options) {
        const optionElement = document.createElement("option");
        optionElement.value = option.id;
        optionElement.innerText = option.name;
        select.append(optionElement);
    }
}

populateSelect(makeSelect);
populateSelect(modelSelect);
populateSelect(transmissionSelect);
populateSelect(fueltypeSelect);
populateSelect(bodyStyleSelect);
populateSelect(colorSelect);
populateSelect(optionSelect);
populateSelect(damageSelect);


const showPredictionResults = (predictionResults) => {
    noResultText.classList.add("hidden");
    resultsDiv.classList.remove("hidden");
    resultsDiv.classList.add("shown");

    resultsCarMake.innerText = predictionResults.make
    resultsCarModel.innerText = predictionResults.model
    resultsCarYear.innerText = predictionResults.year
    resultsCarMileage.innerText = predictionResults.mileage
    resultsCarHorsepower.innerText = predictionResults.horsepower
    resultsCarFueltype.innerText = predictionResults.fueltype
    resultsCarBodystyle.innerText = predictionResults.bodystyle
    resultsCarColor.innerText = predictionResults.color
    resultsCarOptions.innerText = predictionResults.options
    resultsCarDamagelevel.innerText = predictionResults.damagelevel
}

const clearInvalid = () => {
    yearInput.value = yearInput.value.replace(/[^0-9]/g, '');
    mileageInput.value = mileageInput.value.replace(/[^0-9]/g, '');
    horsepowerInput.value = horsepowerInput.value.replace(/[^0-9]/g, '');

}

const collectFormData = () => {
    return {
        make: makeSelect.value,
        model: modelSelect.value,
        transmission: transmissionSelect.value,
        fueltype: fueltypeSelect.value,
        bodyStyle: bodyStyleSelect.value,
        color: colorSelect.value,
        option: optionSelect.value,
        damage: damageSelect.value,
        year: yearInput.value,
        mileage: mileageInput.value,
        horsepower: horsepowerInput.value
    }
}

evaluateButton.addEventListener("click", async (e) => {
    const carProperties = collectFormData();

    e.preventDefault();
    carMetricsForm.reset();

    const predictionResults = await predictionService.getPredictionResults(carProperties);
    showPredictionResults(predictionResults);
})