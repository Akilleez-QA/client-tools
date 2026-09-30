# CLI follow-up39 reconciliation

Composer2.5 completed the source-only stream/fixture review. Parent checked every actionable claim against the frozen37 implementation and39 tests. No model vote supplies native evidence.

- Accepted: wrong resource kinds in open/alias replies and stray return/value fields on void stream commands had not been explicitly exercised by the stream tests. Parent42 now runs four such cases through the actual encoder, reply decoder and Session failure path. All four pass once under strict ASan/UBSan, with caller results unchanged and subsequent exchanges refused.
- Rejected as stated: owned versus borrowed wire identity collision. Identity includes kind, and reply validation requires the opcode's kind. Equal slot/generation with different kinds is not the same wire identity. Host registry must separately enforce native ownership; client checks cannot prove that.
- Rejected as a demonstrated bug: controlSample fallthrough. ownedSample checks membership before dereferencing; a borrowed pointer does not become owned simply because lookup fails. Arbitrary memory corruption is not an established path.
- Rejected: null-after-live untested. broken(4) explicitly exercises that condition after successful alias publication. Composer described that same case while calling it absent.
- Borrowed reverb getter is outside the five actual Audio borrowed operations. The intended shared-handle subset includes the reverb setter; extending unsupported operations is not a coverage repair.
- Stale handles after close are outside the native lifetime precondition. Do not turn undefined caller use or arbitrary third-parent counts into new product requirements.
- Host signed interpretation and true vendor fidelity remain separate, already documented requirements.

Grok4.7-medium on the earlier pair35 slice timed out at240seconds with zero output, exit124. The failed service attempt remains recorded and confers no clearance. No identical retry was made. Composer stream review took51.49seconds and returned exit0; its raw prompt, response and input hashes are retained.
