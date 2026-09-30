# Tests-only first-run results

Both strict C++11 ASan/UBSan executables passed their first compile and scripted run. No repair/retry. All83 inherited37 files retain their manifest hashes, including every implementation/header. Owned test source is byte-identical to frozen35. Native38 remains unexecuted; no VM, SDK/vendor or engine code was run.

New named scenarios passed:

- Two live streams and distinct borrowed samples; closing the first preserves the second and its cached alias.
- Duplicate live stream wire identity poisons without publishing a second return.
- Cross-parent borrowed alias reuse poisons; no subsequent channel call.
- Successful null alias with wrong parent slot, and with malformed parent kind, each poisons before returning output.
- Known open refusal leaves caller return target unchanged and permits later successful open.
- Uncertain open leaves caller return target unchanged and prevents further channel calls.

Inherited stream scenarios passed, including exactly one256-cycle open/close sequence. Inherited owned35 scenarios passed against37 helpers:19 controls, optional output masks, bit patterns, alias consistency, known refusal vs uncertainty, no partial output mutation and borrowed-allocation rejection. Assertion counters in raw logs are diagnostic, not numbers of independent behaviors; no fixed count assertion or performance claim is used.

Source SHA256d337a93cbb349a8e8b110bbf27dbb2e4305b3380ee066ef2197603066d0afd2c; manifest a35b77881a33da17c6594bbcd25d400769651723c96cf20f6328f9c62af18d48; portable receipt73ab33eb41ed55e049fa741fadf0b72d4909a80842c45f82e7ade50bab875f41.

No concrete implementation failure appeared in these scenarios. The SDK stream-sample stability assumption remains unproved; successful scripted tests cannot establish it. Backend still refuses stream open until real file-channel/host lifecycle integration. No readiness or callback implementation was manufactured.
