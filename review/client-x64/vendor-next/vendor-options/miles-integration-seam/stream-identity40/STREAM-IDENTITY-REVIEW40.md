# Original DLL stream-sample identity: bounded static review

The inspected original DLL supports one stable sample pointer during the ordinary live-stream paths traced here. Open allocates and stores it; the getter returns the stored pointer; close clears it before release. Driver teardown also clears the member and closes the stream, so the lifetime bound is **stream close or owning-driver teardown**, not merely an explicit close_stream call. This is static evidence for this DLL, not a universal Miles SDK contract or runtime proof.

Input: original Mss32.dll SHA2560785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe. Exports were independently parsed from the PE for this review. Inspection used objdump without loading/executing the DLL. Possessed7.2a Mss.h identifies _STREAM.samp at5090; the actual binary getter establishes the x86 offset. All disassembly, complete private scan and export tables remain under private/; only this semantic note is shareable.

| Path | Actual evidence | Consequence |
|---|---|---|
| Getter export0x2111b9a0 | Nonnull input loads stream+0x0c at0x2111b9f7 and returns it; null input returns zero. | It does not compute a transient/new sample or allocate one. |
| Open export0x2111b840 → core0x21110a40 | Zeroes newly allocated0x11c-byte stream; calls actual allocate_sample_handle at0x21110ada and stores its result at stream+0x0c at0x21110ae1; null branches to failed-open cleanup. | A successfully exposed stream begins with an allocated sample identity. |
| Close export0x2111b910 → core0x21110db0 | Loads stream+0x0c, clears it at0x21110dd7, then calls actual release_sample_handle at0x21110dda; removes/frees stream state later. | Borrowed sample becomes invalid during close; no post-close getter/control is valid. |
| Driver close0x21114110 →0x211340e0 →0x21111b10 | Walks stream list, matches each sample's driver, clears stream+0x0c at0x21111b35, then calls close_stream. | Owning-driver teardown invalidates both stream and borrowed sample even without explicit client close_stream. |
| Start core0x21111740 | Reads stored sample and operates on it; invokes seek/timer paths. | No direct sample-member replacement in inspected body. |
| Byte seek core0x21111420; millisecond seek0x21111a60 | Millisecond path reaches byte seek. Byte seek repeatedly loads existing sample, resets/reinitializes its content, and uses it again. Its bulk zero/copy at0x21111523/0x21111525 targets sample-internal state derived from that pointer, not stream+0x0c. | Reinitialization is not sample identity replacement in these paths. |
| Loop block0x21111890; loop-count wrapper0x2111bd90 | Operate on stored sample/stream fields. | No direct member replacement identified. |
| Service0x211111a0 and timer0x2110ffa0 | Service mutates stream buffering state; timer traverses live streams and invokes service. | No direct member replacement identified in inspected bodies. |

The stream-region scan found the initialization and explicit-close stores above. A broader scan caught the additional driver-cleanup clear, which must not be omitted from the lifetime model. Other nearby +0x0c stores at0x2110f6ba/0x2110f757 belong to a separately allocated0x58-byte function table, not the0x11c-byte stream. Matching an offset alone is not alias analysis.

Limits: this was not an exhaustive interprocedural proof through every indirect codec/file callback or every arbitrary memory alias. No runtime workload or callback was invoked; no general shutdown-quiescence claim follows. The inspected ordinary operations provide positive support for the bridge's cached identity with parent lifetime validation, but do not by themselves discharge all supported-format/indirect-path obligations. Keep re-query/consistency checks and do not weaken them based on this note. Parent should review the private evidence before treating the stable-pointer premise as established for any operational stream gate.

The current private host still has no stream/file integration. Before adding it, stream registry entries need driver parentage; driver retirement must retire streams and their borrowed aliases as well as owned samples. The public native delegate continues to forward the SDK unchanged. Nothing here authorizes runtime, callback registration, product adoption, broader vendor inspection or an updated interface promise.
