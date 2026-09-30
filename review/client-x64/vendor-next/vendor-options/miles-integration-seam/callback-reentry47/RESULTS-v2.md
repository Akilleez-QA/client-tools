# Callback reentry gate47

V1 failed at link: actual ClientMilesPipe required MilesStartup::signedValue, while its real metadata_wire.cpp had been omitted. No test executed. This was a failed gate, not invalidated evidence. The source, runner and raw linker log remain preserved.

V2 adds exactly that unchanged real dependency from stream-native38. All other production source, tests, flags and expected behavior remain unchanged. Parent compared the source trees and runner paths before execution. First v2 GCC C++11 strict ASan/UBSan pthread build and bounded run passed; build log empty, exits0, all31 frozen inputs unchanged.

The run exercises actual modified pipe entry points and Invocation: public startup/internal request/close rejection before channel access; sticky failure despite a callback swallowing rejection; independent callback throw; nested invocation refusal; same-thread unwind; another thread's scope does not suppress the caller. It uses an authored channel counter and no vendor/engine runtime.

No Windows TLS ABI, arbitrary callback-created-thread cycle detection, actual host failure/termination or full-client fidelity is established. Native object checks remain separate.
