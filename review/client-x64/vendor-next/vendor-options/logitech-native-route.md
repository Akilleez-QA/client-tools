# Logitech LCD native route — 2026-09-30

**New evidence retracts any claim that no official x64 Logitech SDK is available.** The current developer page's HTML retains `https://www.logitechg.com/sdk/LCDSDK_8.57.148.zip`, although the readable page lists only wheel/LED. It downloaded successfully from Logitech. Package SHA256 b60394a555eec0e79e04f7c9cf2a681e2f6a80c67d861c9ba67ea44c84e57fe5. README identifies 2014 LCD SDK with x86/x64 libraries and G15 v1/v2, G13, G510/G510s, G19/G19s support. Package files remain private, outside Git.

Official [LGS 9.04.49 x64 support page](https://support.logi.com/hc/de/articles/6330888992023-Logitech-Gaming-Software) links an installer also downloaded privately. SHA256 6db9f6442d46fbde0953f8bfbc36bd714e5e31a62f927563594cafd60724d3e0. Native Get-AuthenticodeSignature: Valid, Logitech Inc signer, version 9.04.49. Extraction only: no installer, registry, service or hardware changes. It contains both x86/x64 LgLcdApi.dll and LogitechLcd.dll; it did not contain old lglcd.h or lgLcd.lib. Full provenance and SDK file hashes: logitech-package-identity.json.

Native v120 smoke compiled and linked the official new SDK header/library on **both Win32 and x64** (`lcd-sdk-v1/results.json`); the program takes the real LogiLcdInit address, forcing the archive member. It was **not run**, so no manager/hardware behavior is claimed. This is not a complete SWG wrapper build.

## Why this is not a drop-in

The repository uses low-level header version1.02 (2006), 16 source UI wrappers, and an i386 lgLcd.lib loader. The loader's imported Windows functions and strings identify a registry lookup under `SOFTWARE\Classes\CLSID\{FE750200-B72E-11d9-829B-0050DA1A72D3}\ServerBinary`, LoadLibraryA and GetProcAddress("GetInterface"). The transport implementation is outside the repository. We inspected import/export tables and strings, not an undocumented function-table implementation.

Actual wrapper uses: lgLcdInit/DeInit, Connect, Disconnect, Enumerate, Open, Close, ReadSoftButtons, UpdateBitmap, SetAsLCDForegroundApp. LCDOutput.cpp submits asynchronous priorities, removes the display at idle priority, enumerates device0, reconnects after unplug/errors, and controls foreground. SwgCuiG15Lcd.cpp:403 calls SetAsForeground(true), so this is not unused wrapper surface.

New SDK exposes LogiLcdInit, IsConnected, IsButtonPressed, Update, Shutdown, MonoSetBackground/Text and color counterparts. It supports a 160×43 byte bitmap, so keeping SWG's existing GDI render and copying that bitmap is plausible. Using the SDK's text renderer instead would change fonts/layout. But the public header has **no equivalent explicit foreground/priority/connection-handle/device-enumeration controls**. Manual says buttons are pressed only while applet is foreground. Therefore identical pixels alone do not establish equivalent interaction/arbitration. LgLcdApi.dll exposes GetInterface rather than named lgLcd functions; a matching private ABI cannot be inferred merely from that export.

The new SDK manual contains an SDK EULA (pages13 onward); no SDK redistributed. Before distribution, review actual rights for packaging its libraries; availability and a successful link do not establish distribution permission.

## Fidelity and next discriminator

Preferred investigation: locate an official legacy low-level x64 SDK matching the existing wrapper before adapting to the newer high-level interface. Failing that, compare the new SDK on physical supported hardware against stock: exact bitmap bytes and pixel presentation, all four soft buttons/edges, forced foreground, competing applet priority, background/idle transitions, unplug/replug, manager shutdown/restart, multiple displays, disabled-config startup and client exit. Keep same Logitech manager version and device firmware on both sides. Emulator can check pixels/API sequencing, not hardware/driver equivalence.

A 32-bit helper retaining original lgLcd API may retain arbitration better but still changes callback threading/update timing and process registration lifetime. A direct HID/libg15 alternative changes the manager entirely: [source](https://github.com/mike-petersen/g15tools/blob/master/libg15/libg15.c) uses libusb, claims device interfaces and on Linux may detach an existing driver; it is not a behavioral substitute for Logitech's applet manager. That source carries GPLv2-or-later, not a permissive license. No devices touched and no such alternative integrated.

Delivery: investigated and official SDK link-probed. Highest justified claim: genuine x64 SDK and runtime DLLs are obtainable, but SWG's low-level API compatibility and original hardware experience remain unproven. Next hardware observation is controlled by whoever can provide the supported Logitech device; software-only ABI investigation can continue locally.

## Legacy low-level SDK found — supersedes need for high-level adaptation

An old official CDN path is still live: `https://download01.logi.com/web/ftp/pub/gaming/keyboards/lgps306_x64.exe`. It downloads the genuine 3.06 package; SHA25689b5f5cf21a7fc310414ee4e9c34b00081ad0ad5479c2e53bee10ca9a001dbd6, native Authenticode Valid, signer Logitech/OU Gaming, thumbprintACC2DDA18693513C66DB2F8C2A1234A72823C4DB. The historical filename/path was a discovery lead; current HTTPS bytes/signature are the provenance observation. Extracted outer archive→GPInst.msi→LADPSDK_zip, never installed.

It contains **real x86 and x64 lglcd.lib**, low-level header3.01, docs and LCDUI source. All ten API operations used by SWG remain declared/exported, including SetAsLCDForegroundApp, priority-bearing UpdateBitmap and original Connect/Enumerate/Open. Both A/W Connect exports are present. The included low-level SDK license PDF has copyright2010 and the standard permissive permission/notice/warranty form; this differs materially from the high-level SDK EULA. No package files added to Git. SDK/library/header/license hashes are in logitech-package-identity.json.

Native evidence:

- **64/64 real wrapper TU compiles:** all16 unchanged repository LCDUI sources, Win32/x64 × Debug/Release (`lcd-legacy-v2`). Existing project defines/include paths, PCH disabled; this is compilation, not unchanged full-project codegen proof.
- **4/4 original-header low-level API link probes:** all11 symbols (ten operations plus both ConnectA/W variants), genuine low-level SDK library, Windows providers only. No stub and no execution (`lcd-api-link-v1`).
- **4/4 old/SDK header layout comparisons:** deviceDesc16 and bitmap6884 both ABIs; Win32 connect24/connectionOffset20/open20/deviceOffset16/configure8/softbuttonContext8; x64 connect40/connectionOffset32/open32/deviceOffset24/configure16/softbuttonContext16. Both actual headers agree. This sampled layout validation does not establish every callback/constant/protocol rule.
- Whole-wrapper executable experiment retained as **failed**, not claimed passing: v1 probe missing include path; v2 correct wrapper builds but old STLport autolink unresolved; v3 explicitly supplies genuine v120 repository STLport and changes stale library input selection, leaving the real `operator new(size_t, MemoryManagerNotALeak)` dependency. No fake allocator added. Full client will need its actual allocator/export provider.

The newer low-level SDK is the favored route now; the high-level API adaptation and HID rewrite are unnecessary unless this route fails intended-use acceptance. Keep existing Win32 provider unchanged. Before production integration, explicit SDK root plus architecture selection must find the genuine x64 library, retaining original source headers/UI and real STLport/allocator providers. Full client linkage and same-manager/device tests still outstanding.

Caveat from official low-level manual: `isPersistent` is ignored from API3.00 onward, and enumeration/index-open are deprecated but still documented. This does not prove an x64 regression: stock Win32 clients on the same newer manager may already have that behavior. Hold manager version constant and compare Win32/x64 before attributing differences to architecture.

## Current whole-wrapper outcome

The later real-wrapper-v4 run supersedes the earlier failed link attempts without deleting them: all16 unchanged wrapper TUs are linked into real executables on Win32/x64 Debug/Release, using genuine SDK archives and actual SWG core/allocator providers. All four links return0; `executed:false` remains explicit. [Exact inputs and results](lcd-integration/results-v4.json). This establishes neither complete SwgClient integration nor hardware behavior.

The criticism of `_STLP_DONT_FORCE_MSVC_LIB_NAME` was mistaken: tracked `config/stl_select_lib.h:12` does consume it. A default recursive search skipped that directory because of the repo ignore rule. The macro suppresses automatic legacy naming; explicit link inputs and path selection are a separate route that also needs the matching provider. Native property evaluation now confirms preserved Win32 settings and an x64-only SDK directory with a hash-checked genuine archive. No provider replacement, stub, installed service or hardware change occurred.
