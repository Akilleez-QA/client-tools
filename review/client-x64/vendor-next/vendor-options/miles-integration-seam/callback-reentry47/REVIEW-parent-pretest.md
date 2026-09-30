# Parent review and first portable gate

Reviewed the exact guard implementation, both production patches, six selected translation units and their pinned dependency provenance, full test body and runner before execution. Scope is authored C++ with a channel observation counter; no vendor DLL, engine allocator, host-audio or product work.

Prediction: same-thread facade/request/close reentry is rejected before selected-session/channel access; swallowed guard rejection remains CallThrew and cannot encode a reply; nested calls and exceptional unwind restore TLS; another thread is not suppressed. Successful compilation and final scenario marker with exit zero under ASan/UBSan support only these bounded cases. Cross-thread callback-created cycles, actual host termination and fidelity remain open.

Single attempt authorized after all29 frozen identities matched. Retain first compile/run failure, do not auto-rerun. Guard and dependency files remain unchanged; protocol2 composition is explicit.
