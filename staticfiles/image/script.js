const distanceText = document.getElementById("distance");
const buzzerStatus = document.getElementById("buzzer-status");

let distance = 150;

function updateSimulation() {
    distance -= 1;
    if (distance <= 0) distance = 150;

    distanceText.textContent = distance;

    if (distance < 30) {
        buzzerStatus.innerHTML = "🔊 Buzzer: ON (Very Close!)";
        buzzerStatus.style.color = "red";
    } else if (distance < 60) {
        buzzerStatus.innerHTML = "🔉 Buzzer: ON (Close)";
        buzzerStatus.style.color = "orange";
    } else {
        buzzerStatus.innerHTML = "🔈 Buzzer: OFF";
        buzzerStatus.style.color = "green";
    }

    requestAnimationFrame(updateSimulation);
}

function drawWires() {
    const canvas = document.getElementById("wires");
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(150, 90);
    ctx.lineTo(370, 90);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(150, 90);
    ctx.lineTo(370, 250);
    ctx.stroke();
}

drawWires();
updateSimulation();
