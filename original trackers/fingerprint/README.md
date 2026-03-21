# 1. Instructions for Device Fingerprinting Code

1. Open an account on [fingerprint.com](https://fingerprint.com) and obtain your **API key**.

2. Copy code into the Qualtrics survey header under HTML view (can be copied above or below other scripts):  
   *(Survey → Look and Feel → Header → Source)* 

3. Update the placeholder `YOUR_API_KEY_HERE` in the code with your actual Fingerprint API key.

4. Create embedded data fields named `page`, `visitorId`, `requestId`, and `fp_error` in the **Survey Flow** before the first survey block. Set page equal to `1`.

## Notes on Implementation

- This fingerprinting script **may be blocked** by certain browser settings or privacy extensions.

- Ensure that fingerprinting is **compliant with your institution's data privacy policies** before implementation.


# 2. Explanation of Device Fingerprinting Code

## Overview

This script runs when a Qualtrics survey page loads. It checks the value of the Embedded Data field `page` and proceeds only if that value is the string `"1"`. If the condition is met, it dynamically imports the FingerprintJS library, retrieves a fingerprint result, and stores selected values from that result in Qualtrics Embedded Data.

---

## Execution flow

### 1. Run on page load

The script is wrapped in:

```javascript
(function() {
  Qualtrics.SurveyEngine.addOnload(function() {
```

This means the logic is executed when the Qualtrics page loads.

The outer function creates a local scope and executes immediately.

---

### 2. Read the current page value

The script reads:

```javascript
var page = Qualtrics.SurveyEngine.getEmbeddedData("page");
```

This retrieves the value of the Embedded Data field `page`.

---

### 3. Check page condition

The script evaluates:

```javascript
if (page !== "1") { return; }
```

If the value of `page` is not equal to the string `"1"`, the function returns and no further code runs.

If the value is `"1"`, execution continues.

---

### 4. Initialize or reuse FingerprintJS promise

The script assigns:

```javascript
window.fpPromise = window.fpPromise || import('https://fpjscdn.net/v3/YOUR_API_KEY_HERE')
  .then(function(FingerprintJS) { return FingerprintJS.load(); });
```

This performs the following:

- checks whether `window.fpPromise` already exists
- if not, dynamically imports the module from the specified URL
- calls `FingerprintJS.load()` on the imported module
- stores the resulting promise in `window.fpPromise`

If `window.fpPromise` already exists, the existing promise is reused.

---

### 5. Request fingerprint result

The script continues with:

```javascript
window.fpPromise
  .then(function(fp) { return fp.get(); })
```

When the promise resolves, it receives an object (`fp`) and calls:

```javascript
fp.get()
```

This returns a promise for the fingerprint result.

---

### 6. Extract values from result

When the fingerprint result resolves, the script executes:

```javascript
.then(function(result) {
  var visitorId = result.visitorId;
  var requestId = result.requestId;
  console.log('visitorId:', visitorId, 'requestId:', requestId);

  Qualtrics.SurveyEngine.setEmbeddedData('visitorId', visitorId);
  Qualtrics.SurveyEngine.setEmbeddedData('requestId', requestId);
})
```

From the `result` object, it reads:

- `result.visitorId`
- `result.requestId`

It logs both values to the browser console and stores them in Qualtrics Embedded Data fields:

- `visitorId`
- `requestId`

---

### 7. Handle errors

If any step fails, the script executes:

```javascript
.catch(function(err) {
  console.error('FingerprintJS error:', err);
  Qualtrics.SurveyEngine.setEmbeddedData('fp_error', String(err));
});
```

This:

- logs the error to the console
- stores the string representation of the error in the Embedded Data field `fp_error`

---

## Data recorded

This script records up to three Embedded Data fields.

### `visitorId`

Source:

```javascript
result.visitorId
```

Stored with:

```javascript
Qualtrics.SurveyEngine.setEmbeddedData('visitorId', visitorId);
```

---

### `requestId`

Source:

```javascript
result.requestId
```

Stored with:

```javascript
Qualtrics.SurveyEngine.setEmbeddedData('requestId', requestId);
```

---

### `fp_error`

Source:

```javascript
String(err)
```

Stored with:

```javascript
Qualtrics.SurveyEngine.setEmbeddedData('fp_error', String(err));
```

---

## Conditions for execution

The script proceeds only when:

```javascript
page === "1"
```

If this condition is not met, no import or fingerprint request occurs.

---

## Embedded Data output

The script writes the following Qualtrics Embedded Data fields:

- `visitorId`
- `requestId`
- `fp_error` (only if an error occurs)

### Example (success)

```text
visitorId = <value>
requestId = <value>
```

### Example (error)

```text
fp_error = <error message>
```