# Exact original Miles native baseline

Date2026-09-30. Native v120 Win32 executable in disposable C:/vendor-miles-probe. No client backend edits and no audio device installed. Input assets and decoded outputs are private diagnostic files and must not be added to the public repository.

The actual client-root Mss32.dll loads and its resource string is7.2a. All61 used exported AIL functions appear in its export table. The62nd lexical name, AIL_MSS_version, is a Windows SDK macro that loads resource string1; it is not an absent export. export-coverage.json records the DLL hash and decorated names; plugin-manifest.json records original siblingASI/FLT/M3D file hashes. Source and runtime both identify7.2a here.

AIL_startup returns1. Before and after startup the native process has x87control027f and MXCSR1f80. The VM reports waveOutGetNumDevs=0. The original AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0) returnsnull with waveOutOpen()failed. Exit6 means BLOCKED, never a playback pass. No HSAMPLE/HSTREAM/EOS test runs without a real output driver.

An offline decoder path works without that endpoint: actual AIL_decompress_ASI + original mssmp3.asi decode music/mus_player_v_npc_c_vict.mp3 (38,998 bytes) into a428,588-byte WAV. decode-okay=1. x87control stays027f; MXCSR becomes1fa0, adding inexact status. The loaded-module trace records all original ASI/FLT plugins loaded during startup/decoder activity; it does not establish that every provider is used for this asset.

The source uses typed pointers derived directly from the actual7.2a SDK declarations and resolves exactstdcall exports. It does not call substitute functions. The original PCM sample cr_sm_fs_carpet_04.wav is extracted with its source TRE offset/length/hash, but playback remains blocked. The MP3 call is an offline oracle, not proof that SWG's streaming path emits identical output or callback timing.

No postmix capture ABI was invented. The SDK has filter/provider interfaces and the client contains disabled capture code, but their safe configured capture contract is not established by this probe. An audio-capable VM/machine is needed for the planned sample/stream/EOS/service trace. A replacement can now be compared to the exact decoded WAV privately; similarity would not prove mixer/reverb/latency equivalence.

## Open-decoder discrimination

The same real MP3 was decoded privately using host FFmpeg (version saved) and the downloaded miniaudio source (exact inputs/output hashes in decoder-comparison.json). All three return107,136 stereo44,100-Hz16-bit frames. An exhaustive integer-frame alignment search within ±4096 frames found offset0 for each candidate.

Against the original Miles decoded PCM, FFmpeg differs in23,736 of214,272 channel samples; miniaudio differs in23,778. Both have maximum absolute difference502 and RMS about8.98 in signed16-bit units. Length/alignment match does not imply decoded-sample equality. These are numerical observations for one asset, not an audibility verdict or accepted tolerance. No replacement selected. Reproduce with miniaudio-decode.c, ffmpeg command `ffmpeg -i sample.mp3 -c:a pcm_s16le decoded-ffmpeg.wav`, and compare-decoders.py. Original/decoded audio remains private.

## Private Wine null-output seam probe

A separate private Wine prefix uses an explicit ALSA `type null` PCM through a process-local ALSA_CONFIG_PATH and private Wine Audio=alsa registry setting; winepulse is disabled. No host default device, service or registry changed. The sink discards output and cannot establish audible fidelity or real-device latency.

The same native Win32 probe/original DLL creates a 22,050-Hz/16-bit/stereo driver. The real 204-ms PCM asset is accepted; cached sample and stream both reach DONE, each delivering exactly one EOS callback, followed by orderly close/shutdown. In this particular probe callbacks occur on its main thread while explicit AIL_serve calls are made. That does not establish the callback threading contract in the real client or under all asynchronous paths.

Null output consumes buffers faster than real time: the sample reaches EOS about32 ms after start and the stream about112 ms. These numbers are evidence that this environment is unsuitable for timing acceptance, not a performance improvement. `wine-null-run.log`, `wine-version.txt`, `alsa-null.conf` and the source document the environment. The original MP3 decoded under Wine has exactly the same WAV SHA256 as native Windows,44ae67cc466456dd53f128339fff013e1337db90a316fe99a228a41bc9fae749, for this one input.

This establishes that the original decoder/driver/sample/stream API can be exercised in a disposable process without a host audible endpoint. It does not implement an x64↔x86 helper protocol, test its blocking/file callback interactions, validate reverb or measure audible/live gameplay behavior.

## Later clocked-route evidence

The separate `../miles-realtime/RESULTS.md` establishes nonzero real-time capture through a private explicit Pulse/PipeWire sink and a bounded actual x64-controller/x86-host command experiment. It does not retroactively change the ALSA type-null results above. In the clocked route EOS arrives on another thread, so the null probe's main-thread callback observation must not be generalized. PCM varies even across unchanged direct runs; no equivalence tolerance or backend choice follows.
