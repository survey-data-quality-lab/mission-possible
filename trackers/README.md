# Trackers

This directory contains the JavaScript **general**, **keylog**, and **fingerprint** trackers referenced in the paper’s appendix, plus **R script** to turn their JSON outputs into analysis-ready variables.

## Layout
- [`general/`](./general/) — page/activity tracker (focus/blur, visibility, scroll, idle, tab switches).
- [`keylog/`](./keylog/) — keystroke tracker for single-input pages (timestamped key events).
- [`fingerprint/`](./fingerprint/) — optional device/browser fingerprinting snippet (use only if compliant with your policies).
- [`R/`](./R/) — R code that converts trackers’ JSON logs to analysis-ready variables.
