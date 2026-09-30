# Native Miles interface checkpoint 39

The product checkout remains clean at `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. This checkpoint contains component source and evidence; it does not link or run the full x64 client.

## Replacement boundary

The caller-facing `ClientMiles` functions follow the Win64 declarations in the possessed Miles 7.2a header. For example:

```cpp
HSTREAM open_stream(HDIGDRIVER driver, const char *filename, int32_t streamMemory);
HSAMPLE stream_sample_handle(HSTREAM stream);
void set_sample_volume_levels(HSAMPLE sample, float left, float right);
void close_stream(HSTREAM stream);
```

The direct adapter forwards these calls to the actual SDK names. Its imports remain unresolved until an actual x64 library is supplied. The temporary pipe adapter uses the same source declarations and hides its process, wire IDs, proxy storage and file routing. SDK headers and vendor binaries remain private. A future backend change requires rebuilding consumers; this is not a promise of binary interchangeability between arbitrary Miles releases.

Both allocated samples and stream-borrowed samples use the common opaque `Sample` pointer expected by the native API. Their ownership differs: releasing an allocated sample and closing a stream are separate operations. Callback typedefs preserve native pointer width and calling convention.

## New evidence

| Component | Observation | Limit |
| --- | --- | --- |
| Playback and paired outputs | Native36 compiled the x64 pipe, x86 Backend anchor and actual dispatcher; their SDK import counts were 0, 5 and 39 | No runtime output-equivalence claim |
| Streams and shared sample pointers | Native38 compiled three AMD64 objects; the direct adapter has exactly nine SDK imports and the expected caller symbols | The host still refuses stream opens pending file integration |
| Stream state tests | Tests39 cover simultaneous parents, duplicate identities, cross-parent alias refusal, open failures and inherited owned controls; tests42 discriminate four malformed replies | Scripted source behavior, not measured audio fidelity |
| File callbacks | Native35 compiled the direct callback adapter against actual `Mss.h`, with the sole import `AIL_set_file_callbacks`; the engine declaration probe also compiled | The overall gate failed an overbroad header predicate. Raw failure is preserved; parent attribution shows all seven rejected headers came through existing FirstSharedFoundation/STLport and match earlier hashes. No Audio link/runtime proof |
| Session file admission | Candidate34 reuses the Coordinator for one session file table before a driver exists | No callback installation or receiver/worker composition yet |

Native and pipe adapters have now compiled against the same stream declarations. The file-owner implementation and host callback association are the next connections needed to make that interface operational.

## Remaining behavior questions

Static inspection of the original DLL supports stable stream-sample identity on the examined open/start/seek/loop/service paths. Stream close **or owning-driver teardown** invalidates that identity. Future host registration must retain driver parentage and invalidate descendants. Indirect codec and callback paths were not exhaustively proved.

Input-buffer retirement remains open. Provider failure can leave incoming state installed, and actual callers do not expose one universal buffer-owner hook. See `binding-retirement38` and `input-owner39`. The original DLL's identity also does not establish that the helper gives it the same floating-point state as the game; exact Audio/Miles boundaries still need passive measurement.

## Delivery and next work

Source is authored, listed component objects are built, and scripted mechanisms are checked. Full-client and media acceptance remain unobserved. The strongest current claim is compile-compatible native and pipe source interfaces across the listed subsets. Next are actual file routing, safe binding ownership, playback/callback/teardown checks, then full native client and representative gameplay acceptance.

Work stays on the working fork; no new PR or upstream change. The previously rejected real-engine/allocator workload was not rerun.
