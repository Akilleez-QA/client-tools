# Independent review reconciliation

2026-09-30. Agents share source and evidence, so their agreement is not counted as independent runtime proof. The parent checks source sites, native compilation and raw outputs before promoting a finding.

| Lead | Resolution |
| --- | --- |
| Composer: TrackIR was missing from the vendor inventory | Confirmed. Real startup/cockpit path; official x64 provider filename differs. Narrow candidate passes actual native TU and layout checks. Hardware remains untested. |
| Composer: DPVS is binary-only | Rejected. Source and prior all-four-configuration builds exist. |
| Composer: `#if DEBUG=0` is an equality test | Rejected. Actual native preprocessing excludes browser bodies and emits C4067; source history explicitly intended disablement. |
| Grok: free-list node footprint exceeds permitted x64 remainder | Confirmed by native layout. Parent also found allocated tiny blocks need the same minimum, not only split remainders. Candidate passes 1,622 checks in all four configurations. |
| Grok: retaining original DLL automatically favors a helper | Qualified. Original code retains codec/DSP implementation, but scheduling, file callbacks, state queries and device/clock coupling remain unproven. No helper selected. |
| Broad vendor inventory implied every legacy component needs restoration | Corrected after the user directed us to SWG Source documentation. Browser/TCG are documented deprecated features; normal voice controls are disabled. Read BASELINE.md before the option tables. |
| Lack of a visible modern LCD link implied no native provider | Rejected after deeper official-package research. A signed legacy Logitech package contains the correct low-level x64 API. Original header/library link and layout probes pass. |
| MP3 support implies equivalent samples | Rejected by actual one-asset comparison: original Miles differs from FFmpeg/miniaudio despite identical frame counts/alignment. No audibility conclusion assigned. |
| Bink decode/transport implies complete video replacement | Rejected. Public sample codec/IPC probe works, but differs from FFmpeg and has no audio; game assets/presentation/sync remain untested. |

Composer remains useful for broad discovery; its unverified implementation classifications are not acceptance evidence. Grok's arithmetic and architecture critiques supplied useful leads but required corrections and narrower claims. CLI Codex's Bink experiment produced actual runtime evidence and also documented its own initial FFmpeg input-bound mistake. Native agent results likewise retain failed controls and configuration limitations. No model earns blanket trust from these observations.

## Review round4 (source reviews, 2026-09-30)

Composer found the second TrackIR loader in SwgClientSetup. Parent checked that this executable remains Win32; `NPClient.dll` is correct there even when the game is x64. This is a future setup-port dependency, not a current game bug. Its claim that no Audio native ABI tests exist was based on tools/ only; the separate actual TU and callback evidence is in audio-next. Physical provider acceptance is still open.

Grok correctly identified the dependency builder adopting a nonempty output directory when owner.json is absent. Isolated repair/review is underway; existing manifest/library hashing does not establish directory ownership. The nonexistent `_STLP_DONT_FORCE_MSVC_LIB_NAME` macro claim is withdrawn: this bundled STLport has no corresponding auto-link directive, and explicit link input/path selection is what matters. The WinMain1536MB value is a soft budget, not proof of a hard process-address ceiling; downstream cache effects are under review. First Miles successful handle0 equals failed output0, but the callback also returns success separately; this is a contract question, not yet a demonstrated bug.

TrackIR compatibility wording is narrowed to SDK/layout/compile evidence. No actual provider, device or profile6001 acceptance has occurred. The old LCD wrapper now links with genuine official legacy x64 SDK, which must not be confused with the newer high-level SDK missing foreground/priority APIs.

## Rounds 5–7 and current followups

- Dependency-output ownership is now committed in `10e684ba7`: 12 tests pass on host and native Windows; missing/malformed ownership does not adopt existing outputs. The unused STLport macro still needs cleanup; it never supplied the claimed auto-link behavior.
- Grok's handle-zero concern is a missing contract test, not a demonstrated Miles failure. The callback success result and output handle are distinct. A new original-DLL file-callback probe is being prepared. Its one-time TLS latch and unsynchronized handle map are source risks with callback-thread/concurrency conditions still to establish.
- Grok's later claim that the LCD wrapper had only compiled relied on older `lcd-legacy-v2` and API-only records. Parent checked `lcd-integration/results-v4.json`: all four complete wrapper links return0 with real allocator/core symbols, and `executed:false` is explicit. Hardware acceptance remains open.
- The clocked Miles route supersedes no raw logs: it adds an observation of worker-thread EOS and nonidentical captured audio between original repeats. Earlier null-output main-thread EOS is limited to that route.
- Composer corrected its claimed memory-budget discontinuity: 2047*0.75 truncates to1535, followed by1536 at2048. No downward step exists. Parent/native-warning reviewer independently confirmed the crash-pointer formatting defect, and distinguished bounded packet differences from arbitrary pointer-address truncation.
- Native warning review reports808 unique compiler locations, not808 defects. AutoArray/AutoList count writes and crash formatting have narrow candidate work underway; UI allocation-cache keys require a separate bounded analysis. A compiler failing to emit pointer-truncation warnings cannot establish their absence.
