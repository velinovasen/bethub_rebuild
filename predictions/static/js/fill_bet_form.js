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
    datePar: () => document.getElementById('date-par'),
    timeInput: () => document.getElementById('prediction-time-input'),
    timePar: () => document.getElementById('time-par'),
    homeTeamInput: () => document.getElementById('home-team-input'),
    homeTeamPar: () => document.getElementById('home-team-par'),
    awayTeamInput: () => document.getElementById('away-team-input'),
    awayTeamPar: () => document.getElementById('away-team-par'),
    signInput: () => document.getElementById('prediction-sign'),
    signPar: () => document.getElementById('sign-form-par'),
    oddInput: () => document.getElementById('prediction-odd'),
    oddPar: () => document.getElementById('odd-form-par'),
    betAmount: () => document.getElementById('prediction-bet-amount'),

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

    console.log(gameId, date, time, homeTeam, awayTeam, homeOdd, drawOdd, awayOdd)

    const gameIdInputForm = FormSelector.gameIdInputForm();
    const dateInputForm = FormSelector.dateInput();
    const timeInputForm = FormSelector.timeInput();
    const homeTeamInputForm = FormSelector.homeTeamInput();
    const awayTeamInputForm = FormSelector.awayTeamInput();
    const signInputForm = FormSelector.signInput();
    const oddInputForm = FormSelector.oddInput();
    const betAmount = FormSelector.betAmount();

    gameIdInputForm.value = gameId;
    dateInputForm.value = date;
    FormSelector.datePar().innerText = date;
    timeInputForm.value = time;
    FormSelector.timePar().innerText = time;
    homeTeamInputForm.value = homeTeam;
    FormSelector.homeTeamPar().innerText = homeTeam;
    awayTeamInputForm.value = awayTeam;
    FormSelector.awayTeamPar().innerText = awayTeam;
    signInputForm.value = myBets[event.target.parentElement.className];
    FormSelector.signPar().innerText = myBets[event.target.parentElement.className];
    oddInputForm.value = event.target.innerText;
    FormSelector.oddPar().innerText = event.target.innerText;

}

for (odd of document.getElementsByClassName('odds_column')) {
    odd.addEventListener('click', fillForm)
}