# Instructions for Qualtrics Survey File

This directory contains Qualtrics survey files that can be imported into Qualtrics.  

The .qsf files include our three tracker codes: the **General Tracker**, **Key Log Tracker**, and **Device Fingerprinting**.

1. Use [Mission_Possible_Survey_V1.qsf](./Mission_Possible_Survey_V1.qsf) for collecting your own data. It integrates by default with our new data cleaning code. It also has an updated general-purpose consent form.
2. Use [Mission_Possible_Baseline_Survey.qsf](./Mission_Possible_Baseline_Survey.qsf) to see an older version documenting the exact wording of the Baseline Survey in our paper.

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

## 2. Update the Integration with the Survey Platform

1. Set the redirect link in the survey flow.
2. When not running on Prolific, update the embedded data fields to record participant ids and adapt the question for recording the participant id in the survey.

---

## 3. Update Survey Details

1. Adapt payment details (set `showup' in the survey flow).
2. Adapt the consent form.

---

## 4. Update the Device Fingerprinting API Key [OPTIONAL]

The survey includes JavaScript in the survey header that performs device fingerprinting.
You must replace the placeholder API key with your own fingerprint API key to use device fingerprinting.

### Steps

1. Open the survey in the **Survey Editor**.
2. Navigate to: **Survey** → **Look and Feel** → **General** → **Header**.
3. Click **Source** (left of "Less...") to open the HTML editor.
4. Locate the placeholder text `"YOUR_API_KEY_HERE"` and update it with your API key obtained from Fingerprint.com.
5. **Save**, **Apply**, and **Publish**.

---

## 4. Run the Study [OPTIONAL]


