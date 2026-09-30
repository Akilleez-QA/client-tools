# Local preparation v1; native gate not run

Frozen35 authored files and their existing source manifest are byte-identical. This preparation adds `prepare-local35.py`, `run-native35.py`, and a private independent `private-inputs-v1` snapshot. Local preparation verified all frozen33 input hashes, frozen35 source/input hashes and clean product49d0 before copying. No VM was contacted and no native compiler ran.

Private input manifest: `13a7272cdf84d617ea82f70481da686ea4abefc8e198e77e9f3d501f6fc9538a` (9536 files).
Runner: `e2fa5b240a6a1ba645897094fed236edfaf51bd863ff4947f30232626cec6135`.
Unchanged source manifest: `edccd7a8d716f4e81b626c4024e50c6881061361bb54dd1fdea4cc5f0c06057f`.

Proposed invocation after independent root review: stage the private packet in a fresh `C:/native-file-callbacks35`, then run `C:/ci-dpvs-review/python/python.exe C:/native-file-callbacks35/run-native35.py --approved-compile-only` once. The runner validates every staged input, compiles native forwarder first and engine header probe second using the frozen recipe, stops on first failure, inspects actual object machines and the direct Miles import, and records all staged hashes after. Headers are hashed once during compilation, not before/after. Preserve first failure; no retry, linking or execution.

The probe's global `extern` callbacks are shape-only declarations. They are not actual Audio symbols or bodies and provide no link proof. The native source's v120/Win64 guard restricts this test candidate, not a newly proposed product requirement. Neither the gate nor this source preparation claims universal Win32 callback ABI compatibility. The SDK snapshot and later objects/PDB remain private; only authored sources and curated text evidence may be shared for review.
