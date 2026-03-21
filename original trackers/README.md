# Trackers

This directory contains the JavaScript general tracker, keylog tracker, and fingerprinting script referenced in the paper's appendix, plus R code that turns their JSON outputs into analysis-ready variables.

## Layout
- [general tracker/](./general%20tracker/) — Qualtrics page and activity tracker that records page timing, clicks, key counts, scroll activity, paste/copy events, tab visibility changes, and window focus changes.
- [keylog tracker/](./keylog%20tracker/) — Qualtrics keystroke tracker for open-text responses, including timestamped key events and large input jumps.
- [fingerprint/](./fingerprint/) — optional device and browser fingerprinting snippet for Qualtrics; use only if it is compliant with your institution's data privacy policies.
- [code for cleaning/](./code%20for%20cleaning/) — R scripts that parse `tracking_json` and `key_log` into analysis-ready variables.
