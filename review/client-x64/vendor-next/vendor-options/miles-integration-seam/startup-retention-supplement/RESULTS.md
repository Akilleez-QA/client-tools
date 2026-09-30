# Supplemental SessionInputs retention checks

15/15 pass on native v120 Win32/x64 Debug/Release, and 15/15 on the host under ASan/UBSan. No vendor DLL or engine program was executed.

The same frozen v4 metadata owner retains two small payloads, then two additional live payloads that fill exactly MaxFrameBytes logical bytes. Earlier pointers and contents remain valid across all insertions. A further one-byte request returns null, leaves retainedBytes unchanged and preserves all four payloads. These are ordinary successful allocations and an explicit budget rejection, not injected allocation failures or RSS/capacity measurements.

Native receipt: `cdcb86d4920241202bb8ff1e448d3841f6c88265b3f0b90fa41fd1d754ea6ba4`. Exact linked PE hashes and input identities are in verified-results.json and evidence/receipt.json. Frozen metadata header SHA256 `b9c8bbfb3cff6afbe85db418fa32428d1d649308bdaef1fa78bb0eb4ca40f1e8`; implementation `14c2466b9a9fdcaadfd94b4dc930913a7268e429b15484eef18634a1afdb6fa2`.

This is separate from the canonical 39 portable checks and 35 genuine vendor observations. It does not expand those totals or establish asynchronous vendor retention, concurrent access or complete session lifetime correctness. No production changes, commits or pushes.
