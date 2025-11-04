# Trackers — R parsing utilities

R scripts to turn the trackers’ JSON logs into analysis-ready variables.

## What it does
- **General/browser tracker (`tracking_json`)**  
  - Maps your Qualtrics `question_ids` to page **tags** (via `nameQuestion()`), e.g., `consent`, `video`, `textInput`.  
  - For each tag it creates columns like:  
    `<tag>.page`, `<tag>.duration`, `<tag>.paste`, `<tag>.copy`, `<tag>.tab`, `<tag>.blur`, `<tag>.mouseMoveCount`, `<tag>.clickCount`.  
  - If a page appears **multiple times** (refreshes, back/forward), values are **aggregated** (sums for counts/durations; logical OR for booleans). Page indices are concatenated with `|`.

- **Keylog tracker (`key_log`)**  
  - Safely **salvages unfinished JSON** produced when Qualtrics hits its storage limits (closes arrays if needed).  
  - Parses keystrokes, computes:
    - `key_log.str` (pipe-separated keys), `key_log.num`, `key_log.mean`, `key_log.median`, `key_log.sd` (inter-keystroke ms),
    - `key_log.inputJump` (flags `INPUT_JUMP` events),
    - `key_log.wordCount`, `key_log.charCount` (based on your text item `Q16`),
    - `key_log.reconstructedInput` (rebuilds text from keystrokes),
    - `key_log.normDistReconOrg` (normalized similarity of reconstructed vs original using Levenshtein).

## Necessary input Variables
- `tracking_json`: JSON array from the general/browser tracker,
- `key_log`: JSON array from the keylogger (may be empty),
- `Q16`: the free-text response for reconstruction comparisons (rename in the script if different).
- And of course subject ids to later merge these variables with the rest of your data.

## Customize for your survey
- Edit `nameQuestion()` to map your **Qualtrics `QID`s** to page tags. The example mapping is **specific to our survey**.
- Column **naming convention** is arbitrary; we use `<tag>.<metric>` to keep it consistent with our Stata pipeline (which later shortens names).

## Notes & cautions
- **Multiple JSONs per page** are expected (refreshes, retries); the script aggregates them intentionally.
- **Qualtrics byte limits** can truncate long keylogs; the `salvage()` function closes incomplete JSON so rows remain usable.
