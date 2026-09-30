# Bounded native Vivox result

Native VS2013 v120, private C:/vendor-vivox-probe only. Actual provider3.0.0005.7314 from SWG Source client v3.0, exact PE/header/source hashes in manifest.json and binary-inventory.json.

- Win32: all52 actual wrapper imports resolve; provider string allocation/free and unissued request creation/destruction pass, exit0.
- Win32 v2: original SDK XML helpers round-trip synthetic cookie and request type87; no request issued, exit0.
- x64: samex86 provider LoadLibrary fails with error193; expected architecture rejection, not an x64 voice pass.
- Existing SWGVoiceService.exe inspected only, never executed. Its PE isx86 and it imports vivoxsdk.dll.
- No connector/account/service initialization, network request, device enumeration request or audio operation was performed. No credentials or real endpoints read or written.

These observations establish the local ABI boundary, not live voice functionality. See ../vivox-options.md for the critical disabled-baseline source gates and saved-preference caveat. The existence of a legacy out-of-process service does not remove the in-process SDK dependency; it also does not make restoration of this disabled feature necessary for the x64 target.
