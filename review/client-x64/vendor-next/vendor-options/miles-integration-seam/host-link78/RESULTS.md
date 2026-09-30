# Host74 link and import-sensor correction

The one actual v120 link joined the 18 x86 objects from native74 with six explicitly pinned real libraries, including the possessed Mss32 import library. Linker exit was zero; the output was an x86 PE of 567,808 bytes, SHA256 `ac16b362d0e56f888d5547aaba125e23ab67f88d13e2754b5336499a94cbaa15`. Input objects, libraries and tools remained unchanged. No stub or alternate supplier was linked. The target was never executed.

The first overall gate FAILED at import verification. Its regex required a word boundary before AIL and missed the leading underscore in actual Win32 names. The raw failed receipt remains unchanged. Independent source review identified that deterministic parser defect; this is not an excuse based on a suspected runtime problem.

Root reviewed the separate frozen import verifier, then ran it once locally. One miniature positive and seven negative fixtures passed. The exact 50 decorated imports under MSS32.DLL matched the earlier object expectations, including stack-byte suffixes. It rejected wrong DLL placement, missing/extra imports, incorrect suffixes, duplicate rows and undecorated tokens. This checks the same saved dump; there was no relink, second PE inspection or DLL load. See import-verifier-v2/result-v1.json.

The combined observations establish symbol resolution for this74 host against the possessed import library. They do not establish runtime DLL compatibility, playback, callback scheduling, clean teardown or an x64 client link. Newer77 has its own object builds but was not the host linked here. Binary/map/SDK files remain private; authored source and text records are published.
