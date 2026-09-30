# First native55 gate — failed, stopped

One authorized invocation ran. The matrix stopped at its first failure after two compiler attempts. No repair or retry occurred.

- Win32 host-runtime: compiler exit0, no diagnostics, actual COFF0x14c; required header and decorated reference checks passed.
- Win32 host-thunks: compiler exit2; host_sdk_callbacks.cpp line53 reports warning C4702 (unreachable code), promoted by /WX to C2220, no object generated.
- Host install and both AMD64 objects were not attempted. No SDK import-object or completed thunk ABI gate is claimed.

Raw commands, compile logs, include observations and the successful first object's symbols are retained under native-evidence-v1/curated/results. All39 frozen inputs and pinned tools remained unchanged. Curated archive SHA256:1eba37965860a5e974013ce34a47d6ccb58a50e6e494b07cece15cfcb69625e7. SDK remains private; no link, executable, DLL, engine or runtime work occurred. Awaiting parent triage.
