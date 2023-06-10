
document.addEventListener("DOMContentLoaded", function () {
    // Code to be executed after the HTML page has loaded
    // ...

    // Example: Display a message in the console

    // Signature canvas
    const canvas = document.getElementById('signatureCanvas');
    const context = canvas.getContext('2d');

    window.addEventListener('resize', resizeCanvas);

    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        // Perform any additional resizing logic or re-rendering here if needed
    }

    // Call the resizeCanvas function initially to set the canvas size
    resizeCanvas();

    let signaturePad = new SignaturePad(canvas);

    var ctx = canvas.getContext("2d");

    let isDrawing = false;
    let previousX = 0;
    let previousY = 0;
    var rect = canvas.getBoundingClientRect(); // Get the position of the canvas relative to the viewport
    var lastX = 0;
    var lastY = 0;

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


    // canvas.addEventListener('touchstart', handleTouchStart, false);
    // canvas.addEventListener('touchmove', handleTouchMove, false);


    // canvas.addEventListener('mousedown', startDrawing);
    // canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    canvas.addEventListener('touchstart', handleTouchStart, false);
    canvas.addEventListener('touchmove', handleTouchMove, false);
    canvas.addEventListener('touchend', handleTouchEnd, false);

    // let isDrawing = false;

    function handleTouchStart(event) {
        isDrawing = true;
    }

    function handleTouchMove(event) {
        if (isDrawing) {
            let touch = event.touches[0];
            let rect = canvas.getBoundingClientRect();
            let offsetX = touch.clientX - rect.left;
            let offsetY = touch.clientY - rect.top;
            // signaturePad.strokeMoveTo(offsetX, offsetY);
            // signaturePad.lineTo(offsetX, offsetY);
            // signaturePad.stroke();
        }
    }

    function handleTouchEnd(event) {
        isDrawing = false;
        let signatureData = signaturePad.toDataURL();
        // console.log('signatureData', signatureData)
        // const signatureData = canvas.toDataURL();  // Convert canvas to data URL
        const signatureInput = document.getElementById('signatureInput');
        signatureInput.value = signatureData;
    }

    function stopDrawing() {
        isDrawing = false;
        // console.log("stoped")
        captureSignature();
    }

    function captureSignature() {
        let signatureData = signaturePad.toDataURL();  // Convert canvas to data URL
        // console.log('signatureData', signatureData)
        // const signatureData = canvas.toDataURL();  // Convert canvas to data URL
        const signatureInput = document.getElementById('signatureInput');
        signatureInput.value = signatureData;
    }

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
        // console.log("stoped")
        captureSignature();
    }


    document.getElementById("clear-button").addEventListener("click", function (event) {
        clearSignature(event)
    })

    function clearSignature(event) {
        signaturePad.clear();

        // context.clearRect(0, 0, canvas.width, canvas.height);
        captureSignature();  // Clear signature input
        // previousY = event.offsetY;
    }



    console.log("HTML page has loaded.");
});
