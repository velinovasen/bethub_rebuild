const TableSelectors = {
    gameId: () => document.getElementById('game_id'),
    dateField: () => document.getElementById('date-field'),
    timeField: () => document.getElementById('time-field'),
    homeTeamField: () => document.getElementById('home-team-field'),
    awayTeamField: () => document.getElementById('away-team-field'),
    homeOddField: () => document.getElementById('home-odd-field'),
    drawOddField: () => document.getElementById('draw-odd-field'),
    awayOddField: () => document.getElementById('away-odd-field'),
}

const FormSelector = {
    gameIdInputForm: () => document.getElementById('game-id-input'),
    dateInput: () => document.getElementById('prediction-date-input'),
    timeInput: () => document.getElementById('prediction-time-input'),
    homeTeamInput: () => document.getElementById('home-team-input'),
    awayTeamInput: () => document.getElementById('away-team-input'),
    signInput: () => document.getElementById('prediction-sign'),
    oddInput: () => document.getElementById('prediction-odd'),
    predictionTextInput: () => document.getElementById('prediction-text'),

}

const myBets = {
    'home_odd': '1',
    'draw_odd': 'X',
    'away_odd': '2'
}

function fillForm(event) {

    const gameId = TableSelectors.gameId().innerText;
    const date = TableSelectors.dateField().innerText;
    const time = TableSelectors.timeField().innerText;
    const homeTeam = TableSelectors.homeTeamField().innerText;
    const awayTeam = TableSelectors.awayTeamField().innerText;
    const homeOdd = TableSelectors.homeOddField().innerText;
    const drawOdd = TableSelectors.drawOddField().innerText;
    const awayOdd = TableSelectors.awayOddField().innerText;

    const gameIdInputForm = FormSelector.gameIdInputForm();
    const dateInputForm = FormSelector.dateInput();
    const timeInputForm = FormSelector.timeInput();
    const homeTeamInputForm = FormSelector.homeTeamInput();
    const awayTeamInputForm = FormSelector.awayTeamInput();
    const signInputForm = FormSelector.signInput();
    const oddInputForm = FormSelector.oddInput();
    const predictionTextInputForm = FormSelector.predictionTextInput();

    gameIdInputForm.value = gameId;
    dateInputForm.value = date;
    timeInputForm.value = time;
    homeTeamInputForm.value = homeTeam;
    awayTeamInputForm.value = awayTeam;
    signInputForm.value = myBets[event.target.parentElement.className];
    oddInputForm.value = event.target.innerText;

}

for (odd of document.getElementsByClassName('odds_column')) {
    odd.addEventListener('click', fillForm)
}