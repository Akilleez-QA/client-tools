from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;root=p.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
asset=json.loads((p/'asset.json').read_text());v=json.loads((p/'verification.json').read_text());c=json.loads((p/'comparison.json').read_text())
receipt=json.loads((p/'logs/final-vm-receipt.json').read_text())
for h in receipt['source_hashes']:assert sha((p/h['file']).read_bytes())==h['sha256']
assert not receipt['remaining_probe_processes']
assert c['oracle_sha256']=='26367917f1c10ac71f4794846446c0270057c92cffc79a82a73ac474c54d4988'
assert all(not f['exact_equal'] and f['old_pixels_above_16']>0 for f in c['frames'])
historical=json.loads((root/'source-hashes.json').read_text());checks={}
for name,expected in historical.items():
 file=Path(name)
 if file.is_file():checks[name]=dict(expected=expected,current=sha(file.read_bytes()))
assert all(x['expected']==x['current'] for x in checks.values())
(p/'historical-source-check.json').write_text(json.dumps(checks,indent=2))
(root/'report.md').exists()
history=p/'historical-report.md'
if not history.exists():history.write_bytes((root/'report.md').read_bytes())
result=dict(status='public_non_swg_decode_and_pixel_transport_verified_oracle_mismatch',asset=asset,runtime=v['identities'][2],build=v['identities'][:2],transport=dict(runs=2,payload_bytes=4917065,fnv1a64='d98d4def671705d1',sha256=v['runs'][0]['payload_sha256'],verified_on_vm_and_linux=True),decoded_frames_per_original_process=32,retained_frame_numbers=[1,8,16,32],all_selected_nonblack=True,ffmpeg_exact_matches=0,ffmpeg_selected_frames=4,ffmpeg_bounded_followup_identical=True,audio=dict(tracks=0,extraction_exercised=False,playback=False),swg_asset_acceptance=False,game_fidelity_proven=False,production_edits=False,commits=False,limits_deviation='Initial verbatim FFmpeg command limits 32 output frames after selecting 4, so does not enforce 32 input decodes; may decode all 150 sample frames. Follow-up limits 4 selected outputs with identical bytes. Original DLL always bounded to 32.',vm_directory_bytes=receipt['probe_directory_bytes'])
(p/'results.json').write_text(json.dumps(result,indent=2))
report='''# Disposable Bink feasibility result

**The actual original Bink 1.9c PE32 DLL decoded this public non-SWG sample, and a v120 x64 driver transported four nonblack decoded frames through a pipe with verified framing/checksums. All four frames mismatch installed FFmpeg under the predeclared oracle. This proves bounded codec/IPC feasibility only; it does not prove SWG asset compatibility, integrated playback, or game fidelity.**

## Public sample experiment — 2026-09-30

Source: [FFmpeg's logo_legal.bik](https://samples.ffmpeg.org/game-formats/bink/logo_legal.bik), 395,724 bytes, SHA-256 `10c375fd8c6e2fa11db83daaabdabc94a6f9b9b77dcce52720d71b8aa2da7145`. Header/container version `BIKi`, 640×480, 150 frames, 30/1 fps, five seconds, flags 0, zero audio tracks. The original header's declared size agrees with the download. FFprobe independently agrees on dimensions, rate, version and absence of audio. This is a public decoder test asset, **not an SWG movie**. No fallback sample was needed. URL, HTTP headers, hash, container metadata and installed FFmpeg n9.0.1 build are retained in `public-sample/`.

Runtime remains the installed original `binkw32.dll`, PE32/i386, version 1.9c (header dated 2008-01-15), SHA-256 `e67e0319f9929c024a6d0757de50c65257f686f6711cb0efb7ad53afc3405dd4`. The DLL was loaded by absolute path; actual decorated exports resolved, including track functions. No replacement DLL or installation was downloaded. New binaries are v120 /MT x86 (`0x14c`) and x64 (`0x8664`); executable hashes and runtime/sample identities are in `public-sample/verification.json`.

Each of two original-runtime processes sequentially decoded frames 1–32. All reported decode/copy statuses and read errors were zero. Frames 1, 8, 16 and 32 were copied as BINKSURFACE32A | BINKCOPYALL, positive width×4 pitch, top-down BGRA, initially zeroed buffers. Each retained frame is 1,228,800 bytes. No color, alpha, pitch, orientation or frame selection was changed after results.

The x86 child emitted JSON record headers plus length-delimited binary pixels over stdout; the x64 driver captured actual pixel bytes, not filenames or metadata alone. Both complete payloads were 4,917,065 bytes, FNV-1a-64 `d98d4def671705d1`, SHA-256 `d32e4156186403d35530f8abf9eb72b8c4cd908e66153f9646564a51f025b147`, with child exit 0 and x64 pointer size 8. Independent Python verification on Windows and Linux checked outer length/checksum, nested frame lengths/separators, exact frame sequence, x86 pointer size 4, metadata, read errors, and extracted bytes. Both runs were byte-identical. Recorded verification wall times (~0.98 and ~0.75 seconds) include transport and Python verification and are not real-time playback benchmarks.

## Fixed-oracle comparison

Installed FFmpeg used the oracle's explicit BT.601 limited-range to full-range, bilinear BGRA conversion, alpha included. No settings were tuned to obtain equality. Every original/reference byte remains private, and complete signed old-minus-FFmpeg BGRA differences are retained as zlib-compressed int16 little-endian arrays. `public-sample/comparison.json` holds frame SHA-256 values, per-channel error histograms, maximum/mean errors and difference-file hashes.

| Frame (1-based) | Original pixels with any RGB >16 | RGB-mismatching pixels / 307,200 | Alpha-mismatching pixels | Exact BGRA match |
|---|---:|---:|---:|---|
| 1 | 27,387 | 305,500 | 307,200 | No |
| 8 | 27,314 | 306,768 | 307,200 | No |
| 16 | 27,314 | 306,768 | 307,200 | No |
| 32 | 27,314 | 306,768 | 307,200 | No |

Maximum absolute differences are B=2, G=5, R=3, A=255 for every selected frame. Original alpha is uniformly 0; FFmpeg alpha is uniformly 255. The file has no alpha flag; the zero-initialized destination's observed alpha must not be promoted into a general alpha-format conclusion. RGB mismatches also remain after separating alpha. The large mismatch pixel count includes small near-black differences; the >16 counts establish substantive nonblack frame content independently of that effect. Frames 8/16/32 repeat within each decoder; this static sample does not test meaningful motion fidelity. Original conversion is opaque; the cause of the differences is not conclusively established.

**Command-bound limitation:** the verbatim predeclared FFmpeg command has `-frames:v 32` after a filter retaining only four frames, so it does not enforce at most 32 input decodes and may decode all 150 frames of this five-second sample. That initial command, output and log remain preserved. A follow-up changes only the output count to four, stopping at the fourth selected frame (32); its output is byte-identical (combined SHA-256 `75e4bd07d37affc2579d33f7cd6168b11681393639c21675a7cd0938dd40d7d9`). Internal FFmpeg input decode counts were not instrumented. Original DLL processes each strictly stop at frame 32. This is a disclosed bound defect in the original reference command, not a color/alpha retune or a discarded mismatch.

## Audio, bounds and retained evidence

There are zero tracks in both runtime and container metadata, so BinkOpenTrack/GetTrackData extraction is not applicable and was not executed. Export resolution alone does not establish correct track-call sequencing, PCM equivalence or A/V synchronization. The new sample probe rejects an unexpected nonzero track count; the historical unexecuted track branch remains historical, not validated. No sound provider was initialized, no audio was played, and no device settings were changed. A future audio-bearing test must establish the original API's extraction sequence before decoding and retain per-frame PCM under the MaxSize ≤4 MiB bound.

Download was capped at 1 MiB/60 seconds; input is below the oracle's 64 MiB maximum. Dimensions are below 1920×1080. The original child has a 60-second driver watchdog and 40 MiB pipe bound; each build invocation has a 120-second timeout. Four selected frame numbers are retained, with duplicate transports for repeatability and private reference/difference files. Per-host probe data are below 256 MiB. The final VM receipt reports 16,022,820 bytes for the whole authorized VM probe directory and no remaining probe/driver process. Local byte totals and every artifact hash are in `public-sample/artifact-manifest.json`.

All writes were confined to this scratch directory and `C:/vendor-bink-probe`. The existing VM SSH helper, compiler and Python were used. No global Q: mapping, installation, game launch, production edit, commit, push or public media publication occurred. Local sample, decoded bytes, raw IPC captures and differences are under mode-700 `private/public-sample/`; VM copies are local probe artifacts. Do not publish media, pixel captures, difference arrays, proprietary SDK headers or the DLL.

Reproduction commands: `public-sample/download.sh`, `prepare.py`, `run-vm.sh`, `run-ffmpeg.sh`, `run-ffmpeg-bounded.sh`, `compare.py`, `final-receipt.sh`, `finalize.py`, in that order (commands assume a fresh output directory; FFmpeg does not overwrite existing evidence). `public-sample/logs/` preserves build, download, decode, comparison and final receipts; `verification.json`, `comparison.json`, `results.json` and the manifest provide structured results. `historical-source-check.json` verifies every still-present source listed by the previous manifest remained byte-identical, including the oracle and historical probe/driver.

## Historical metadata-only result

The previous report is preserved verbatim in `public-sample/historical-report.md`. Root `results.json`, `asset.json`, `source-hashes.json`, `seam-verification.json`, `commands.sh`, original sources and root `logs/` remain historical and unchanged. Their 116-byte metadata payload, FNV `478950ba1e591338`, SHA-256 `fa2b4ae80efc784bbe343f9c0104c707ba5755b7d2ffaae4330a52cd6073d32a`, proves only metadata transport. It is not the decoded-pixel result above.

The prior search found no supplied SWG BIK: 209 top-level TREs inspected, 72 supported archives without a `.bik`, 137 unsupported version-0006 zero-entry archives rejected, 5,373,439 metadata bytes read, no loose `.bik`/`.bk2`/`.smk`. That search was not repeated or expanded. No unsupported sample-format failure occurred for this BIKi file; compatibility with other revisions remains untested.

## Still needed for actual game playback and fidelity

- Authentic SWG movie assets with installation provenance, all used Bink revisions, alpha/no-alpha and audio/language/multitrack coverage. Compare to the original game's rendering and output; neither a public sample nor a matching hash on it substitutes for acceptance assets.
- A production integration design for x64 hosting: worker lifetime, bounded streaming/backpressure, cancellation/crash recovery, format negotiation, seeking, looping, skipping, shutdown, resource ownership and measured throughput/latency. This whole-payload console experiment is not a streaming player.
- Correct original audio extraction API sequence, PCM format/sample-count comparison, Miles integration or an accepted replacement, volume/routing and clock ownership; test A/V drift, startup latency, pause/resume, seeks, loops and frame scheduling over full movies. No A/V evidence was produced here.
- TreeFile callbacks preserving archive lookup, offsets, read/seek semantics, async/buffer control and thread lifecycle. Existing BinkTreeFileIO casts AbstractFile pointers to U32; those cannot cross an x64/x86 boundary directly. The experiment used ordinary file I/O only.
- Real graphics integration and device-loss/restoration tests, texture/backbuffer allocation, pitch/orientation, 32A/565/5551 surfaces, scaling, compositing and color/alpha behavior. No D3D texture upload, rendering, input handling or device lifecycle was exercised.
- Preserve and resolve the measured RGB/alpha discrepancies against a declared game-level fidelity criterion, then validate timing, audio, visual output and gameplay transitions. This experiment neither approves an FFmpeg replacement nor proves a helper preserves the original experience.
'''
(root/'report.md').write_text(report)
manifest={str(f.relative_to(root)):dict(bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in sorted(root.rglob('*')) if f.is_file() and f!=p/'artifact-manifest.json'}
size=sum(v['bytes'] for v in manifest.values());assert size<256*1024**2
(p/'artifact-manifest.json').write_text(json.dumps(dict(files=manifest,local_probe_bytes_excluding_manifest=size,vm_probe_bytes=receipt['probe_directory_bytes']),indent=2))
print(json.dumps(dict(local_probe_bytes_excluding_manifest=size,vm_probe_bytes=receipt['probe_directory_bytes'],historical_sources_unchanged=len(checks),oracle_unchanged=True,vm_source_hashes_match=True,all_four_frames_nonblack=True,exact_matches=0)))
