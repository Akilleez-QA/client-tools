# Composition68 source contract

Inputs are frozen plain-pipe61 and reviewed paired-bootstrap64. This is author-only source work, not a test/build/runtime target. Preserve both inputs. Parent owns the next review gate.

| Input | Exact integration |
|---|---|
|61 plain ClientMiles.h | Becomes the sole selected public header at candidate/backend-boundary24/ClientMiles.h. No std types or pipe arguments. |
|61 PipeCore.h | Move to backend-boundary24/pipe/PipeCore.h; include ../ClientMiles.h. Preserve private ClientMilesPipeCore57 namespace and imports of the public opaque types. |
|64 ClientMilesPipe.cpp | Rename implementation TU to PipeCore.cpp. Keep opaque ClientMiles structs and the actual ClientMilesPipe Session owner; move operation definitions and four-argument installer into private core namespace. Remove old partial facade header includes. No implementation logic/validation order is replaced with61's older core. |
|64 Session/LiveChannel/Channel | Retain actual runtime reference, raw retained channel, selected callback pins, verified-resource scan, pure reply owner validation before returned/join, both-pipe bootstrap and failure behavior. Session includes PipeCore.h instead of obsolete public Failure/OwnedText declarations. |
|61 guarded wrappers | Place at backend-boundary24/pipe/ClientMilesPipe.cpp; route all45 definitions to that64-derived private core. Use copied52 fatal boundary and existing64 guard47. No new public file installer is exported. |
|64 native-file-callbacks35 header | Reduce to compatibility include of the one plain public header; exact callback typedefs now come from that header. No runtime callback or TLS policy changes. |
|52 private failure boundary | Copy h/cpp unchanged into a private directory. Composition root must bind its engine fatal reporter before any public call. Bootstrap remains a private call with its existing explicit failure behavior. |

Do not compile any alternate native facade TUs or obsolete partial declaration headers. The copied source tree preserves64 parents for traceability; its selected pipe source list must be explicit. Old public64 object must not coexist with the new wrappers. There is one Sample/OwnedStream identity and one existing proxy registry, not aliases to distinct classes.64's inline namespace code and selected runtime remain the implementation.

Exactly45 public definitions remain, with the same17 omissions as61. The real64 installer exists privately but does not become a46th public definition: callback TLS adoption and public installation remain gated. No stubs are added for EOS, text snapshots/version, locks, image binding, metadata or missing telemetry. Fatal Session destruction and unavailable normal close are preserved, not replaced by inferred shutdown success.
