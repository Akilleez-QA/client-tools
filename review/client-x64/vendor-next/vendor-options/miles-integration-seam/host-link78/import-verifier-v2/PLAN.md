# Import verifier v2 — prospective, NOT RUN

Run only `python3 test_verifier.py` after parent review. This reads frozen text, exercises one miniature positive and seven negative fixtures, then compares the actual78 dump with exact decorated import tokens derived from74 x86 UNDEF symbols by removing only __imp_. No compiler, linker, subprocess, VM, PE reading or target execution occurs. Inputs are hashed before/after. Preserve the original78 runner, receipts and failed first gate unchanged.

The parser recognizes complete DLL group headings, the four observed metadata lines and complete hex-hint/name rows. The complete Mss32.dll token set must match, including each leading underscore and @stack-byte suffix. Duplicate groups/imports, unrecognized lines inside groups, missing summary, unexpected Miles tokens and Miles tokens under another DLL fail. Seven negative fixtures cover wrong DLL, missing/extra import, wrong stack suffix, duplicate row, undecorated token and a duplicate Miles token under another DLL. The accepted format is intentionally scoped to this dumpbin12 observation, not a universal dumpbin parser.

A later successful verifier run would reconcile a faulty first-gate import sensor against its frozen dump. It would not rerun or retroactively pass78, independently inspect PE bytes, or establish runtime compatibility.
