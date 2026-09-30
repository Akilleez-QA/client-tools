# Composition 46 initial portable gate

The ONE authorized initial gate passed at freeze SHA256 `4f04a5beec06c0581a38607334f1eb3847fa9c5838ac30875da00c47f3f32b31`.

- Strict clang C++11 build exit: 0. Build log empty.
- ASan/UBSan execution exit: 0; no sanitizer diagnostics; leak detection enabled.
- Raw test output: `PASS 333 composed selected-service/control-owner checks; scripted worker/job only`.
- Named scenario groups: 20, each PASS marker exactly once. These are scenario groups, not 20 individual assertions or independent runtime integrations.
- Frozen inputs changed after run: none (31 checked).
- Attempts: one; no retries, repairs or post-result test expansion.

The command, sanitizer settings, exits, per-marker counts and post-run identity checks are preserved in evidence-v1/results.json; raw outputs are build.log and run.log. The result is ready for blind source/evidence review. Test execution has stopped.

This executes the real selected-services adapter, mapper, owner, coordinator, Invocation and codec with scripted portable worker/job plumbing. It exercises distinct tables through the composed path, retained lifetime, ACK/forward-return ordering, late causal arrivals while waiting, uncertainty and terminal rejection. It does not execute the actual Windows FileInvocationJob TU, engine thread/TLS, real filesystem callbacks, Endpoint I/O, DLL callbacks, or vendor lifecycle. The temporary native-header macro wrapper gives no MSVC calling-convention evidence. The Table nonassignment compatibility declaration has no new native compiler validation from this gate. Existing native41/native39 results are separate evidence; native64 library/runtime fidelity is not implied.

The pretest corrections and both draft freezes remain preserved. PLAN.md remains frozen as the pre-execution plan; this result supersedes only its statement that the gate had not yet run. No VM, native build, engine/allocator workload, product edit, or original DLL run occurred.
