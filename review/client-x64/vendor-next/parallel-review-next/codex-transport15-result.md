No concrete implementation defect found in this bounded pass. Two actionable verification gaps remain; neither establishes a runtime failure.

1. **Successful dispatch marshalling is untested by the inspected host preflight.** It exercises rejection paths and explicitly checks that the vendor DLL remains unloaded ([preflight.cpp:16](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/preflight.cpp:16), [preflight.cpp:49](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/preflight.cpp:49)). Thus it cannot detect wrong argument order, signed conversion, or output-pointer selection in the 39 vendor arms.
   
   **Minimal regression:** use ABI-compatible recording stubs to check each supported arm’s selected function and arguments; include `0xffffffff`/`0x80000000` signed words, unsigned high-bit positions, distinct float arguments, and getter masks 0–3. This would validate marshalling, not vendor behavior or client fidelity.
   
   **Strongest disconfirming evidence:** the implementation preserves signed/float representations through `memcpy` ([host_dispatch.cpp:9](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/host_dispatch.cpp:9)); inspected signed millisecond and loop-offset arguments match the SDK declarations ([Mss.h:4749](/home/akilleez/Work/swg-source/client-build-next/src/external/3rd/library/miles/include/Mss.h:4749), [Mss.h:5178](/home/akilleez/Work/swg-source/client-build-next/src/external/3rd/library/miles/include/Mss.h:5178)). No mismatch observed.

2. **Host failure-output assertions check status only.** The helper poisons the result but verifies only the returned status and `transport_status` ([preflight.cpp:7](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/preflight.cpp:7)). Removing result clearing would therefore escape these assertions.
   
   **Minimal regression:** for `Unsupported`, `InvalidFields`, and `InvalidResource`, start with poisoned output and assert every result field except `transport_status` is zero.
   
   **Strongest disconfirming evidence:** dispatch currently clears the entire result before validation and then sets status ([host_dispatch.cpp:330](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/host_dispatch.cpp:330)). This is a test gap, not observed stale output.

Other strongest disconfirming evidence:

- Span validation enforces contiguous payloads, subtraction-based bounds, canonical empty spans, and exact frame consumption ([codec.cpp:89](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/transport-candidate/codec.cpp:89)).
- Borrowed resolution checks the parent’s live identity; stream retirement invalidates its aliases ([resource_registry.h:103](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/transport-candidate/resource_registry.h:103), [resource_registry.h:126](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/transport-candidate/resource_registry.h:126)). Tests cover parent closing, replacement generations, exhaustion, and independent parents ([tests.cpp:168](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/transport-candidate/tests.cpp:168)).
- Session/lane/lease admission and vendor quiescence are explicit caller requirements, not implemented protections; I did not classify their absence as exploitable implementations ([host_dispatch.h:13](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/host_dispatch.h:13), [resource_registry.h:12](/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/transport-candidate/resource_registry.h:12)).

Product HEAD confirmed: `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. SHA-256 values below were unchanged at the beginning and end of review; paths are relative to the candidate root:

```text
transport-candidate/codec.cpp
15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e
transport-candidate/resource_registry.h
f2a4131c73d831a0e407bd67eb1803ec1f8a72ccd0cf36e6af979cae3e8a3768
host-candidate/registry_resolver.h
2b405ebf56ac51ecc81c8ac919809c5b0f16524c248fc1a932fbc2d7b8fd584a
host-candidate/host_dispatch.cpp
4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595
transport-candidate/tests.cpp
a913db4f70acba9d2c611486a0431cab9c76749e7508f8c32ce5983989ad8eff
host-candidate/preflight.cpp
d71b0aa2fb90aef45ef52e740af53ba96caef753b111326b56f36dadd8919c33
```

Source-only review completed; no tests or candidate executables ran, and the stated 449-check result was not independently verified. No changes, reviewer-output reads, or out-of-scope sound-info/retained-buffer file reads. These components do **not** establish original client experience or full fidelity.