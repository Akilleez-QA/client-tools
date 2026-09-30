# Composer native-call review62 — parent reconciliation

Composer2.5 read the supplied authored plain60 sources and returned exit0. It found no concrete argument-order/signedness inversion. It proposed optional null-output checks, a second WAV result check inside the private delegate, and concern about treating nonzero WAV status as success. These are source-review suggestions, not observed failures or independent runtime evidence.

Parent checked the actual caller and prior bounded output analysis. Product49d0 Audio.cpp:3710–3712 itself branches on the actual nonzero AIL_WAV_info result.60 preserves that rule and leaves the projected output unchanged at zero. Public WAV_info checks its required nonnull output before entering the private delegate; inventing bypass callers does not establish a defect on this boundary. Private delegate preconditions remain explicit.

The four getter pairs deliberately forward optional/aliased pointers unchanged. The possessed original-DLL static inspection in output-static33/OUTPUT-STORES-REVIEW33.md establishes individual null checks and write ordering for its scoped normal paths. Adding blanket nonnull checks would narrow that existing interface. It would not prove the eventual x64 SDK behaves identically. No speculative pointer-validation patch is made.

Composer's missing Preference/Speaker assertion note excludes the unchanged52 native startup TU, where these assertions already exist. Native54 actually compiled that TU; this does not validate the50 new60 calls. Opaque object pointers round-trip without dereference or integer narrowing; real type assertions and imports for60 still require the separately prepared62 compiler gate. No unsafe callback function-pointer cast or forged native library is introduced.

Independent Astra source review read the possessed declarations and all nine60 files, with no blocking source defect identified. Same source/model-family review agreement is not runtime corroboration. Three callback registrations, actual x64 Miles library, full client/adoption/fidelity remain incomplete.
