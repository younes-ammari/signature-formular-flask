
document.addEventListener("DOMContentLoaded", function () {
    // Code to be executed after the HTML page has loaded
    // ...

    // Example: Display a message in the console

    // Signature canvas
    const canvas = document.getElementById('signatureCanvas');
    const context = canvas.getContext('2d');

    let signaturePad = new SignaturePad(canvas);

    var ctx = canvas.getContext("2d");

    let isDrawing = false;
    let previousX = 0;
    let previousY = 0;
    var rect = canvas.getBoundingClientRect(); // Get the position of the canvas relative to the viewport
    var lastX = 0;
    var lastY = 0;


    // function startDrawing(e) {
    //     isDrawing = true;
    //     [lastX, lastY] = [e.clientX - rect.left, e.clientY - rect.top]; // Adjust the coordinates based on the canvas position
    // }

    // function draw(e) {
    //     // if ((e.buttons || e.which) === 1) {
    //     //     const x = e.pageX, y = e.pageY;
    //     //     ctx.fillRect(x, y, 1, 1);
    //     // }
    //     if (!isDrawing) return;
    //     var x = e.clientX - rect.left; // Adjust the coordinates based on the canvas position
    //     var y = e.clientY - rect.top; // Adjust the coordinates based on the canvas position
    //     ctx.beginPath();
    //     ctx.moveTo(lastX, lastY);
    //     ctx.lineTo(x, y);
    //     ctx.stroke();
    //     [lastX, lastY] = [x, y];
    // }

    // function stopDrawing() {
    //     isDrawing = false
    //     captureSignature();;
    // }
    let ongoingTouches = [];

    function handleTouchStart(event) {
        event.preventDefault();
        let touches = event.changedTouches;

        for (let i = 0; i < touches.length; i++) {
            let touch = touches[i];
            let touchData = {
                identifier: touch.identifier,
                x: touch.clientX - canvas.offsetLeft,
                y: touch.clientY - canvas.offsetTop
            };
            ongoingTouches.push(touchData);
        }
    }

    function handleTouchMove(event) {
        event.preventDefault();
        let touches = event.changedTouches;

        for (let i = 0; i < touches.length; i++) {
            let touch = touches[i];
            let touchData = getOngoingTouchByIdentifier(touch.identifier);

            if (touchData) {
                let previousX = touchData.x;
                let previousY = touchData.y;
                let currentX = touch.clientX - canvas.offsetLeft;
                let currentY = touch.clientY - canvas.offsetTop;

                drawLine(previousX, previousY, currentX, currentY);

                touchData.x = currentX;
                touchData.y = currentY;
            }
        }
    }

    function getOngoingTouchByIdentifier(identifier) {
        for (let i = 0; i < ongoingTouches.length; i++) {
            if (ongoingTouches[i].identifier === identifier) {
                return ongoingTouches[i];
            }
        }
        return null;
    }

    function drawLine(startX, startY, endX, endY) {
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
    }


    canvas.addEventListener('touchstart', handleTouchStart, false);
    canvas.addEventListener('touchmove', handleTouchMove, false);


    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    function startDrawing(event) {
        isDrawing = true;
        previousX = event.offsetX;
        previousY = event.offsetY;
    }

    function draw(event) {
        if (!isDrawing) return;
        context.beginPath();
        context.moveTo(previousX, previousY);
        context.lineTo(event.offsetX, event.offsetY);
        context.stroke();
        previousX = event.offsetX;
        previousY = event.offsetY;
    }

    function stopDrawing() {
        isDrawing = false;
        captureSignature();
    }

    function captureSignature() {
        const signatureData = canvas.toDataURL();  // Convert canvas to data URL
        const signatureInput = document.getElementById('signatureInput');
        signatureInput.value = signatureData;
    }

    document.getElementById("clear-button").addEventListener("click", function (event) {
        clearSignature(event)
    })

    function clearSignature(event) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        captureSignature();  // Clear signature input
        previousY = event.offsetY;
    }

    function resizeCanvas() {
        var ratio = Math.max(window.devicePixelRatio || 1, 1);
        canvas.width = canvas.offsetWidth * ratio;
        canvas.height = canvas.offsetHeight * ratio;
        canvas.getContext("2d").scale(ratio, ratio);
        context.clearRect(0, 0, canvas.width, canvas.height);
        
        // canvas.clear(); // otherwise isEmpty() might return incorrect value
    }

    // window.addEventListener("resize", resizeCanvas);
    // resizeCanvas();


    // document.getElementById("registration-form").addEventListener("submit", function (event) {
    //     event.preventDefault();

    //     var form = event.target;
    //     var formData = new FormData(form);

    //     var xhr = new XMLHttpRequest();
    //     xhr.open("POST", form.action);
    //     xhr.onreadystatechange = function () {
    //         if (xhr.readyState === XMLHttpRequest.DONE) {
    //             if (xhr.status === 200) {
    //                 // console.log(xhr.responseText)
    //                 // var recordsContainer = document.getElementById("records-container");
    //                 // recordsContainer.innerHTML = xhr.responseText;
    //                 form.reset();
    //             } else {
    //                 console.error("Error submitting the form.");
    //             }
    //         }
    //     };
    //     xhr.send(formData);
    // });
    console.log("HTML page has loaded.");
});
