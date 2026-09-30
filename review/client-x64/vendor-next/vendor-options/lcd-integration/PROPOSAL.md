# Original Logitech LCD integration proposal

2026-09-30; no production LCD edits. Current SWG Source baseline keeps this hardware feature. Browser/TCG deprecation does not imply LCD deprecation.

## Dependency route

Use the genuine low-level Logitech LCD SDK embedded in the signed official package, not the newer high-level LogiLcd API. Download only from:

https://download01.logi.com/web/ftp/pub/gaming/keyboards/lgps306_x64.exe

SHA256: `89b5f5cf21a7fc310414ee4e9c34b00081ad0ad5479c2e53bee10ca9a001dbd6`.

Package signature verified Valid on Windows (Logitech; package version 3.06). Extract only: EXE → `1b-GamePanel-x64/GPInst.msi` → `LADPSDK_zip` → `LCDSDK/Lib/x64/lglcd.lib`. Do not run installer or modify driver/device state. Keep SDK/license private and out of Git; retain official license locally. Detailed file hashes, signature and API evidence: `../logitech-package-identity.json`, `../logitech-native-route.md`.

## Smallest configuration change proposed for parent

An explicit external property `SwgLogitechLcdSdkDir` points to extracted `LCDSDK` root. On x64 **SwgClient only**, place `$(SwgLogitechLcdSdkDir)\Lib\x64` before inherited library directories. Require this exact library exists before Link, and validate its archive machine against x64 using the existing dependency-validation mechanism or a bounded archive inspection. Do not autodownload and do not silently fall back to the repository's x86 archive. Prefer replacing the specific legacy LCD library directory in x64 evaluated paths rather than accumulating ambiguous providers. Preserve both explicit `lgLcd.lib` input and the existing source `#pragma comment(lib, "lgLcd.lib")`; they then select the same genuine provider. No change to Win32 configuration, headers, providers, wrapper source or priorities.

Current XML has x64 lcdui output directories but still carries `src/external/3rd/library/lcdui/lib` (x86) in both x64 SwgClient link configurations. The `lcdui` target itself is a static archive and need not link the SDK; its project reference to sharedMemoryManager stays. `LCDOutput.cpp` auto-links `lgLcd.lib`. New SDK header layout checks already match original header for structures the wrapper uses. Keep the original public header; replacing it is unnecessary.

This is a proposal for the parent's shared build-properties work, not a second configuration framework or a SDK-bundling change. Renderer/JPEG/STLport properties do not currently apply to the executable; shared dependency settings must be deliberately imported there if reused.

## Evidence ceilings

All 16 unchanged wrapper TUs compile on Win32/x64 Debug/Release. All 11 old low-level entry points link against the official matching-architecture SDK. New/old structure layouts match in 8 native probe runs. Complete wrapper/core link is being tested separately. No manager service, connected LCD, foreground arbitration, priority scheduling, button delivery or reconnect behavior has run. The SDK retains these APIs; API presence is not hardware acceptance. SDK 3.01 documents persistence ignored since 3.00, a manager-version difference that must be compared on both ABIs.

## Candidate files for parent review

`logitech-lcd.props` and `validate-logitech-lcd.py` are scratch files only. Import the props after existing executable item definitions (e.g. via the parent's x64 common props); its conditions limit action to x64 SwgClient. It prepends the external SDK's correct directory. The exact archive SHA gate rejects the x86 library or any changed provider before build/link; both positive x64 and negative x86 checks have run locally. Actual MSBuild import/evaluation and full executable resolution with this props file still need the build agent's isolated integration pass. This must not be claimed proven by the earlier direct wrapper link.
