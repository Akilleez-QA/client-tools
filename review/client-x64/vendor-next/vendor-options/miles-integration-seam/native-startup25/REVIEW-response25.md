# Response to blind senior review

The parent accepts the three bounded findings. This remains a compile-only
increment; its sample is not executable product policy.

- Use a freshly constructed `Observations` for each call to the sample. Reusing
  it can retain branch-dependent output. No executed result relies on reuse;
  the sample has not been executed at all.
- The sample's `stereoProvider` input must equal the possessed SDK's stereo
  specification. Arbitrary caller-supplied values do not model SWG's fallback.
  The next source revision should use a named constant checked against the SDK
  and reset observations at entry before any vendor operation.
- The recorded native receipt does contain transitive headers, including the
  expected Miles header. Equal empty header sets were not the basis of this
  run. The next build-driver revision must nevertheless reject empty discovery
  and require that exact SDK header before treating header identity as covered.

Frozen v1 sources, archives and receipts are retained unchanged. These are
accepted follow-up requirements before promoting the sample or reusing its
build driver for new evidence, not retroactive fixes to the recorded run.
