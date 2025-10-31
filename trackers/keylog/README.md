# Implementation Instructions

1. Copy code as **JavaScript** into the open text survey question.

2. Create one embedded data field named `key_log` in the **Survey Flow**, before the first survey block.

---

## Notes on Implementation

- The keylog tracker may not work properly if **multiple text input fields** are present on the same page.  
  In such cases, the code would need to be modified to associate keystrokes with specific or all text input fields.

- Given the limit to the size of embedded data fields in Qualtrics, the keylog tracker will track approximately the **first 1000 keystrokes**.
