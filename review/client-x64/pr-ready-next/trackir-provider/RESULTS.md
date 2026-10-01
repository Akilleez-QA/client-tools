# Trackir provider

Candidate `12e1a62160f83827ad345ddf8fb8a53299b5060a`, prerequisite base `949451032647e45e42c3aaef3f41b132c8af36e3`. [Description](PR.md), [exact file identities](receipt.json), and [independent review](INDEPENDENT-REVIEW.md). Candidate hashes and dependency ancestry were checked before publication.

The original capacity finding is preserved in the initial review; the [fix review](INDEPENDENT-FIX-REVIEW.md) closes that narrow source issue. [Native registry-contract records](registry-contract/RESULTS.md) cover16cases/32queries per ABI. The original runner and hardened reproduction runner are separate artifacts. Root inspected the hardened validator and saved-record controls. This is not execution of the production loader or hardware.

To reproduce on Windows with v120 and Python3, copy only `probe.cpp`, `prospective-contract.json`, `run-id.json` and the current `run-native.py` from registry-contract into a fresh empty directory, then run `python run-native.py`. Do not copy the existing Win32/x64 outputs into that directory. The test uses a uniquely named temporary HKCU key, requires new-key ownership, and removes it. A nonzero exit is failure. No provider SDK or DLL is needed.
