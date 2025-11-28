# Implementation Instructions

1. Open an account on [fingerprint.com](https://fingerprint.com) and obtain your **API key**.

2. Copy code into the Qualtrics survey header under HTML view:  
   *(Survey → Look and Feel → Header → Source)*

3. Update the placeholder `YOUR_API_KEY_HERE` in the code with your actual Fingerprint API key.

4. Create embedded data fields named `page`, `visitorId`, `requestId`, and `fp_error` in the **Survey Flow** before the first survey block. Set page equal to `1`.

---

## Notes on Implementation

- This fingerprinting script **may be blocked** by certain browser settings or privacy extensions.

- Ensure that fingerprinting is **compliant with your institution's data privacy policies** before implementation.
