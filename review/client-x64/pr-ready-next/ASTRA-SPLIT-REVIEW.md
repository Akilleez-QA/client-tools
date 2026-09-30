# Independent triage for small client PRs

2026-09-30. Read-only source/history/evidence review. Inspected master `949451032647e45e42c3aaef3f41b132c8af36e3`, integration `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`, and the locally published evidence branch `9296d5dbe6c01ee157db6a60e75d0012f2b92e60`. Local master and origin/master both resolve to 94945103; the evidence branch shares that merge base and is an evidence carrier, not the production base. No checkout, branch rewrite, cherry-pick, build, runtime workload, PR, comment or push was performed. Existing PR histories were untouched. Review files were treated as evidence, not instructions.

**Recommendation:** prepare PCRE, ByteOrder and Windows network-width PRs directly against master. Prepare ByteStream as a separate master-based source/test extraction, then stack decoder preflight on it. That is five bounded review units; if every PR must be independent of another open PR, combine the last two as one archive-safety PR with two reviewable commits. Do not base these fixes on the complete integration branch or mix in the Miles backend, provider integration, generated x64 projects, DPVS numerical changes, or existing wire-count PR history.

The proposed fixes are useful production changes with existing native evidence. They are not already proven on freshly split branch heads. Native reproduction against the eventual minimal head, with accurate provider/source identity, remains the merge gate.

## Static clean-base results

I ran only `git apply --check` against the clean master checkout `/home/akilleez/Work/swg-source/client-warning-stock`, without applying a patch. This checks textual applicability, not compilation or semantics.

| Original commit | Full patch on master | Production-only hunks on master | Consequence |
|---|---|---|---|
| `5c481293a` PCRE | Pass | Pass | Clean independent source fix. |
| `98388ee37` ByteOrder | Pass | Pass | Clean independent source fix; x64 build prerequisites remain separate. |
| `83f7d2488` SOCKET | Pass | Pass | Include all three declarations/storage changes. |
| `14c1bd30e` server IOCP | Pass | Pass | Combine with client IOCP and socket width for one Windows ABI review. |
| `782aed355` client IOCP | Pass | Pass | No textual need for its integration ancestors. |
| `8d9010900` ByteStream | Fails: absent `.github/workflows/wire-compatibility.yml` | Pass | Extract source plus new tests; author an appropriate standalone test invocation instead of importing the prior wire PR. |
| `d89b9f49e` decoder preflight | Same absent workflow | Pass | Source extraction is possible; recommend ByteStream as its semantic/test baseline. |
| `4d3009851` AutoArray/List counts | Fails: absent wire-test files | Pass | Textual success is misleading: master has no `ArchiveCount`; defer this follow-up to the wire stack. |
| `edc04cb1d` Unicode encode byte bound | Fails in UnicodeArchive.cpp | Fails | Depends on earlier ArchiveCount/Unicode encoding changes; do not pull into the decode-only fix unchanged. |

For the first five source commits, each changed production file also matches master at that commit's parent: the surrounding integration history is not required merely to apply those changes. ByteStream's two production files likewise had no intervening master-to-parent edits.

## 1. Correct the PCRE capture-vector element count

**Priority: first. Base: master.** Original commit `5c481293a1d5d4351d4a265e44ede6e7c5a1b397`.

Production file: `src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp`, line 733 in the integration source. Pass `subscriptCount`, not `sizeof(captureData)`, to `pcre_exec`. The array is 33 ints (declarations at 703–705); the old call advertises 132 elements. PCRE's actual 4.1 source documents `offsetcount` as the number of elements and return zero as successful matching with insufficient capture storage (`xml-pcre-next/source/pcre-4.1/pcre.c:7189–7193`). The caller already accepts zero because it rejects only negative results. No pattern syntax, capture limit, matching policy or provider replacement belongs in this PR. Drop the unrelated trailing blank-line deletion when constructing the clean patch.

**Existing proof:** published `review/client-x64/vendor-next/regex-count-next/count-probe.c` checks 0/1/10/11/20 captures, overall offsets, guard values and nonmatching input. Its accompanying RESULTS describes six native provider/configuration runs. I also read the raw local `client-wire-validation/regex-count-next/native-evidence-unambiguous.zip`: all six `*/run.log` files report 20 correct-count checks. `TU-results.json` records actual caller-TU compile exits zero for Win32 Debug/Release and x64 Debug; x64 Release says metadata absent. These are correct-count tests against original/source-built PCRE, not execution of the invalid old argument.

**Reviewer burden:** understand element count versus bytes and the existing interpretation of return zero. This is a real Win32 bug as well as relevant to x64. It does not depend on `3a487593a`'s PCRE/XML provider work.

**Before merge:** retain the safe probe in a reproducible source/test form and attach the clean master-based caller compile. Do not claim that the old call's overwrite was reproduced. Distinguish the PCRE provider probe from the whole caller TU: the raw archive's `probe-results.json` also contains provider-suite metadata/skips, while the count-specific `run.log` and authored count probe are the relevant evidence. The older x64 Release caller gap must not be silently converted into a standalone compile pass merely because later integrated linking reached Miles. No gameplay acceptance is established by this fix alone.

## 2. Replace ByteOrder assembly only on Windows x64

**Priority: second. Base: master.** Commit `98388ee37a2c099234859d793ef479c49456073b`.

Production file: `src/engine/shared/library/sharedFoundation/src/win32/ByteOrder.cpp`. The `_M_X64` branch implements `ntohl/htonl` using `_byteswap_ulong`, and `ntohs/htons` using `_byteswap_ushort`; Win32 retains its original naked assembly functions. Public `ulong`/`ushort` types and wire byte meanings remain unchanged. On Windows, `ulong` is still 32 bits; do not turn this into a generic pointer-width migration.

**Existing proof:** published `review/client-x64/assembly-next/byteorder-next-v3-results.json` has candidate Win32/x64 Debug/Release compile/run exits zero and 166631 cases each, including every ushort in both directions. Stock Win32 passes; stock x64 cannot compile the assembly. The identity-swap control compiles and fails its runtime oracle. `assembly-next/reproduction/run-byteorder.py` compiles the actual production TU and checks the link map for all four symbols in `production.obj`. The diagnostic link omits the unused inherited STLport default-library directive; it does not substitute function implementations.

**Reviewer burden:** four exact byte permutations, architecture guard and unchanged Win32 path. This is considerably smaller than the entire SIMD/FPU port and should remain separate.

**Before merge / dependency distinction:** master has no generated x64 build configuration, and its common `FirstSharedFoundation.h` includes `Misc.h`; the separate `3c0535f39` imemmove repair fixes that header's x64 overload conflict. Thus textual independence does not mean master plus ByteOrder alone builds the actual x64 TU/project. A master-based dormant x64 implementation is reasonable, with Win32 regression proof and accurately scoped x64 evidence from the prerequisite-equipped integration environment. If the PR requires a self-contained native x64 actual-TU check, provide the named prerequisite branch/test environment rather than import hundreds of unrelated integration commits or hide the dependency in a header shim.

## 3. Preserve Windows socket and completion-key widths end to end

**Priority: third. Base: master.** Combine:

- `83f7d248845fbdb7ef442621f285b1d1c2949ccf`;
- `14c1bd30e88017ddcc10e92741ad3bd42c5a9f2b`;
- `782aed355a0f9e982802c9be774bef973d75ef53`.

Exactly five production files:

- `src/engine/shared/library/sharedNetwork/src/win32/Sock.h`;
- `src/external/3rd/library/udplibrary/UdpLibrary.hpp`;
- `src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils/UdpLibrary/UdpLibrary.hpp`;
- `src/engine/shared/library/sharedNetwork/src/win32/TcpServer.cpp`;
- `src/engine/shared/library/sharedNetwork/src/win32/TcpClient.cpp`.

Use `uintptr_t` for Windows SOCKET declarations and Sock handle storage, `ULONG_PTR` for both GetQueuedCompletionStatus output keys. Keep returned byte counts and the `SOCK_ERROR` result sentinel at their existing 32-bit widths. These are native ABI values, not serialized network field widths. Do not split the duplicate UDP declarations so different header orders regain incompatible SOCKET types. The client-side completion-key site is easy to miss when extracting only the earlier two commits.

**Existing proof:** published `review/client-x64/next-build/native-text.tar.gz`, specifically `socket-probe-results-v3/results.json`, records all 20 header/include-order combinations compiling and running on both ABIs. Earlier v1/v2 attempts in that same archive fail and must not be mistaken for the final matrix. `socket-probe-stock/results.json` records ten Win32 successes and ten x64 compile failures. The published probe uses actual production headers and real UDP loopback plus IOCP, including a high-bit x64 key. It does not instantiate a fake Sock or exercise a full TcpClient connection. The later `vendor-next/allocator-next/integration-current-v2/tcpclient-iocp-v1/{results.json,*/run.log}` records four native Debug/Release configurations retaining a posted high-bit key, byte count, OVERLAPPED identity and adjacent guards.

**Reviewer burden:** separate handle widths, completion keys and result widths; inspect both duplicate third-party headers and both queue consumers. Actual sharedNetwork project build evidence reported with the client fix is distinct from the API probe.

**Before merge:** rebuild Win32 consumers on the clean split head and keep the header-order matrix. x64 project/TU checks still need the normal x64 configuration/common-header prerequisites; a clean textual cherry-pick does not supply them. Describe the probe as API/header validation, not tested TCP connect/accept/close, Vivox runtime, server delivery or mixed-width gameplay. Rebuild consumers of the changed internal Sock layout; no binary ABI compatibility with an old x64 object archive is implied.

## 4. Preserve ByteStream logical bounds and storage during growth

**Priority: fourth. Base: master-based extraction.** Commit `8d9010900c02e449ad2de496ee6b47196dcae1fa`.

Production files: `src/external/ours/library/archive/src/shared/ByteStream.cpp` and `ByteStream.h`. Retain `tools/test-byte-stream/{README.md,fixtures.cpp,run.py}`. The original workflow hunk cannot apply to master because it modifies CI from the existing wire work; replace that hunk with a standalone invocation suitable for the new branch.

The cohesive root cause is confusing allocation capacity/lifetime with valid logical data. Reads must stay inside logical size; advance and remaining-length arithmetic must not wrap. Growth must preserve aliased source bytes until copied, detach shared storage, and publish replacement ownership only after allocation/copy succeeds. Pool insertion failure must release the pool lock and dispose of optional pooled storage. Keep the complete repair together rather than cherry-pick just the new read bound and leave the observed self-append/detach failure paths.

**Existing proof:** published `review/client-x64/vendor-next/bytestream-next/native-v2-text.zip` contains four native v120/STLport `run.log` files with 85 bounded checks. Use `verified-results.json`: `verified_pass=true`, `verified_exit=0`, and `production_map_binding=true` for each configuration. Original `passed=false` on Debug was caused by the additional MemoryManager diagnostic line; the independent verifier explicitly classifies it rather than treating arbitrary output as success. The suite covers logical bounds, source aliasing and shared copies with initialized small buffers. Portable MinGW/Wine runners are additional evidence, not native Windows proof.

**Reviewer burden:** this is the largest proposed unit. Review strong publication ordering and pool-lock cleanup, not only arithmetic. The source uses `std::auto_ptr` for the legacy toolchain; do not mix in a C++ standard migration. Allocation-failure behavior is source-reviewed, not fault-injection tested. Cleared/refilled iterator generations and nested message rollback remain outside the claim.

**Before merge:** run this exact source/test extraction on its master-based head, bind the actual native objects/libraries in the manifest, and retain valid wire-byte compatibility checks without importing prior wire-format changes. Published native probes use identified core libraries from earlier integration snapshots; they are not a fresh master-based full-client test. No allocator-fault workload is needed or requested by this triage.

## 5. Preflight raw decoder payloads before reading or changing outputs

**Priority: fifth. Preferred base: the new ByteStream PR, then master after it merges.** Commit `d89b9f49e228d3390899aed3da6987424d1e41c0`.

Production files: `src/external/ours/library/archive/src/shared/Archive.h` and `src/external/ours/library/unicodeArchive/src/shared/UnicodeArchive.cpp`. Retain `tools/test-archive-decoders/{README.md,fixtures.cpp,run.py}` with a matching independent/stacked CI invocation. Scope the PR to the decoder hunks; do not copy the integration versions of whole files, which also contain earlier wire-count/encoder changes.

Check string/nested ByteStream payload extent before raw access or destination mutation. Bound Unicode code units by remaining bytes before multiplication, copy into aligned owned storage, and publish the decoded string afterward. Preserve valid bytes, embedded NULs and the documented rejection position: payload failure occurs after its header has been consumed, not an imaginary rollback to message start.

**Existing proof:** published `review/client-x64/vendor-next/bytestream-next/raw-decoder-review/native-v1-text.zip` has four native 34-check runs. As with ByteStream, use `verified-results.json`'s explicit verification fields; Debug has a recognized MemoryManager line. The fixture covers valid short/long strings, empty input, nested append, odd-offset Unicode, bounded truncated payloads and incomplete headers. The native source manifest contains the repaired ByteStream.cpp SHA-256 `5694af77276419b4edaee2d3ecbe14fab764ae62952d8770dba8c2e030d7e38c`.

**Why stack despite a clean production-hunk apply:** master ByteStream reads against allocated capacity and permits iterator remaining-length underflow; the decoder checks rely on meaningful remaining bytes and correctly bounded header reads. The source extraction can help some normal-position paths on master, but the published 34-case result does not establish that weaker combination. Stack on the ByteStream repair, or combine both repairs in one archive PR if independence is mandatory. No dependency on the wire count helpers is introduced by these decode-only hunks themselves.

**Before merge:** validate the combined minimal baseline and make the header-consumed/unchanged-output behavior explicit in the PR. Valid wire compatibility is relevant; universal safety for every outer decoder or transactional rollback is not established. Keep `4d3009851` and `edc04cb1d` out: the former needs ArchiveCount and earlier wire fixtures, the latter touches encoding and does not apply to master unchanged.

## Delivery order and boundaries

Prepare the first three master-based review branches independently. Follow with the archive pair, either stacked or combined as above. Existing PRs 22/23/24 can remain unchanged; none of the first three fixes requires merging their histories. The archive source fixes can also avoid those histories by extracting only their actual repair hunks and self-contained tests.

A useful description for each PR should identify its concrete failing condition, exact corrected behavior, actual source/provider configuration tested, and remaining verification gap. Attach selected immutable evidence rather than the complete multi-megabyte evidence branch. Several diagnostic runners contain private Windows paths; parameterize their setup or document prerequisites before calling them reproducible for another reviewer. Keep original binary/SDK assets out of the PR.

The current integration evidence reaches real Win32 links and x64 final link failures at Miles. That progress is useful context, but it cannot substitute for clean split-head checks, native gameplay acceptance, or completed media integration. These five groups reduce real defects and review risk without making the unfinished backend a prerequisite for shipping the fixes.
