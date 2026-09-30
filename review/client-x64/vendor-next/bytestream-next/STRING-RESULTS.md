# Checked-once string writer

Local server fork was clean before edit; fork remote is Akilleez-QA/src. No commits or remote writes by this agent. Identical semantic edit applied server first then client, preserving pre-existing uint16_t versus unsigned-short cast spelling.

Existing test runners:
- Server g++ -m32:19 PASS (MissionListResponse not run without full same-ABI libraries).
- Server g++ -m64:20 PASS, same limit.
- Client PE Win32 under Wine wow64:50/50.
- Client PE Win64 under Wine:57/57.
- Includes actual 65,534/65,535 string headers and round trips, existing checked-count bounds; no oversized allocations.
- Client original --bits32 default attempted obsolete win32 Wine prefix and failed before tests; preserved client32.log. Correct supported --wine-arch wow64 rerun passed; no fixture edits.
- git diff --check clean for both edited files. Native MSVC actual consumer compile is being performed independently by build_config_next; these are portable fixture results, not that native result.

Each edit4 insertions/4 deletions. Checked conversion occurs before the first destination write; ByteStream internals and partial-failure semantics remain unchanged. Source hashes: string-repair-manifest.json.
