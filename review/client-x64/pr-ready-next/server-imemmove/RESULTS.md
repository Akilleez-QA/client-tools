# Server memory-move helper submission

Base: SWG-Source/src `master`, `7d2159a337281184d6a55db30d2bc9a4013c0e80`.
Candidate: Akilleez-QA/src `review-ready/server-imemmove`, `1481143ca4f033ef979faff52a4d03bb8d636292`.
Production commit: `abdd4e94`; later commits add tests and CI only.

The three production files change +5/-5 lines: distinguish `imemmove(..., int)` from the CRT name, delegate with `size_t`, and update the three int-count calls in Md5 and Iff. No platform types or wire formats change. This is the server counterpart of [client PR #25](https://github.com/SWG-Source/client-tools/pull/25), independently applicable to the server's current master.

| Check | Outcome | Evidence scope |
|---|---|---|
| Candidate Linux32, GCC 16.2.1 | 30 checks; actual Md5/Iff compile | Release header policy, no whole-library link |
| Candidate Linux64, GCC 16.2.1 | 30 checks; actual Md5/Iff compile | Two existing Iff warnings retained |
| Upstream Linux32 | 30 checks | Same fixture against original implementation |
| Upstream Linux64 | Exactly two expected ambiguity errors | Strict negative control, no binary executed |
| Candidate native VS2013 Win32 Release | 30 checks | Exact repository headers, no replacements |
| Candidate native VS2013 x64 Release | 30 checks | Exact repository headers, no replacements |
| MSVC diagnostic classifier | 14 tests | Reject missing, duplicate and unrelated errors |

[Hosted Linux CI](https://github.com/Akilleez-QA/src/actions/runs/36818778615) passed at the candidate head, reproducing the Linux matrix, actual consumer compiles and pinned upstream controls with its own toolchain. The workflow retains only text artifacts. Hosted CI and native VS2013 are different environments; neither result substitutes for the other.

Local commands, hashes and unedited compiler/runtime logs are in [logs](logs). The native run used an exact Git archive containing the three required header libraries and the test directory. All included repository-header hashes recorded by both native runs were compared with the candidate Git blobs; compiler and system-header hashes remain recorded separately. No Windows server build or initialized-engine Debug runtime is claimed. The native logs retain the `PLATFORM_WIN32` macro-redefinition warning.

Linux64's actual Iff compile retains warnings at unchanged lines 638 and 644: legacy master defines `uint32` as `unsigned long`, so those memcpy calls read eight bytes from four-byte int objects. This submission does not repair that pre-existing LP64 type issue. Linux32's actual caller compile logs contain no warnings.

The valid-buffer oracle uses a pre-copy snapshot, checks the full destination buffer and return pointer, and exercises both overlap directions, disjoint/identical regions and zero length with valid pointers. The helper keeps its Debug pointer checks and adds no new length validation. No invalid-length, null-pointer, full-server or gameplay equivalence claim follows from these checks.

Reproduce with the candidate's [test instructions](https://github.com/Akilleez-QA/src/blob/1481143ca4f033ef979faff52a4d03bb8d636292/tools/test-imemmove/README.md). A reviewer can run Linux checks without the Windows SDK; native Windows checks require the stated compiler environment.
