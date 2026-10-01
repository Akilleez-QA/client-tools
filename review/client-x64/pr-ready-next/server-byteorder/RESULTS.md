# Server Windows byte-order counterpart

[Fork draft #2](https://github.com/Akilleez-QA/src/pull/2) has one source-only commit, `adb1bc91d2ad0a923a828204410c72d7cab9dbc1`, above the combined PR #37/#38 base `09932a32c9949bd40e8e4dbb22e1a7027944eb21`. GitHub confirms one file, +26/−0. The source patch applies to master as well; the stacked base preserves the foundation helper and repaired inherited workflow.

[Description](PR.md) and [identity comparisons](receipt.json) distinguish the identical conversion implementation from different server include context. Existing client native/hosted leaf-function results apply to the implementation only; no server Windows compile or runtime claim is made. Primary review checked the source delta and dependency statement. No new tests or build were run during packaging.
