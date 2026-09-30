# ByteOrder revision 2 reproduction

Reviewed head: `110c7b4ba7cf317760119c1b298fabe7d30b61d8`. Review production against prerequisite `9eadbbbebd515a0fffad2133300703dff68bd7ef`; the separate imemmove change requires its own approval.

The native run used VS2013 Update 5: cl 18.00.40629.0, link 12.00.40629.0, Windows SDK 8.1. `toolchain-native18.json` records subsequent read-only version/hash observations of both architecture tool executables on the same VM; these are not a complete toolchain lockfile. Exact compiler/include paths used by the run are retained in the archived commands and logs.

From the candidate checkout on Windows, with Python 3 and VS2013 available:

```bat
python -c "import pathlib,subprocess; pathlib.Path('C:/temp/stock-ByteOrder.cpp').write_bytes(subprocess.check_output(['git','show','949451032647e45e42c3aaef3f41b132c8af36e3:src/engine/shared/library/sharedFoundation/src/win32/ByteOrder.cpp']))"
python tools/test-byteorder/run.py --out C:/temp/byteorder-fresh --baseline C:/temp/stock-ByteOrder.cpp
```

Create `C:/temp` if it does not exist. The output directory must not already exist. This is the control-enabled ten-case matrix, not the four-case default. See README for a nonstandard VS2013 installation.

The original master-only candidate failed x64 in Misc.h; `isolated-v1-text.zip` preserves that failure. `stacked-v2-text.zip` is the explicit prerequisite stack run. The original baseline is only ByteOrder.cpp; it intentionally uses the same prerequisite headers as the candidate. It is not a claim that upstream master now builds x64.

All 192 recorded repository source, probe, runner and header hashes match the committed tree. No runtime source changed between that native run and the test commit; only the README was added afterward. These results establish finite function behavior and discrimination, not complete client operation.
