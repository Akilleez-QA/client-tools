# Blind maintainer review — round 1

Reviewed 2026-09-30. Read-only source/evidence audit; no builds or runtime tests performed. I read REVIEW-INPUTS.md, candidates-v1.json, the three actual base-to-worktree diffs, neighboring implementations, PR-v1.md drafts, probe/runner sources, and selected raw historical results. I did not read sibling reviews, ASTRA-SPLIT-REVIEW.md, or other author conclusion documents.

All three worktrees were clean and their HEADs matched candidates-v1.json. Base: `949451032647e45e42c3aaef3f41b132c8af36e3`.

| Candidate | Reviewed HEAD | Engineering | PR readiness |
| --- | --- | ---: | ---: |
| ByteOrder | `8f136d19935515c471af46e56c509df0cbdeed89` | 8.5/10 | 6/10 |
| Socket widths | `a393d1233aada331f99d4edb50f678e8c186fff2` | 7.5/10 | 5/10 |
| PCRE count | `85cd72af93e8d63cdcec5e2ea8a579ea7f2d0b94` | 8.5/10 | 6/10 |

These are good small fixes, but not completed submission packets. I found no demonstrated production defect introduced by the diffs. The required revisions below concern trustworthy verification and reviewability, not demands to broaden these into a full client port. The drafts are commendably explicit about historical evidence and absent candidate validation; that honesty should be preserved.

## ByteOrder

The four x64 implementations correspond directly to the existing 16/32-bit Windows API contracts. `_M_X64` keeps the existing Win32 assembly intact. The adjacent header retains its declarations and calling convention. Scope is appropriate and independent of the other two candidates.

Evidence is unusually good for the function behavior: the probe checks all 65,536 short values, selected long boundaries/bit patterns, and 100,000 generated long values against an independent byte oracle. It tests both directions rather than merely round trips. Historical v3 results show candidate success on four architecture/configuration combinations, stock Win32 success, stock x64 compilation failure, and a no-swap mutation failing. I inspected v3 build/run logs inside `swg-source/client-pr-evidence/review/client-x64/assembly-next/native-text.tar.gz`; the archive also contains failed earlier v2 runs, so links should name the v3 paths explicitly.

The current ByteOrder.cpp SHA-256 is `84d6a070f6412908e2fb95cf4dfb9268478f9dc0be5b2fe4cd10f4b77b7a2f17`, exactly matching the v3 candidate source hash. This supports the draft's “same production patch” statement. It does not establish identity of all headers, compile flags, and external build inputs for the newly isolated branch.

Required before submission/merge:

1. Supply a checkout-scoped reproducer and candidate-bound manifest/results, or establish the complete relevant input equivalence to the historical run. `run-byteorder.py` currently reads `C:/client-next-results/*.audit.log` to obtain definitions/includes and expects several prepopulated `C:/...` locations. A fresh reviewer checkout cannot reproduce it. Accept explicit checkout/output/toolchain arguments and derive or document the actual compile inputs. Preserve the baseline and mutation checks, source hashes, object architecture, and map checks that establish the linked definitions are production code.
2. Replace preparation-only validation prose with exact commands, expected outcome, candidate identity, and a stable evidence location. No full sharedFoundation or client link is required to substantiate this isolated function change.

Optional: omit manually maintained line-count prose from the final PR; reviewers can see the diff. No additional production abstraction or test framework is needed.

## Socket widths

The type changes correctly separate pointer-sized handles/completion keys from 32-bit operation results and transferred-byte counts. `Sock::handle` flows into Winsock calls and initializes/resets to INVALID_SOCKET; the surrounding implementation does not reveal a signed-negative comparison broken by this change. Both production IOCP functions use the address of the changed local as the output parameter and otherwise ignore the key. Updating both is coherent scope. Updating the two UDP header copies avoids incompatible declarations in consumers. The sharedNetwork project targets v120, which makes the added stdint.h dependency plausible for this project.

Historical `socket-probe.cpp` compiles actual headers in both include orders, asserts handle/member widths, then exercises raw Winsock UDP and IOCP. This is useful header compatibility/API evidence. It does not construct Sock or compile either changed IOCP implementation. The later `tcpclient-iocp-probe.cpp`, despite its name, includes only Windows/stdio headers and calls Windows directly. Its four successful historical results therefore cannot validate TcpClient or TcpServer. PR-v1 correctly discloses this distinction. The draft's integration-library compilation claim needs a specific source/build manifest and logs before it can substantiate this isolated branch.

Required before submission/merge:

1. Package and rerun header/include-order checks against the candidate, and compile the actual affected network translation units with clearly identified inputs in Win32 and x64. Baseline x64 failures should distinguish the header width/member errors and each IOCP output-parameter mismatch. A genuine production runtime test is useful but not necessary for this narrow type correction if production compilation and type coverage are convincing; a raw Windows API test alone is insufficient.
2. Make the runner fail the overall command on any unexpected compile/run failure. `next-build/run-socket.py` collects nonzero return codes into JSON but has no aggregate failing exit status. It also extracts into and writes to reusable fixed paths, with no candidate identity verification. Use a clean output directory, checkout argument, explicit result assertions, and source/toolchain identity. Do not let an apparently successful command mask failed cases.
3. State the rebuild requirement: these header changes affect x64 class layout and type signatures, so consumers and relevant libraries must be rebuilt consistently. Distinguish production independence of this PR from any separate x64 configuration or other integration patches needed by the test build. Do not imply this independently enables a complete x64 product build.

Optional: a member/getHandle round-trip probe with a synthetic high-bit value can discriminate handle truncation without treating a fabricated value as a real Windows socket. Keep public description centered on type correctness; real allocated handles need not have high bits set, so UDP loopback alone cannot prove truncation coverage. A combined five-file PR is reasonable; further splitting is not necessary.

## PCRE count

The existing `subscriptCount` is 33 and declares the array's extent. Passing that constant corrects the element/byte confusion without changing allocation or match acceptance. The surrounding code treats only negative pcre_exec results as failure, so a successful match returning zero because capture storage is insufficient remains accepted. This is a small, architecture-independent correction that need not depend on the broader x64 work or a replacement provider.

I inspected `count-probe.c`, both runners, and raw logs/results inside `regex-count-next/native-evidence-unambiguous.zip`. The six provider/configuration probe runs report 20 checks each. They check zero/one/ten/eleven/twenty captures, match spans, adjacent sentinels, and nonmatch behavior. Every probe calls pcre_exec with literal 33. “Stock” in these results identifies a provider variant, not execution of the old production argument. PR-v1 accurately states this limitation. The historical TU results contain Win32 Debug/Release and x64 Debug success; x64 Release says `metadata absent`. Do not describe that as a completed four-way parser compile matrix. The x64 Debug log includes existing size_t-to-int and other warnings; success does not mean warning-free compilation.

Required before submission/merge:

1. Tie the reproducer to this production call site. At present reverting the one-line fix would leave all bounded probe results unchanged. The smallest useful revision is a candidate source/argument assertion alongside a provider-backed bounded probe and actual parser compile evidence; label the assertion as structural validation. Alternatively use a safe test harness derived from the actual call and prove it rejects a reverted argument. There is no need to execute an out-of-bounds old call on a 33-int allocation.
2. Provide explicit provider location/version/hash and reproducible build instructions. The runner depends on `C:/pcre-native-v3`, `C:/parser-integration-v3`, a legacy library, and an external probe copy. `compile-tu.py` recovers command lines from other integration trees and compiles an external scene file. Neither establishes candidate identity. Record source/input hashes and commands, and fail the overall run for missing metadata or failed cases rather than merely writing results. `run.py` and `compile-tu.py` currently do not aggregate failures into a failing process exit status.
3. Clearly distinguish the supported Win32 validation from any optional x64 provider/configuration dependencies. Report missing x64 Release TU coverage explicitly if it remains missing. A full client link or game-level command test is not a prerequisite for this local argument correction.

Optional: restore the unrelated trailing blank line so the product patch is exactly one changed line. Remove irrelevant POSIX-locale skip metadata from this bounded probe's JSON; there is no locale test in count-probe.c, and inherited reporting scaffolding obscures what ran.

## Smallest useful next revision

Keep the production changes essentially as written. Add compact, checkout-scoped validation packets with candidate identity, declared compiler/provider prerequisites, commands that propagate failures, raw expected/actual outcomes, and precise limits. For socket widths ensure real changed implementation compilation; for PCRE ensure the test packet detects a reverted production argument. Preserve historical evidence as historical and link directly to the chosen successful run version. Once these gaps are closed, concise final PR narratives can replace the current preparation notes without overclaiming full-client coverage.
