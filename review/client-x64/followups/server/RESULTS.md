# Final-head server validation

Exact source archive: `8e57911e` (SHA256 `a7f3b681cf145b85d50adb04edb098d25d228ae87ff2c5aaa53ccf0be70c1b85`). Fresh32/64 full builds and all three Oracle fixture targets passed. Source-file SHA256 manifest remained unchanged. Installed GCC7.5.0, CMake3.17, Java11; validation configuration RELEASE with C++ optimization overridden to `-O0`, wrappers append `-Wformat`. This is not an optimized production-release proof.

Actual fixture runs on each ABI: DB binding62passes, snapshot-send19, cluster-list7. Clock and OsFile each report ALLPASS on both ABIs; Miff33cases,0failed on both.

Three cluster starts (64,64restart,32) each had84 processes, including38GameServers; executable hashes recorded and all ELFclasses matched the selected ABI. Console reported running and database connected. After console-requested shutdown, Central/GameServers exited; residualTaskManager/LoginServer were explicitly SIGTERM-stopped. Captures after each had zero processes from the validation build. Logs retain connection-closure and broken-pipe messages; no fatal/segfault/assertion matches were found. This does not independently establish final-save acknowledgement.

All activity occurred in a new child of the stopped prior completion disk. Before runtime, the build child was gracefully shut down and preserved as immutable pre-runtime backing, then a separate runtime child was booted. The unrelated personal-labVM and old completion disks were untouched. BothABIs reused the same copied database sequentially; this is not separate-identical-state parity.

No client was connected in this run, so no new login/gameplay/waypoint-save acceptance is claimed. Historical observations remain historical. Controlled crash recovery, realistic soak, full gameplay, and genuine pre272 upgrade remain unproven. The validationVM was requested to shut down after evidence capture.

The files alongside this report exclude backup configs and contain build, fixture, console/process evidence and [summary.json](summary.json). Raw evidence archive is local-only.
