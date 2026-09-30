# Independent source and first-result check 42

Read the four-case fixture, inherited Script implementation, composed reply validator and first recorded execution log. No rerun, compiler, engine or vendor execution by this reviewer.

Each case first obtains a valid scripted result, changes one field, then serializes and decodes it through the actual composed result validator: open returns Driver instead of Stream; borrowed lookup returns OwnedSample instead of BorrowedSample; void start returns nonzero return_bits; void start supplies stray value[7]. The caller checks BackendFailed, session uncertainty, and suppression of subsequent channel calls. Open/lookup cases also check that the caller's null output variable remains null. The first log has one PASS line for each of cases0–3. No concrete fixture-discrimination defect found for these four claims.

This establishes scripted malformed-result rejection and facade poisoning only. It does not exercise the vendor, actual host stream implementation, native identity stability or every malformed reply field.

Raw SHA256 attribution:

- `test.cpp`: `d6b98bf24f74da1f1f14b98f7dc6ce6951e9920fc58df3f6a4355f34b6da27d3`
- `evidence-v1/malformed-scripted.log`: `d85b303270b7694b5525b4159b9cb2b4e49c3dc5cf30c5754d23b28b5c369808`
- `private-source-v1/startup-bridge23/reply.h`: `5a95a70bc3622bb500057d77a37629fa82127d7fbafe9095abf09b1292e437b6`
