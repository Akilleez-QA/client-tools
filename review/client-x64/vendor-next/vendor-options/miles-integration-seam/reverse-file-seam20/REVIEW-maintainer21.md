# Blind maintainer review 21

2026-09-30. Reviewed independently from raw candidate and unchanged product source; no other reviews or parent conclusions were read. Product HEAD observed: `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`.

**Engineering: 8.5/10. Standalone PR readiness: 7/10 (reviewable experimental seam; not yet demonstrated build-ready).** No concrete introduced behavioral or integration defect was established. I would request the actual Windows translation-unit compile evidence before merge. I would not require a reverse-RPC dispatcher, TLS redesign, transport, or device/runtime tests merely to accept this dormant seam as its own explicitly scoped change.

## Purpose and integration

The purpose is precise: make four file-local functions callable through a client-local C++ interface, without copying the filesystem implementation, changing SDK registration, or changing file ownership. Patch lines 31–55 are four one-call wrappers. Keeping definitions in Audio.cpp is justified by the callbacks' static declarations at original Audio.cpp:234–237. The existing registration at 1293 remains untouched. Namespace external linkage provides the intended call surface; changing the original callbacks' linkage would be a wider alternative.

The current integration story is credible. `clientAudio/build/win32/clientAudio.vcxproj:31–56` declares StaticLibrary configurations and v120 toolset; line 279 already compiles Audio.cpp. Therefore this patch needs no added compilation unit and no DLL export decoration. Public-header `ClInclude` registration would aid IDE discoverability but is not required for compilation. Patch:115–121 matches the existing `include/public/clientAudio/Audio.h` forwarding convention. The seemingly short `../../src/win32/...` include relies on the existing include search directories, including the library's `include/public` at project:106 (and subsequent configurations); it is not evidence of a broken include simply because resolving relative to the forwarding header's own directory alone fails. Original Audio.cpp:38–40 already supplies stdint and limits. No missing `<limits>` defect exists.

Actual v120/PCH/STLport compilation remains unobserved. The project includes STLport 4.5.3, so modern standalone g++/MinGW success is not a substitute. The added assertions are reasonable, but their evaluation against real Miles macros and the configured standard library is the next useful check. Ordinary consumer calls also need the same compatible build ABI and linkage to clientAudio; the API is not a stable cross-compiler or cross-process ABI.

## Callback semantics

- **Handle zero:** original Audio.cpp:123 starts the key at zero; 3948–3965 returns success separately from the key and writes zero on failed open. Header:17–20 and patch:31–37 preserve this distinction. The typed wrapper's lack of implicit bool/pointer conversions is helpful. Its public integer member still requires disciplined callers; it is not an unforgeable capability and does not solve stale handles or native counter wrap. Those are not falsely claimed.
- **Open result and ownership:** one original open, separate status and key, no extra file allocation or secondary map. Initializing the temporary native key to zero does not change the observed failure semantics. Closing dispatches to the original owner at Audio.cpp:3968–4004, where close/delete/erase occur. No ownership is transferred by returning the small wrapper value.
- **Calling convention:** SDK typedefs at Mss.h:5222–5242 and original `__stdcall` declarations remain authoritative. These are normal C++ calls into functions compiled with their declared calling convention, not function-pointer casts. The new struct-returning open deliberately cannot stand in for the Miles open function pointer. That is correct for this purpose.
- **Seek:** original Audio.cpp:4007–4059 accepts signed offset, ignores AbstractFile's bool seek result, returns signed tell(), and has a fatal invalid-origin branch only after finding a live key. Patch:45–48 preserves this. Do not normalize a negative tell result to zero or substitute the ignored bool. The enum is documentation/convenience while the function accepts uint32_t; admission still must reject unsupported origins.
- **Read:** original Audio.cpp:4063–4098 takes U32 count, passes it to `AbstractFile::read(void *, int)`, then casts its signed result to U32. Patch:51–54 preserves those bits. A negative read result becomes a large unsigned number; the seam correctly does not fabricate EOF. It equally does not make such a result safe for copying. README:97–114 correctly locates request-range checks, staging bounds and transport failure outside this direct adapter. Requests above INT_MAX are not a safe admitted domain merely because the signature is U32. This is an inherited domain issue, not a new narrowing conversion introduced by the wrapper.

The type-width assertions support this local mapping without aliasing a uintptr_t pointer as UINTa*. They are not a proof of every possible C++ implementation, nor need they be: the declared target is the concrete Windows project.

## Lifetime, threads, and the strongest rival

The strongest challenge is that publishing another entry point makes an unsafe multi-thread use easy. That is a credible future integration risk, but no consumer exists in this patch and the header explicitly requires compatible thread context, lifetime, serialization with all original callbacks, and pins (header:30–38). Counting absence of the future scheduler as an introduced defect would change the requested scope.

The source substantiates the warnings. Audio.cpp:3936 introduces a process-wide `once`; each callback checks it, and the first nonmain path installs TLS. `PerThreadData.cpp:189–227` allocates new Data/Gate and overwrites the TLS slot; false bypasses the existing-slot assertion, so preinstallation is not an idempotent solution. FileStreamer.cpp:208–242 uses the caller's gate and waits. The callbacks' map/counter and file positions have no enclosing serialization. A mutex used only by the four new wrappers would not cover the still-registered original callback addresses. Audio.cpp:1421–1437 clears installed state before Miles shutdown; an isInstalled-only admission rule could reject legitimate shutdown work. README:116–163 acknowledges these issues accurately.

These are gates before adding callers: establish an actual execution route for causal and unsolicited callbacks; coordinate every original entry path; pin operations and buffers; order close and engine/TLS teardown; and reconcile disconnect ownership. None is implemented or tested here. They do not independently block a dormant source seam when its PR explicitly has that limited purpose. A maintainer who does not accept unused public API can defer the seam until its first consumer; that is a scope/maintenance decision, not evidence the wrappers malfunction.

## Verification and requirements

I independently ran the three COMPILE-PLAN syntax-only commands (native g++, i686 MinGW, x86_64 MinGW); all exited zero without diagnostics. I also ran `git apply --check` against the pinned checkout, checked the original Audio.cpp diff remained empty, and confirmed HEAD. No patch was applied. No engine/vendor executable, allocator workload, fault test, or runtime callback was run.

These observations establish applicability and standalone declaration/type-probe syntax only. `compile_types.cpp:33–36` demonstrates a constant success-with-zero representation, not an actual open. It contains no wrapper definitions. No instrumented-double test or actual engine call is claimed. Repeating the supplied probe independently is repeat observation of the same narrow test, not independent behavioral corroboration.

Concrete requirements before calling this standalone PR merge-ready:

1. Compile the patched Audio.cpp in an authorized disposable checkout with the actual supported Windows project configurations/toolchain, including Win32 and x64 as claimed. Capture compiler/configuration identity and output. This tests the actual forwarding include, STLport numeric_limits, SDK scalar macros and wrapper definitions. The existing standalone test cannot satisfy it.
2. Keep the PR title/body explicitly about exposing existing callbacks through a dormant client-local interface. Include the no-consumer/no-scheduling limitation and the successful type checks plus missing actual-TU compile. Do not claim a completed reverse-file bridge or validated file I/O.
3. Preserve the header preconditions and unresolved coordinator requirements when the artifact is moved into the PR. No invented SDK error mapping, adapter-only concurrency guarantee, registry cast of zero, or duplicated filesystem implementation should be introduced to make this look more complete.

Optional: list the header in the IDE project and later verify a consumer link when the first consumer exists. Neither is an established current defect. A mocked wrapper test could check one-call forwarding but would still not test actual TreeFile behavior and should not be presented as doing so.

## POODO record and decision boundary

Entry exchange waived because the assignment specifies artifacts, purpose, output, and prohibited runtime/source actions precisely. Linguistic frame: “integration defect” means an introduced failure in this proposed source integration, not missing future functionality; “PR readiness” means a reviewable and compilable dormant API change, not production bridge readiness. Authority permits read-only inspection and safe static probes plus this report only. Fan-out considered at each transition and not used: this is already the primary's blind review spike, no descendant capacity was allocated, and an extra reviewer of the same tiny source surface would not add a distinct evidence family.

Observed topology: declaration/definition/include/build chain; SDK-to-local scalar and calling-convention boundary; map ownership and handle zero; signed seek and unsigned read conversion; TLS/serialization; shutdown; current probe versus actual compiler versus runtime. All were inspected or explicitly left beyond authority. The strongest rival is “the seam is unusable without a complete scheduler”; the discriminator is its explicitly dormant API scope versus any actual new invocation path. The patch adds none.

Research gate completed before synthesis on 2026-09-30. Queries: “site.learn.microsoft.com C++ static library header include lib linker” and “site.learn.microsoft.com C++ thread local storage threads dynamic TLS”; inspected Microsoft static-library and Win32 TLS documentation, plus the C++ draft integral-conversion section as an independent language-specification family. [Static-library walkthrough](https://learn.microsoft.com/en-us/cpp/build/walkthrough-creating-and-using-a-static-library-cpp?view=msvc-170) supports the distinction between headers, objects, libraries and consumer linkage. [Win32 TLS](https://learn.microsoft.com/en-us/windows/win32/procthread/thread-local-storage) explains per-thread storage even with a global index. [Integral conversions](https://eel.is/c++draft/conv.integral) supplies the modulo-result context for unsigned conversion. Microsoft static-library search metadata reports publication about 2.5 years ago; TLS about 1.2 years ago; exact update dates and the live draft revision were not established. These are conceptual sources, not exact-version v120 build evidence. No conflict overrides the local source; in particular current signed-conversion rules cannot certify old-compiler out-of-range U32-to-int behavior. The disconfirming TLS inquiry rules out treating one global initialization flag as per-thread installation.

Twenty paths considered before selecting requirements (distinct mechanism or evidence gain):
1. Accept the dormant seam after actual-TU compilation.
2. Defer the seam until a concrete first consumer justifies public API.
3. Reject the new API and retain the untouched SDK-only surface.
4. Expose original callback symbols directly instead of wrappers (wider SDK coupling).
5. Extract original callback bodies into a separately compiled component (larger linkage/state refactor).
6. Introduce an injected callback façade for consumer dependency control (larger abstraction).
7. Build the touched TU with real Windows configurations (actual compiler discriminator).
8. Compile a public-header consumer using real project include settings (include-boundary discriminator).
9. Inspect compiled object symbols or consumer linkage without execution (linkage discriminator).
10. Use isolated fake callback definitions to test scalar forwarding (narrow behavioral proxy).
11. Audit actual call sites when a consumer is proposed (admission discriminator).
12. Design a waiting-client callback route (causal progress mechanism).
13. Design a dedicated owned service thread with explicit TLS changes (alternative scheduling mechanism).
14. Redesign synchronization across original and new callback paths (shared concurrency boundary).
15. Add generation-aware binding records (wire identity ownership mechanism).
16. Reserve file-binding capacity before open (publication-failure containment).
17. Define a bounded read domain and staged transfer (buffer/transport contract).
18. Define exceptional raw-read result protocol behavior (compatibility mechanism).
19. Specify shutdown/disconnect reconciliation (lifetime recovery mechanism).
20. Escalate actual Windows build and thread-affinity contracts to their owning maintainers (authority/evidence gap).

Selected 1 conditioned on 7, with 2 a legitimate maintenance alternative and 8/9 useful at first consumer integration. Paths 4–6 are unnecessarily broad for the stated seam; 10 is optional and proxy-limited; 11–19 belong to a future admitted consumer and are not authorized implementation work here. Path 20 resolves unavailable actual-build evidence. Bounded saturation is limited to the small patch and its immediate source/build boundaries, not whole-engine correctness. Reopen if the actual compiler rejects it, any consumer appears, supported ABI changes, or lifetime assumptions are relaxed.

Artifact identity: patch SHA-256 `61dc2fff8978e379bb11011b5b9db67bb7c8fc8138215dc133f09657d9d74b99`; standalone header SHA-256 `d116186a05fc44cc4809231ff114aa526514edb6155e40e70edd6a147769a9b0`.

`delivery_state`: reviewed; standalone probes checked; report authored.
`outcome_state`: passed for patch applicability and standalone type syntax; actual engine compilation/runtime unobserved.
`highest_justified_claim`: a minimal, source-consistent candidate exposing original callbacks; no demonstrated introduced defect within this inspection scope.
`required_runtime_observation`: none required to establish this dormant source seam's purpose; actual callback-route/lifetime/progress observations are required before a future bridge can claim working I/O.
`who_controls_next_test`: user/Windows build owner controls the separately authorized actual-TU compile; future integration owner controls runtime admission tests.
