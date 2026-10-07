let timeLeft = 300;
let timerinterval = null;

function updateTimer() {
    let minutes = Math.floor(timeLeft/60);
    let seconds = timeLeft % 60;

    document.getElementById("timer").textContent = 
    String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
}

function startTimer() {
    if(timerinterval !== null)return;

    timerinterval = setInterval(function () {
    if(timeLeft > 0) {
        timeLeft--;
        updateTimer();
    } else {
       pauseTimer();
    }
}, 1000);
}

function pauseTimer() {
    clearInterval(timerinterval);
    timerinterval = null;
}

function resetTimer() {
                 pauseTimer ();
    timeLeft = 300;
    updateTimer();
}

updateTimer()