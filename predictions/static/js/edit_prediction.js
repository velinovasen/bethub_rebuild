
const HTMLSelectors = {
    editButton: () => document.getElementsByClassName('edit-prediction-button'),
    myThoughts: () => document.getElementById('my-thoughts'),
    predictionText: () => document.getElementById('prediction-text'),
    editForm: () => document.getElementById('edit-prediction-form'),
    gameIdInput: () => document.getElementById('game-id-input')
}

function fillForm(e) {

    const userPredId = e.target.getAttribute('data-id')
    console.log(userPredId)
    HTMLSelectors.gameIdInput().value = userPredId;
    HTMLSelectors.predictionText().innerText = HTMLSelectors.myThoughts().innerText;

}

for (button of HTMLSelectors.editButton()) {

    button.addEventListener('click', fillForm)
}
