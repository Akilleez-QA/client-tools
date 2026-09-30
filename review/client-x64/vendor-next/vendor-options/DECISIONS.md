# Third-party decisions for the x64 client

Updated 2026-09-30. No replacement backend has been selected. Work continues on the native client and on the experiments below. The requirement is the original SWG Source game experience and fidelity, preserving its supported features and documented removals. See [baseline correction](BASELINE.md); this is not a restoration of every historical SOE component. A DLL that loads, a successful link, or a matching feature list cannot establish that result.

**The most promising currently available experiment is to retain the original 32-bit media implementations behind a carefully measured process boundary. That is a hypothesis, not an architecture decision.** Matching historical native x64 SDKs or original source could be better for active dependencies, but none has been established locally for Miles or Bink. Vivox first needs a current-baseline reachability decision because SWG Source disabled its normal user controls. Meanwhile, several supposed blockers are source-buildable, configuration-specific, or unused scheduled projects. Treating all of them as one vendor replacement problem would add unnecessary change.

## What the tests have established

| Test | Actual result | What it does not establish |
| --- | --- | --- |
| Original Miles 7.2a native DLL | Loads; 61 used exports resolve. The 62nd lexical API name is a version-resource macro. Original MP3 plugin decodes a real game asset. | An x64 implementation, live playback, room effects or helper timing parity |
| Same MP3 through replacement decoders | All produce 107,136 stereo frames at 44.1 kHz, aligned at offset zero. FFmpeg differs from Miles in 23,736/214,272 samples; miniaudio in 23,778. Maximum absolute difference is 502 signed-16-bit units. | Audibility, accepted error tolerance, or equivalence of streaming/mixing. These are differences on one asset, not a verdict on every asset |
| Original Miles under private Wine null output | Original cached sample and stream complete, with one EOS each. Native VM has no output endpoint. | Real-time latency or listening fidelity: the null sink runs faster than the nominal clip duration |
| Original Bink 1.9c | Decodes 32 frames of a public non-SWG sample; x64 driver transports four nonblack frames. All four differ from FFmpeg (RGB up to 5, alpha 0 versus 255). No audio track exists in that sample. | Game movie playback, frame conversion, audio synchronization, TreeFile integration or a working x64 player |
| Actual vendor consumers, native v120 | 24/24 TU compile/preprocess combinations. Browser bodies absent in all four configurations; TCG/LCD references present; capture references Debug only. | Complete final executable or dynamic module closure |
| Official Logitech LCD SDK | Genuine x86 and x64 libraries compile/link with v120. | Drop-in compatibility: newer public API lacks the old foreground/priority controls SWG uses |
| TrackIR | Official vendor SDK selects NPClient64.dll on x64; SWG requests NPClient.dll on both. Legacy/current header layouts are being checked. | Profile 6001 acceptance or physical head-tracking/cockpit behavior |

The asset census found 5,900 nonempty WAV entries (all PCM or extensible PCM), eight empty entries and 373 MP3 entries across the inspected TREs. Counts include patch duplicates. No game Bink movie was found in the inspected installation; that is a coverage limitation, not permission to remove movies. [Miles evidence](miles-probe/RESULTS.md), [Bink evidence](bink-probe/report.md), [native reachability](native-reachability.md).

## Decision by dependency

| Dependency | Options worth retaining | Principal downside / fidelity risk | Next decision-changing evidence |
| --- | --- | --- | --- |
| **Miles audio** | Matching original native SDK/source; original 32-bit runtime host; separately evaluated native OpenAL/miniaudio/XAudio2/JUCE/FMOD implementation | Host changes command/callback timing and ownership. Replacement changes decoder, resampler, panning, reverb, looping and clipping. JUCE provides building blocks, not Miles behavior. | Stock command/output trace with real output device, room presets and looping; original-runtime host replay using the same workload. Keep measured decoder differences visible. |
| **Bink video** | Matching native SDK; original Bink plus Miles in one 32-bit media host; native FFmpeg decoder/player | Bink currently consumes the Miles driver in the same process. Separating them changes sound-provider/clock coupling. Decode parity alone omits presentation, skip/seek, device loss and audio. | Decode nonblack frames and audio with the original runtime; compare independently converted outputs without tuning the oracle. Then test an actual SWG movie and D3D presentation. |
| **Vivox voice (normal controls disabled)** | Audit remaining saved-setting/server paths before any provider decision; retain existing disabled baseline | SWGVoiceService.exe does not eliminate the client-side vivoxsdk.dll. A new SDK may require new authentication/provisioning and change channels, spatialization, codecs, PTT and events. A helper cannot resurrect an unavailable service. | Audit saved preferences, direct setters and server-message activation; disabled UI alone does not prove all code unreachable. Source-only assumptions cannot decide service availability. |
| **Mozilla/browser (deprecated)** | Prove current non-use and repair build scheduling; restoration alternatives are outside current scope | Source guards currently exclude the inspected UI. Porting an unused project may be unnecessary. Restoring/changing browser behavior, page rendering, input, cookies or TLS is separate feature work. | Full linked-member and consumer audit, plus unchanged Win32 relink. Do not define x86 SDK macros in an x64 compiler merely to silence errors. |
| **TCG (deprecated)** | Preserve documented disabled state; remove stale build inputs only with proof | Setup stores configuration; engine loads on launch. Normal HUD launch is commented. Window/pixel callbacks, audio hooks, resize order and remote card/account service remain obligations if reachable. | Verify no active launch path and prove any build cleanup preserves the existing client; no TCG engine/service restoration is required by the current scope. |
| **Capture** | Matching capture SDK/source; original capture host; explicit replacement encoder | Actual references are Debug-only in inspected TUs. Encoder/container, audio feed, frame pacing and allocator interfaces matter. A new encoder is a behavior change. | Original Debug recording of known frames/audio and final link extraction. Preserve original configuration differences. |
| **Logitech LCD** | Matching low-level native SDK; original low-level API host; measured newer official SDK adaptation | New SDK can receive the existing bitmap but omits explicit priority/foreground/device controls. Same pixels are not identical button/app-arbitration behavior. | Original supported hardware: pixels/buttons, competing applets, forced foreground, hotplug and manager restart. Continue software ABI investigation meanwhile. |
| **TrackIR** | Official native provider and minimal filename selection | SDK source indicates a compatible native route; old profile recognition, provider behavior and hardware remain unmeasured. An emulator changes the provider. | Native old/new layout checks, documented architecture-specific DLL selection, then actual profile/cockpit comparison on supported hardware. |
| **libsndfile and transitive voice libraries** | Matching source build where ABI is known; retain original provider in voice host | No direct first-party caller was found; vendor transitive usage still needs actual imports/modules. New codec/version is not automatically equivalent. | Exact Vivox dependency/export closure and runtime version. |
| **SOE platform APIs** | Build genuinely required source; prove stale inputs before removing them | Repository has both source and binaries. Names in a shared link list are not proof the client calls server/service APIs. | Per-library extracted members and real consumer symbols, then service requirements if any. |
| **Deja, ATI compression, Cg/tool SDKs** | Keep tools scoped separately; source-build a real dependency; prove unused game link entries | Modern compression can change asset bytes/quality. Tool libraries and diagnostic examples do not prove game-runtime implementation availability. | Actual client member extraction and caller/configuration census; format-specific output comparisons if used. |
| **DPVS, JPEG, STLport and other source-built components** | Build original implementation for the correct architecture and validate it | Source availability removes the binary architecture barrier, not numerical/ABI/runtime risk. | Existing DPVS and renderer probes, then full client integration and representative scenes. These are not missing proprietary binary SDKs. |

The detailed [Miles dossier](miles-options.md), [secondary vendor dossier](secondary-vendors.md), [LCD route](logitech-native-route.md), and [TrackIR audit](trackir.md) record source sites and primary sources. This is a bounded inventory, not a certificate that every future runtime module has been found.

## All architecture choices considered

The options below are distinct implementation routes; none is a shortcut around acceptance. Historical browser/TCG/voice-restoration options are retained for completeness, not work authorized or required by the present SWG Source baseline.

1. Rebuild the exact licensed original implementation for x64, if its source becomes available.
2. Obtain the matching historical native x64 SDK and all required plugins through an authorized source.
3. Upgrade to the current vendor SDK, measuring version and API changes.
4. Keep original Miles in a 32-bit helper that owns its original output driver.
5. Co-host original Miles and Bink, preserving their direct driver relationship.
6. Put Bink in a separate host and redesign its audio bridge; more clock/sound-provider change than option 5.
7. Put the complete original Vivox wrapper and SDK in a separate host, retaining its existing local service.
8. Put all legacy vendors in one host; fewer process links, but wider crash/lifetime coupling and competing workloads.
9. Use separate vendor hosts; better isolation, more cross-host scheduling and lifecycle work.
10. Use JUCE as a native audio framework and implement the missing SWG/Miles semantics.
11. Build a modern JUCE backend behind a narrow C ABI so v120 need not compile JUCE itself.
12. Use older JUCE compatible with the legacy toolchain; this retains framework maintenance costs without establishing fidelity.
13. Use OpenAL Soft plus an explicit decoder and SWG policy layer.
14. Use miniaudio plus the required environmental DSP and compatibility behavior.
15. Use XAudio2/X3DAudio with separate decoding and effects.
16. Use FMOD or another licensed game-audio engine; broad facilities still introduce different DSP and another vendor dependency.
17. Use SDL audio/mixer plus custom behavior; basic playback/positioning is not the full contract.
18. Reimplement the Miles API/behavior from measured contracts; this is substantially more than matching function names.
19. Use native FFmpeg for Bink decoding plus a faithful player/sound integration.
20. Transcode original media to a different format; this changes the asset pipeline and cannot be presumed acceptable.
21. Migrate voice to modern Vivox, Mumble, WebRTC or another service; server/authentication/UI and codec behavior are part of the change.
22. Keep a 32-bit game/media shell and move selected world/render work to x64; this moves a much larger engine boundary and leaves the game process's memory limits.
23. Emulate or translate x86 vendor code inside an x64 host; Windows API callbacks, vendor plugins, threading and FPU still require an extensive compatibility system. Ordinary DLL loading cannot do this.
24. Preserve the complete Win32 client as the baseline/fallback while x64 work continues; useful operationally but not completion of the x64 goal.
25. Remove features or provide success-returning stubs. **Excluded by the user's requirement.**

“Use JUCE” therefore addresses only some audio plumbing. It does not supply Bink playback, the original Miles algorithms, a Vivox service, TCG, browser behavior, TrackIR or the LCD manager.

## What retaining 32-bit helper processes costs

A 64-bit main client can retain its larger memory address space while a separate 32-bit component retains legacy behavior. This resembles keeping a fixed-width protocol in the sense that compatibility boundaries can stay narrow. It adds a different kind of boundary: scheduling, copying/shared buffers, callbacks and process ownership.

Windows supports cross-process interoperability but does not ordinarily permit an x64 process to load an x86 DLL. Shared memory provides bytes, not portable pointers, C++ objects or callback addresses. Handles must become explicit tokens with lifetimes and generations. [Microsoft interoperability](https://learn.microsoft.com/en-us/windows/win32/winprog64/process-interoperability), [shared memory](https://learn.microsoft.com/en-us/windows/win32/memory/creating-named-shared-memory).

The main costs are added command latency/jitter; preserving synchronous getters and callback reentrancy; avoiding TreeFile request deadlocks; maintaining per-process memory limits; startup/shutdown/recovery; packaging and tracing multiple processes; and platform compatibility testing. Batching or mirroring state can reduce overhead but can also change game decisions. Sending decoded PCM through another mixer adds another possible resampler and clock; direct output from the original host avoids that particular change. No design removes the need to measure the original and the candidate.

A source rebuild or exact native SDK would avoid IPC, but can still change floating-point paths and behavior across versions. RAD's history records x64 Miles support as early as 7.0j and later mixer/decoder changes. That disproves “Miles cannot be x64”; it does not supply the needed licensed artifacts here. [Miles history](https://www.radgametools.com/msshist.htm).

## Acceptance gates before a vendor decision

1. **Identity and reachability:** exact source/runtime/plugin versions; real compiled callers, extracted libraries and dynamically loaded modules.
2. **Original baseline:** same assets, configuration, device and service. Record original variability without treating it as automatic permission for regressions.
3. **Small discriminating experiment:** actual implementation and real inputs; immutable oracle; exact output/event differences retained. No mock provider counted as a vendor pass.
4. **Lifecycle and integration:** valid ownership, callbacks, stop/restart, device loss, loading, scene transition, exit, under load.
5. **Full-client acceptance:** native x64 startup, representative ground/space behavior, mixed-width server connection, original hardware features and working services. Every known difference must be resolved or explicitly presented for a decision.

Finite tests cannot prove universal equivalence. That limitation does not reduce the requested fidelity: it means we must keep untested behavior and measured differences visible, avoid declaring success early, and retain the original client as the reference. No perceptual tolerance, latency allowance or feature deletion has been accepted on the user's behalf.

## Current implementation checkpoint

The native integration snapshot including statistics, Audio callback and renderer candidates builds **Win32 Release with zero errors**. Its x64 Release attempt has **24 compiler errors from the single Mozilla SDK architecture root**; the client link has not yet been reached. Debug configurations and the bounded unused-project investigation continue. The allocator minimum-block repair passes **1,622/1,622** checks per ABI/configuration, and Audio callbacks pass **18/18 Release, 20/20 Debug** with that repair. These do not constitute a complete x64 client.

The persistent goal is the finished, polished x64 client. Research, builds, source fixes and evidence publication continue in parallel; no upstream PR or backend replacement is being made by this decision packet.

The user has designated SWG-Source/client-tools `x64` as the eventual upstream target. Development and evidence remain on the fork. No upstream PR may be created until the client is finished and the user separately approves it.
