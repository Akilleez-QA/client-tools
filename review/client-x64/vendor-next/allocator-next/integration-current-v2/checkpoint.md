# Integration v2

Immutable committed source: 94a81438c4c442f21105a58047c82d34e04c9cb4.
Source is git archive,20,533 file hashes; uncommitted TrackIR and crypto proposals
are excluded. Includes reviewed Mozilla graph cleanup, Audio and Archive narrowing,
committed allocator minimum-free-block fix and previous renderer dependencies.
The superseded precommit dirty patch remains as a historical capture only; it is
NOT the source of this native run.

Native tree C:/integration-current-v2/workspace/repo, mapped R: in build session.
All132 evaluated outputs passed isolation (66 projects × Debug/Release x64).
Native VS2013/v120, actual SDKs, no stubs or feature defines. Fresh x64 Release
then Debug compiling. Previous v1 Q: matrix/results untouched.

Crypto is a separate diagnostic candidate, absent from v2. First scoped-header
candidate passes positive /WX controls and negative leak-header discrimination on
both ABIs/configurations; before/after layout probes match. Full crypto build3/4:
Debug x64 advances to independent StringStore count narrowing/AnyMessages bool
warnings and later STLport deque/memory includes. No overall crypto pass claimed.

## Completed frozen matrix

Release x64:3874 warnings/1 error,450s; TcpClient SDK completion-key output type.
Debug x64:3722 warnings/1 error,315s; crypto PCH balanced-pack warning under /WX.
Neither configuration reached product link. Original source remains exact94a in R:
until explicitly versioned incremental overlay. Separate private Q: affected-project
probes pass sharedNetwork all4 and final crypto all4. New crypto runtime checks
10/10 Win32 and12/12 x64 both modes, bounded as detailed in crypto findings.
