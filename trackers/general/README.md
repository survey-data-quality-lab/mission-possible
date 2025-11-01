# Implementation Instructions

1. Copy code into the Qualtrics survey header under HTML view:  
   *(Survey → Look and Feel → Header → Source)*

2. Create two embedded data fields named `tracking_json` and `page` in the **Survey Flow**, before the first survey block.  
   Set `page` equal to `1`.

---

## Notes on Implementation

- There is a limit to the size of embedded data fields in Qualtrics.  
  Thus, the general tracker code only works reliably for short to medium-length surveys like ours (10 pages).

- For much longer surveys, one would need to modify the code to store data for sets of pages separately in different embedded data fields (e.g., `tracking_json_1`, `tracking_json_2`, etc).

- The longest tracking JSON in our data successfully stored 47 tracking entries.

- Note that the tracker generates multiple entries per page if the page is reloaded (e.g., when respondents did not complete all required fields).

- Therefore, **matching to survey pages should be done via `question_ids` and not via page numbers**.
