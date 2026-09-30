# SWG Source baseline correction

2026-09-30. The user explicitly directed this effort to the SWG Source copy, supplied the Client v3.0 release and the project's VM v3.0.2 announcement, and asked us to read the project documentation. The preservation target is the SWG Source client experience. Restoring every historical SOE component is not part of the x64 conversion.

The earlier vendor inventory correctly identified real leftover code and binaries but over-expanded the acceptance scope. This correction applies to every vendor dossier and option table: classify intentional upstream removals before spending time on provider replacement.

## Evidence

- The [official client-tools README](https://github.com/SWG-Source/client-tools#deprecated-components), also present at our base `94945103`, lists browser, TCG, help/bug UI and Perforce integration as removed or disabled. Its known-issues section explicitly identifies lingering Mozilla link problems. Qt is described as a development-tool dependency.
- [Commit 68e4f185](https://github.com/SWG-Source/client-tools/commit/68e4f185bfdb61c5c4b17f3c880adfa0a8883037) (2017) deliberately disabled the browser implementation. The unusual guards emit native MSVC C4067 warnings but exclude the inspected implementation bodies; they must not be misread as equality expressions.
- [Commit 82c76fe8](https://github.com/SWG-Source/client-tools/commit/82c76fe8599b4652cf8de72bd361631e221f83ef) (2020), an ancestor of our base, removed browser commands, disabled voice controls/commands and noted the prior removal of TCG/help menu choices. `setVoiceChatEnabled` returns immediately. Remaining saved-preference/config/server paths still need auditing before calling all Vivox code unreachable.
- Native preprocessing/compilation confirms absent browser implementation references in Win32/x64 Debug/Release. The fresh Win32 product has no Mozilla/NSPR/XUL imports. A separate COFF audit reports no consumer references to the 153 exported libMozilla namespace symbols across the 64 other fresh Release archives; the subsequent no-input relinks passed on Win32 Debug and Release, with whole-executable equality after normalizing timestamps and PDB age only (see the integration-current/mozilla-link-proof-v2 packet).

## What changes in the plan

**Browser and TCG are deprecated-component/build-cleanup investigations, not features to recreate as a requirement of this migration.** Keep remaining data/API assumptions explicit; prove clean builds without stale inputs. No x86 header macro workaround is appropriate for Mozilla.

**Vivox is a deprecated-interface/reachability investigation first.** The original runtime/ABI inventory can establish what remains, but a service migration or voice helper is not justified merely because vendor files remain. The worker is tracing all activation paths.

Miles remains a genuine audio dependency. Bink, LCD, TrackIR, capture and other providers must each be classified from current project scope and actual callers. No general permission to delete features follows from the browser's deprecation.

## Release and documentation identity

The [Client v3.0 release](https://github.com/SWG-Source/releases/releases/tag/swgsourceclientv3.0) contains split-volume download instructions, not a feature changelog. Its GitHub publication timestamp is 2024-02-09. The [VM v3.0.2 release](https://github.com/SWG-Source/releases/releases/tag/swgsourcevmv3.0.2) is a separate server appliance. The supplied Discord screenshot identifies both packages but is not a current runtime test.

The installed directory is named `SWGSource Client v3.0`; its `version.txt` contains `3.0.1`, and its packaged README describes the client-assets updater. Therefore directory name alone does not pin executable/assets to a pristine release. Preserve binary/asset hashes and updater revision for acceptance rather than silently updating the reference installation.

The [project wiki](https://github.com/SWG-Source/swg-main/wiki) links setup and update procedures. These are documentation sources; this investigation did not run the client updater, replace the VM, change network settings or mutate upstream repositories.
