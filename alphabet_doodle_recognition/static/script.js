let canvas;
let ctx;
let isDrawing = false;
let lastX = 0;
let lastY = 0;

document.addEventListener("DOMContentLoaded", () => {
    canvas = document.getElementById("drawingCanvas");
    ctx = canvas.getContext("2d");

    // Set canvas background to black
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Drawing logic
    canvas.addEventListener("mousedown", (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener("mouseup", () => isDrawing = false);
    canvas.addEventListener("mouseleave", () => isDrawing = false);

    canvas.addEventListener("mousemove", (e) => {
        if (!isDrawing) return;
        ctx.strokeStyle = "white";         // white strokes
        ctx.lineWidth = 15;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });
});

// Clear the canvas
function clearCanvas() {
    ctx.fillStyle = "black";  // reset background to black
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    document.getElementById("result").innerText = "";
}

// Convert data URI to Blob
function dataURItoBlob(dataURI) {
    let byteString = atob(dataURI.split(",")[1]);
    let arrayBuffer = new ArrayBuffer(byteString.length);
    let uint8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }
    return new Blob([uint8Array], { type: "image/png" });
}

// Send image to backend for prediction
function sendToServer() {
    const image = canvas.toDataURL("image/png");  // send raw (already white-on-black)
    const blob = dataURItoBlob(image);
    const formData = new FormData();
    formData.append("image", blob, "drawing.png");

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Prediction: " + data.prediction;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error occurred. Try again.";
    });
}
