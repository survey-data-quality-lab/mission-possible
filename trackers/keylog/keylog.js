Qualtrics.SurveyEngine.addOnload(function () {
    
    var keylog = [];

    // Keystroke logging
    document.addEventListener("keydown", function (e) {
        const event = { key: e.key, time: Date.now() };
        keylog.push(event);
    });

    // Detect and log large input jumps
    const inputField = document.querySelector("textarea");
    let lastLen = inputField ? inputField.value.length : 0;

    if (inputField) {
        inputField.addEventListener("input", function () {
            const len = inputField.value.length;
            const jump = len - lastLen;

            if (jump > 10) {
                keylog.push({
                    key: "INPUT_JUMP",
                    time: Date.now(),
                    jump: jump,
                    total: len
                });
            }
            lastLen = len;
        });
    }

// Save everything when page submits
Qualtrics.SurveyEngine.addOnPageSubmit(function () {

   Qualtrics.SurveyEngine.setEmbeddedData("key_log", JSON.stringify(keylog));
    });
});
