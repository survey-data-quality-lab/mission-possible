# 1. Instructions for General Tracker Code

1. Copy code into the Qualtrics survey header under HTML view:  
   *(Survey → Look and Feel → Header → Source)*

2. Create two embedded data fields named `tracking_json` and `page` in the **Survey Flow**, before the first survey block.  
   Set `page` equal to `1`.


## Notes on Implementation

- There is a limit to the size of embedded data fields in Qualtrics.  
  Thus, the general tracker code only works reliably for short to medium-length surveys like ours (10 pages).

- For much longer surveys, one would need to modify the code to store data for sets of pages separately in different embedded data fields (e.g., `tracking_json_1`, `tracking_json_2`, etc).

- The longest tracking JSON in our data successfully stored 47 tracking entries.

- Note that the tracker generates multiple entries per page if the page is reloaded (e.g., when respondents did not complete all required fields).

- Therefore, **matching to survey pages** should be done via `question_ids` and **not** via `page`.


---

# 2. Explanation of General Tracker Code

## Overview

This script runs when a Qualtrics survey page loads. It records page timing, page number, counts of several browser events, selected event timestamps, the IDs of visible Qualtrics questions on the page, and stores the result in Qualtrics Embedded Data when the page is submitted.

---

## Execution flow

### 1. Run on page load

The script is wrapped in:

```javascript
Qualtrics.SurveyEngine.addOnload(function () {
```

This means its logic starts when the Qualtrics page loads.

It first stores:

```javascript
const startTime = Date.now();
```

This timestamp is later used to calculate time on page.

---

### 2. Read the current page number

The script reads the Embedded Data field `page`:

```javascript
let page = parseInt(Qualtrics.SurveyEngine.getEmbeddedData("page")) || 1;
```

- If the stored value can be parsed as a number, that number is used.
- Otherwise, `page` is set to `1`.

---

### 3. Initialize counters, flags, and log storage

The script initializes:

```javascript
let mouseMoved       = false;
let mouseMoveCount   = 0;
let clickCount       = 0;
let keyCount         = 0;
let pasted           = false;
let copied           = false;
let tabHidden        = false;
let windowBlurred    = false;
let scrollEventCount = 0;
let eventLog         = [];
```

These variables hold page-level tracking values.

---

### 4. Record mouse movement

The script adds:

```javascript
document.addEventListener("mousemove", () => {
    mouseMoveCount += 1;
    mouseMoved = true;
});
```

For each `mousemove` event on `document`:

- `mouseMoveCount` increases by 1
- `mouseMoved` is set to `true`

---

### 5. Record scroll events

The script adds:

```javascript
document.addEventListener("scroll", () => {
    scrollEventCount += 1;
}, { passive: true });
```

For each `scroll` event on `document`, `scrollEventCount` increases by 1.

---

### 6. Record click events

The script adds:

```javascript
document.addEventListener("click", () => { clickCount += 1; });
```

For each `click` event on `document`, `clickCount` increases by 1.

---

### 7. Record keydown count

The script adds:

```javascript
document.addEventListener("keydown", () => {
    keyCount += 1;
});
```

For each `keydown` event on `document`, `keyCount` increases by 1.

---

### 8. Record paste events

The script adds:

```javascript
document.addEventListener("paste", () => {
    pasted = true;
    eventLog.push({ event: "PASTE", time: Date.now() });
});
```

For each `paste` event on `document`:

- `pasted` is set to `true`
- an object is appended to `eventLog` with:
  - `event`: `"PASTE"`
  - `time`: current timestamp from `Date.now()`

---

### 9. Record copy events

The script adds:

```javascript
document.addEventListener("copy", () => {
    copied = true;
    eventLog.push({ event: "COPY", time: Date.now() });
});
```

For each `copy` event on `document`:

- `copied` is set to `true`
- an object is appended to `eventLog` with:
  - `event`: `"COPY"`
  - `time`: current timestamp from `Date.now()`

---

### 10. Record tab visibility changes

The script adds:

```javascript
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        tabHidden = true;
        eventLog.push({ event: "TAB_HIDDEN", time: Date.now() });
    } else {
        eventLog.push({ event: "TAB_VISIBLE", time: Date.now() });
    }
});
```

When `visibilitychange` fires:

- if `document.hidden` is `true`:
  - `tabHidden` is set to `true`
  - `{ event: "TAB_HIDDEN", time: Date.now() }` is appended to `eventLog`
- otherwise:
  - `{ event: "TAB_VISIBLE", time: Date.now() }` is appended to `eventLog`

---

### 11. Record window focus changes

The script adds:

```javascript
window.addEventListener("blur", () => {
    windowBlurred = true;
    eventLog.push({ event: "WINDOW_BLUR", time: Date.now() });
});

window.addEventListener("focus", () => {
    eventLog.push({ event: "WINDOW_FOCUS", time: Date.now() });
});
```

When the window `blur` event fires:

- `windowBlurred` is set to `true`
- `{ event: "WINDOW_BLUR", time: Date.now() }` is appended to `eventLog`

When the window `focus` event fires:

- `{ event: "WINDOW_FOCUS", time: Date.now() }` is appended to `eventLog`

---

### 12. Register page-submit handler

The script sets:

```javascript
let submitted = false;
Qualtrics.SurveyEngine.addOnPageSubmit(function(type) {
    if (submitted) return;
    submitted = true;
```

This creates a flag named `submitted`. On the first call to the page-submit handler, the flag is set to `true`. Later calls return immediately.

The handler receives one argument, `type`.

---

### 13. Calculate time on page

Inside the submit handler, the script computes:

```javascript
const endTime = Date.now();
const timeOnPage = Math.round((endTime - startTime) / 1000);
```

This stores page duration in seconds, rounded with `Math.round(...)`.

---

### 14. Collect visible question IDs

The script collects question IDs with:

```javascript
const questionIDs = Array.from(
    document.querySelectorAll('.QuestionOuter')
).map(el => el.id).filter(id => id.startsWith('QID'));
```

This:

1. selects all elements matching `.QuestionOuter`
2. maps them to their `id` values
3. keeps only IDs that start with `"QID"`

The resulting array is stored in `questionIDs`.

---

### 15. Create the tracking object

The script builds:

```javascript
const trackingEntry = {
    page: page,
    question_ids: questionIDs,
    start_time: startTime,
    time_on_page: timeOnPage,
    mouse_moved: mouseMoved,
    mouse_move_count: mouseMoveCount,
    click_count: clickCount,
    total_keys: keyCount,
    paste_detected: pasted,
    copy_detected: copied,
    tab_hidden: tabHidden,
    window_blurred: windowBlurred,
    scroll_event_count: scrollEventCount,
    event_log: eventLog,
    ts: Date.now()
};
```

This object contains the page number, question IDs, timing values, counters, flags, and the `eventLog` array.

---

### 16. Append to `tracking_json`

The script reads and updates Embedded Data:

```javascript
const prev = Qualtrics.SurveyEngine.getEmbeddedData("tracking_json");
const list = prev ? JSON.parse(prev) : [];
list.push(trackingEntry);
Qualtrics.SurveyEngine.setEmbeddedData("tracking_json", JSON.stringify(list));
```

This does the following:

- reads the Embedded Data field `tracking_json`
- parses it as JSON if it exists
- otherwise creates an empty array
- appends the current `trackingEntry`
- writes the updated array back to `tracking_json` as a JSON string

---

### 17. Update the stored page number

At the end of the submit handler, the script checks the submit type:

```javascript
if (type === "next") {
    Qualtrics.SurveyEngine.setEmbeddedData("page", page + 1);
} else if (type === "prev") {
    Qualtrics.SurveyEngine.setEmbeddedData("page", Math.max(1, page - 1));
}
```

- If `type === "next"`, it stores `page + 1` in Embedded Data field `page`.
- If `type === "prev"`, it stores `Math.max(1, page - 1)` in Embedded Data field `page`.

---

## Data recorded

This script stores page-level data with these fields inside each `trackingEntry` object:

- `page`: numeric page value read at load time
- `question_ids`: array of visible DOM IDs beginning with `QID`
- `start_time`: timestamp recorded on page load
- `time_on_page`: rounded page duration in seconds
- `mouse_moved`: whether any `mousemove` event occurred
- `mouse_move_count`: number of `mousemove` events
- `click_count`: number of `click` events
- `total_keys`: number of `keydown` events
- `paste_detected`: whether any `paste` event occurred
- `copy_detected`: whether any `copy` event occurred
- `tab_hidden`: whether `document.hidden` was ever `true` during `visibilitychange`
- `window_blurred`: whether any window `blur` event occurred
- `scroll_event_count`: number of `scroll` events
- `event_log`: array of timestamped event objects for `PASTE`, `COPY`, `TAB_HIDDEN`, `TAB_VISIBLE`, `WINDOW_BLUR`, and `WINDOW_FOCUS`
- `ts`: timestamp recorded when `trackingEntry` is created

---

## Embedded Data output

This script writes or updates two Qualtrics Embedded Data fields:

- `tracking_json`
- `page`

### `tracking_json`

This field contains a JSON string representing an array of tracking objects.

Example structure:

```json
[
  {
    "page": 1,
    "question_ids": ["QID4", "QID5"],
    "start_time": 1710000000000,
    "time_on_page": 18,
    "mouse_moved": true,
    "mouse_move_count": 92,
    "click_count": 3,
    "total_keys": 14,
    "paste_detected": false,
    "copy_detected": false,
    "tab_hidden": true,
    "window_blurred": true,
    "scroll_event_count": 2,
    "event_log": [
      { "event": "TAB_HIDDEN", "time": 1710000004000 },
      { "event": "TAB_VISIBLE", "time": 1710000009000 }
    ],
    "ts": 1710000018000
  }
]
```
