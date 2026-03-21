# Instructions for Qualtrics Survey File

This directory contains a Qualtrics survey file of our baseline survey which includes the three tracker codes of the **General Tracker**, **Key Log Tracker**, and **Device Fingerprinting**. 

This survey file should be ready to use after uploading to Qualtrics; only device fingerprinting will require you to update it with your API key.

The survey is set up for **Prolific** as it asks for the Prolific ID on page two, and records `PROLIFIC_PID`, `STUDY_ID`, and `SESSION_ID` as embedded data fields.

Tracking data is stored in embedded data fields:

| Field | Description |
|---|---|
| `tracking_json` | Records data for the **General Tracker** running on all pages |
| `key_log` | Records keystroke data from the **Key Log Tracker** in the open text question (Q16) |
| `key_log2` | Records keystroke data from the **Key Log Tracker** in the video check (Q34) |
| `visitorId` / `requestId` / `fp_error` | Stores data from device fingerprinting (optional) |

These can be cleaned using the R code provided under `\trackers\R`.

Code for recording Prolific's Authenticity Check is not included, but can be added following Prolific's latest instructions.

---

## 1. Upload the `.qsf` File to Qualtrics

1. Log in to **Qualtrics**.
2. Go to the **Projects** dashboard.
3. Click **Create new project**.
4. Select **From a File** (or **Import a QSF** depending on your interface).
5. Upload the provided `.qsf` file.
6. After the import completes, open the newly created survey project.

---

## 2. Update the Device Fingerprinting API Key [OPTIONAL]

The survey includes JavaScript in the survey header that performs device fingerprinting.
You must replace the placeholder API key with your own fingerprint API key to use device fingerprinting.

### Steps

1. Open the survey in the **Survey Editor**.
2. Navigate to: **Survey** → **Look and Feel** → **General** → **Header**.
3. Click **Source** (left of "Less...") to open the HTML editor.
4. Locate the placeholder text `"YOUR_API_KEY_HERE"` and update it with your API key obtained from Fingerprint.com.
5. **Save**, **Apply**, and **Publish**.


