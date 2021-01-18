<h1>BETHUB</h1>
    <p><b>A web-crawler which checks multiple websites and stores the data into postgres.
    Users are able to register and place bets, so they can try out different strategies, without costing them any money.</b></p>
    <p><b>We have a traffic page, which gives you the most placed bets in Europe at the moment, as well as predictions, 
    which are scraped from www.forebet.com</b></p>
    
<h2>Installation</h2>
    <p><b>After you clone the repo, install requirements.txt in your venv. Hook your PostgreSQL in the settings.</b></p>
    <p><b>For automation we use celery. If you are on Windows10, download Ubuntu from the Microsoft Store and 
    run redis-server on it. Make sure you have the correct ports in the settings menu. <br>
    To run the Celery worker, in terminal we use: <p>`celery -A bethub worker -l info`</p>
    !!! FOR WINDOWS10 WE USE: <p>`celery -A bethub worker -l info -P solo`  !!!</p>
    For monitoring you can start: <p>`celery -A bethub flower`</p>
    which you can open in your browses on: `localhost:5555`</b></p>
    <p><b>To start the beat use: <p>`celery -A bethub beat -l info`</p></b></p>
    <p><b></b></p>
    

<b>Home page</b>
<a href="https://ibb.co/NSy98Tx"><img src="https://i.ibb.co/9trbFZn/home-page.png" alt="home-page" border="0"></a>

<b>History page</b>
<a href="https://ibb.co/CtBSmc4"><img src="https://i.ibb.co/X4XGjQ6/history-page.png" alt="history-page" border="0"></a>

<b>Traffic page</b>
<a href="https://ibb.co/BK9v0Pz"><img src="https://i.ibb.co/R4qtRSv/traffic-page.png" alt="traffic-page" border="0"></a>

<b>My Predictions page</b>
<a href="https://ibb.co/2tHKHVn"><img src="https://i.ibb.co/swz3zxm/predictions-page.png" alt="predictions-page" border="0"></a>
