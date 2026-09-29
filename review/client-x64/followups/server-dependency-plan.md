# Server final-head validation and upstream dependency assessment

## Immutable identities and scope

Read-only local Git inventory: server final head `8e57911e`; PR35 base `22dd13d4a40014899c547cd370de969ac6ae1fdc`; master `7d2159a337281184d6a55db30d2bc9a4013c0e80`. The local master-to-64-bit-types diff is 619 files, +158,163/-6,812 across 50 reachable commits. These numbers describe local refs, not a fresh remote API check.

The previous completion run's full-build scripts and runtime records predate the final four wire commits. They establish prior results, not final-head validation. Prior runtime was 84 processes on each ABI, 38 GameServers and 38 PlanetServers, login/new character/waypoint save-reload and cross-ABI reload. It did not establish full gameplay parity, final-save acknowledgement, crash recovery or independent identical-starting-database comparisons.

## Isolation and safety

The completion experiment's stopped `test.qcow2` backs its stopped `base.qcow2`. No process had either file open. A fresh qcow2 child now preserves both disks as read-only backing data. The separate live personal-lab VM is unrelated and is untouched. Validation VM has only loopback SSH2224 and QEMU restricted networking: no game ports or external route. Oracle boot recovery can write only the fresh child; the preboot backing state remains immutable. This was the pre-execution safety plan; completed results are recorded in server-validation/RESULTS.md.

Before runtime, inspect boot services, credentials' destinations and cluster scripts inside the child. Never run old host CLI helpers: they hard-code SSH2222 and target another environment. Preserve a stopped pre-runtime child copy/overlay checkpoint before DB-mutating tests. A running-disk file copy is not a consistent snapshot. No credential values belong in published logs.

## Build reproduction

Archive precisely `8e57911e` into a new guest source directory, record hash manifest, and use two fresh build directories. Reuse installed dependencies, not existing build outputs. Existing recorded compiler wrappers are `/home/swg/gxx-fmt` and `/home/swg/gcc-fmt`; inspect and archive their text as environment evidence. Prior full build used CMAKE_BUILD_TYPE=RELEASE and CMAKE_CXX_FLAGS_RELEASE=-O0, so it was a low-optimization Release-labelled validation build, not production optimization evidence.

For both ABIs: CMAKE_CXX_COMPILER=gxx-fmt, CMAKE_C_COMPILER=gcc-fmt. For64: ORACLE_HOME=/usr/lib/oracle/18.5/client64, JAVA_HOME=/usr/lib64/jvm/java, explicit Java include/JVM paths and CMAKE_ORACLE_INCLUDE_DIR=/usr/include/oracle/18.5/client64. For32: ORACLE_HOME=/usr/lib/oracle/18.3/client, JAVA_HOME=/usr/java, CMAKE_PREFIX_PATH=/usr/lib32:/lib32, all compile and executable/module/shared link flags -m32, Oracle include /usr/include/oracle/18.3/client. Build all with make -j4, then targets int32_db_binding_test, int32_snapshot_send_test, int32_cluster_list_test. Build success is separate from executing these DB-mutating tests.

Runtime steps after safety confirmation: identify guest launch/config/bin scripts; point only cloned bin/config at final64 output; capture process executable hashes and ELF classes, console runState/dbconnected/game enumerate; console-request shutdown and bounded process exit; explicit residual TaskManager/LoginServer handling. Repeat restart64, then32 against copied schema. Exact launch commands must come from inspecting guest scripts, not guessed names. For deterministic parity use separate children of the same stopped pre-runtime state. Historical sequential cross-ABI reuse is only cross-ABI compatibility evidence.

## src23 dependency decomposition

The dominant diff is `external/ours/library/crypto/src`: 404 files, +156,441/-5,234. Thus about 99% of added lines are vendor crypto source; the remaining diff is 215 files, +1,722/-1,578. This makes vendor isolation valuable without portraying all 158k additions as handwritten port code.

Plausible review units (not yet proven cherry-pick-independent):

1. Crypto++ vendor refresh plus required adapter/build edits. Commit0139fd83 itself says the whole build does not work; follow-up e172d412 and cleanup8be3a301 must be assessed together. Do not submit the initial vendor commit alone or drop licensing files. Validate authentication/token behavior and32/64 builds.
2. Build/toolchain and Oracle discovery: CMake, compiler flags, Java/Oracle lookup. Recent a7c14599 is a focused Oracle19 discovery candidate; old configuration commits interact with vendor layout and should be extracted from final state.
3. Fixed-width archive/message/datafile boundaries plus DB ABI types: archive, network messages, DbBindableInt32/Long, OCI varrays and queries. These are coupled semantic changes, not cosmetic type substitutions; current PR35 repairs known defects in this baseline. Reuse final fixed semantics rather than releasing intermediate broken states.
4. Host-pointer/platform diagnostics and monotonic clock fixes: ec3419db,750f7d86,4fac50d2 are focused candidates but require caller/type and platform builds. They can be evaluated before the larger ABI batch.
5. Remaining server/runtime/script and tool corrections: classify individually by actual behavior, not the broad historical commit subjects.

History is tangled: initial60c8c1fc touches54files including crypto headers, generic/platform types and packed maps; database8fbee785 combines OCI data binding and ServerClock. Merges bring master and PR34 into the branch. Therefore no safe automatic three-way cherry-pick partition has been established. Recommended next artifact is final-diff ownership/dependency map and extracted candidate branches, preserving existing refs. PR35 can merge into64-bit-types; its delivery to master remains dependent on resolving that underlying branch. No rewrite or split performed.

## Confirmed guest details

Guest booted without LoginServer/TaskManager/CentralServer. Oracle does auto-start. Root filesystem has only4.1GiB free, so final builds use a new40GiB virtio scratch filesystem at `/mnt/validation`; no old output reuse. Compiler wrappers only append `-Wformat` to `/usr/bin/gcc` or `g++`. Source is an exact `git archive 8e57911e`; build runner is archived alongside this note.

`swg-main/exec.sh` changes to `exe/linux`, launches `./bin/LoginServer -- @servercommon.cfg` in background, waits4seconds, then launches `./bin/TaskManager -- @servercommon.cfg`. taskmanager.rc defines the remaining services relative to bin. Existing configs have centralServerAddress10.0.0.220 and registrarHost127.0.0.1; restricted guest networking provides isolation even if another endpoint is missed. Existing .32bit/.64bit servercommon copies select JVM loader paths. Console helper pads commands to1023bytes plusNUL and invokes ServerConsole with20second timeout. Do not invoke startServer.sh blindly: it runs `ant start`, an unnecessary layer for pinned executable validation.

Before runtime, gracefully power down this child and freeze its disk as a pre-runtime parent, then boot a fresh runtime child with the scratch build disk. This preserves Oracle's quiescent state after boot recovery without copying a running DB. Record new executable hashes/ELFclass and source manifest. Execution subsequently completed; see server-validation/RESULTS.md.

## Remote base check after execution

GitHub PR23 API reports master baseRefOid1df9ef14e7e990296fd6388575c7d0b2da680b59, head22dd13d4,613files,+158123/-6690. Fetching upstream master returns7d2159a3; its triple-dot comparison is613files,+158127/-6694. Earlier619file figures were a two-tip diff, not PR triple-dot. Do not repeat them as PRsize. The crypto subtree remains404files,+156441/-5234; the local triple-dot remainder is209files,+1686/-1460. Vendor-isolation recommendation is unchanged.
