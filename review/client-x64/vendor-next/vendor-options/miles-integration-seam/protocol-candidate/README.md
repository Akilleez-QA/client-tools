# Experimental protocol review packet

Start with miles_wire.h (fixed layout/opcodes) and API-MAP.md (all61 field mappings). CONTRACT.md holds lifecycle, callback and unresolved lock/thread semantics separately. No implementation, adoption, runtime-fidelity or full-client claim.

Compile evidence: GCC -m32/-m64 syntax checks pass. Native VS2013/v120 Win32 and x64 sdk-declarations.cpp compile exit0 against actual repository Mss.h. The follow-up v3 validates61 frozen exact callable types (return, parameter types and calling convention),6 callback types, fixed scalar signedness/widths and all message sizes/offsets. This proves compatibility with the included actual header declarations, not behavioral equivalence of serialization or future thunks. No copied SDK code or vendor binary is bundled here.

Known blockers: speaker-array extent/lifetime, buffer-retention/reassignment policy, real caller thread/lane and nested lock/callback admission, return-string shadow lifetime. Explicit sizes require tiny Audio adapters at the sample-cache and WAV-info call sites, not unsafe header scanning. MSS version is host macro query because x64 default macro targets MSS64.DLL. Bink must share real host driver; its video transport is outside this schema.

Verification detail: initial v2 generator failed on compact `*AILCALL` spacing before writing updated source; its native run therefore only repeats v1 checks and is not counted as61-signature evidence. Corrected v3 generator froze all61 types and both native compilations exit0. v1 source/results and v2 failed-generation history are preserved. `exact-signature-map.json` records the private original header SHA256 and per-opcode type list, not the SDK header itself.
