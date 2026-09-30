# Independent78 failed-sensor audit

The original results.json remains FAILED: passed:false, linked:false, one invocation. It separately records link_exit_code:0, headers/imports exit0, output567808 bytes and SHA ac16b362d0e56f888d5547aaba125e23ab67f88d13e2754b5336499a94cbaa15. These are saved observations, not an independent PE-byte inspection by this reviewer.

Actual imports.log has an MSS32.DLL group with decorated rows such as _AIL_startup@0 and _AIL_open_digital_driver@16. The original regex starts with a word boundary immediately before AIL; underscore and A are both word characters, so it cannot match these actual names. Its empty list is a concrete sensor failure, not evidence of missing Miles imports. Exact complete-set reconciliation is delegated to the prospective separate import-verifier-v2; this review does not mark the original gate passed or claim that verifier has run. No relink/VM/runtime occurred during this review or parser authoring.
