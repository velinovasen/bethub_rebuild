
const HTMLSelectors = {
    editButton: () => document.getElementsByClassName('edit-prediction-button'),
    myThoughts: () => document.getElementById('my-thoughts'),
    predictionText: () => document.getElementById('prediction-text'),
    editForm: () => document.getElementById('edit-prediction-form'),
    gameIdInput: () => document.getElementById('game-id-input'),

    deleteButton: () => document.getElementsByClassName('delete-prediction-button'),
    deleteForm: () => document.getElementById('delete-prediction-form'),
    gameIdDeleteInput: () => document.getElementById('game-id-delete-input'),
}

function fillForm(e) {

    const userPredId = e.target.getAttribute('data-id')
    console.log(userPredId)
    HTMLSelectors.gameIdInput().value = userPredId;
    HTMLSelectors.predictionText().innerText = HTMLSelectors.myThoughts().innerText;

}

function fillDeleteForm(e) {

    const userPredId = e.target.getAttribute('data-id')
    HTMLSelectors.deleteForm().action = '/delete/' + userPredId + '/'

}

for (button of HTMLSelectors.editButton()) {

    button.addEventListener('click', fillForm)
}

for (button of HTMLSelectors.deleteButton()) {

    button.addEventListener('click', fillDeleteForm)
}
