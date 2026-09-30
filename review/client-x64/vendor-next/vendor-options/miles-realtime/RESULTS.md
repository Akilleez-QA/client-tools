# Original Miles clocked capture and one-command transport

2026-09-30. Private diagnostic only; no backend selection, production edits, device installation or public media. Sources/commands and prospective decisions in PLAN.md; raw audio remains private.

## Capture route established

Host Wine11.17 → process-local ALSA pulse PCM explicitly naming a unique temporary null sink → PipeWire1.6.8 → that sink's monitor. Winepulse disabled; no physical ALSA definition/fallback. Capture is signed16 stereo22050Hz; observed producer is float32 stereo48000Hz, so this is a resampling/mixing graph, not a native Miles output-byte tap. Input volume observed100%, unmuted. No host defaults or existing volumes were changed. Every created module was unloaded and final sink inventory contains no experiment sinks.

First run had near-real-time EOS but captured silence with default parec buffering. Preserved as failed evidence. Explicit20ms capture latency and10ms processing then captured nonzero bytes with clock progression near88200bytes/s. Three repeats of unchanged original probe returned3.70/3.78/3.82s PCM over3.733/3.803/3.864s wall. Exact original runtime/assets held fixed; output was **not byte-identical** after bounded integer alignment. Immediate release after EOS made this initial probe unsuitable for a complete output comparison.

## Drain-preserving reference

Separate native x86 probe: one sample or one stream per process, fixed500ms post-EOS handle retention with real AIL_serve every5ms, then release. Three runs each. No reverb or extra simultaneous sound. Original asset contains4488 mono22050Hz frames (203.54ms). Each capture's full4488-frame aligned window correlates0.999827–0.999994 with source; this identifies the clip and captures its window, not sample equality. Raw captures preserved. Only integer frame offset and fixed frame-window trimming used; no gain normalization/resampling/noise removal in analysis.

Repeated sample output differs in5444/5908 of8976 channel values, max absolute33/103, RMS6.67/19.34. Repeated stream output differs5960/5820 values, max112/77, RMS19.35/13.17. Baseline variation is not permission or an accepted tolerance. Resampling phase/timing remain uncontrolled; their exact contribution has not been isolated.

## Real x64 controller → x86 original host

Native v120 PE controller machine8664 creates a native host machine14c, sends exactly `sample` or `stream` over an inherited stdin pipe, closes it, waits at most10s, and propagates child status. Identical host binary runs directly with a mode argument for control. The actual original7.2a DLL performs every audio operation; no API replacement or provider stub. Exact binary/asset hashes in command-analysis.json.

| Mode | Direct / controlled result | Capture PCM / wall seconds (direct; controlled) | Differing channel values after alignment | Max / RMS |
|---|---|---|---:|---|
| Sample | 0 / 0 |3.94/3.956;3.94/3.971|5266/8976|35 /6.67|
| Stream |0 /0|4.16/4.186;4.10/4.128|5960/8976|112 /19.35|

Correlation with original asset stays0.999827–0.999994. There is no byte-equality result or accepted fidelity verdict. Similarity to baseline variance is an observation only.

## Callback and floating-point correction

All four one-command runs below delivered EOS on a separate Miles thread. The retained-handle direct repeats include both main-thread and foreign-thread callbacks; this route does not have one universal callback thread. Direct sample: main304/EOS328; controlled sample360/408. Direct stream440/488; controlled stream524/572. Sample EOS139/138ms; stream268/269ms. EOS is not the device-drain timestamp. Callback x87 word027f/MXCSR1f80; main after offline decode has MXCSR1fa0. These are probe/backend observations, not a universal Miles threading rule. SWG's actual PC64 render/collision FPU state has not been replayed here.

## Evidence ceiling

This proves the original32-bit runtime can emit clocked audio privately and accept a one-command request from an actual64-bit process. It does **not** implement a game audio helper: no synchronous getter protocol, handle map, PCM transport, callback RPC, file callbacks, streaming seeks, cancellation, restart, reentrancy, multi-sample mixing or gameplay integration. No reverb testing yet. No physical endpoint latency/nativeWindows equivalence or full original-experience claim. Files remain local/private; no commits or uploads.
