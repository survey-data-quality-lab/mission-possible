# 1. Instructions for Keylog Tracker Code

1. Copy code as **JavaScript** into the open text survey question.

2. Create one embedded data field named `key_log` in the **Survey Flow**, before the first survey block.

## Notes

- The keylog tracker may not work properly if **multiple text input fields** are present on the same page.  
  In such cases, the code would need to be modified to associate keystrokes with specific or all text input fields.

- Given the limit to the size of embedded data fields in Qualtrics, the keylog tracker will track approximately the **first 1000 keystrokes**.

- When using the keylog tracker on multiple pages, create separate embedded data fields for each page
(for example, `key_log_1`, `key_log_2`, and so on) and update the code accordingly on each page:

```javascript
Qualtrics.SurveyEngine.setEmbeddedData("key_log_1", JSON.stringify(keylog));
```

---

# 2. Explanation of Keylog Tracker Code

## Overview

This JavaScript runs when a Qualtrics survey page loads. It creates an array named `keylog`, records `keydown` events on the page, checks the first `textarea` for large positive changes in text length, and saves the collected data to Qualtrics Embedded Data on page submit.

---

## Execution flow

### 1. Run on page load

The script is wrapped in:

```javascript
Qualtrics.SurveyEngine.addOnload(function () {
```

This means its logic starts when the Qualtrics page loads.

At that time, it initializes:

```javascript
var keylog = [];
```

This array stores the logged events.

---

### 2. Record `keydown` events

The script adds this event listener:

```javascript
document.addEventListener("keydown", function (e) {
    const event = { key: e.key, time: Date.now() };
    keylog.push(event);
});
```

For each `keydown` event on `document`, it appends an object to `keylog` with:

- `key`: the value of `e.key`
- `time`: the current timestamp from `Date.now()`

---

### 3. Select the first `textarea`

The script selects the first `textarea` element on the page:

```javascript
const inputField = document.querySelector("textarea");
let lastLen = inputField ? inputField.value.length : 0;
```

- If a `textarea` is found, `inputField` references it and `lastLen` is set to its current text length.
- If no `textarea` is found, `inputField` is `null` and `lastLen` is set to `0`.

---

### 4. Listen for `input` events on the `textarea`

If a `textarea` exists, the script adds this listener:

```javascript
inputField.addEventListener("input", function () {
    const len = inputField.value.length;
    const jump = len - lastLen;
```

On each `input` event, it computes:

- `len`: current length of the textarea value
- `jump`: difference between current length and previous length

---

### 5. Log large positive length changes

Inside the `input` listener, the script checks:

```javascript
if (jump > 10) {
    keylog.push({
        key: "INPUT_JUMP",
        time: Date.now(),
        jump: jump,
        total: len
    });
}
```

If the change in length is greater than 10 characters, it appends an object to `keylog` containing:

- `key`: `"INPUT_JUMP"`
- `time`: current timestamp from `Date.now()`
- `jump`: number of characters added since the previous value length
- `total`: current total length of the textarea value

After that, it updates:

```javascript
lastLen = len;
```

This sets the new reference length for the next `input` event.

---

### 6. Save the collected log on page submit

The script registers:

```javascript
Qualtrics.SurveyEngine.addOnPageSubmit(function () {
   Qualtrics.SurveyEngine.setEmbeddedData("key_log", JSON.stringify(keylog));
});
```

When the page is submitted, it serializes `keylog` with `JSON.stringify(...)` and stores the result in the Qualtrics Embedded Data field named `key_log`.

---

## Data recorded

This script records two kinds of entries in the `keylog` array.

### `keydown` entries

Format:

```json
{ "key": "a", "time": 1710000000000 }
```

Fields:

- `key`: the value of `e.key`
- `time`: timestamp in milliseconds

### `INPUT_JUMP` entries

Format:

```json
{
  "key": "INPUT_JUMP",
  "time": 1710000002000,
  "jump": 25,
  "total": 30
}
```

Fields:

- `key`: fixed string `"INPUT_JUMP"`
- `time`: timestamp in milliseconds
- `jump`: positive change in textarea length since the previous `input` event
- `total`: total textarea length after the change

---

## Embedded Data output

The script writes one Qualtrics Embedded Data field:

- `key_log`

Its value is a JSON string representing the `keylog` array.

Example structure:

```json
[
  { "key": "H", "time": 1710000000000 },
  { "key": "i", "time": 1710000000500 },
  { "key": "INPUT_JUMP", "time": 1710000002000, "jump": 25, "total": 30 }
]
```