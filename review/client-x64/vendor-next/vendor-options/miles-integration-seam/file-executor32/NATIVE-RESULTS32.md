# Step32: worker compiled; first adapter failure preserved

One authorized20-object gate ran. Debug|Win32 engine-worker compiled cleanly, exit0, actual COFF0x14c. Debug|Win32 invocation-job then failed exit2:

```
file_channel.h(66): error C2220: warning treated as error - no 'object' file generated
file_channel.h(66): warning C4512: 'MilesFileChannel26::Binding': assignment operator could not be generated
```

Binding's const members in the unchanged file26 header cause this warning under v120 `/W4 /WX`. It is a frozen-adapter source warning surfaced by this gate, not an original-engine warning. No suppression, source repair or retry occurred. The remaining18 objects (including all Release/x64 objects) were not attempted. File-channel, canonical-services and codec objects were not reached even for DebugWin32.

Both attempted include-boundary checks passed:232 headers for engine/STLport,222 for modern invocation-job. All9547 staged input hashes match before/after. Actual include hashes were recorded once during compilation; system headers were not rehashed afterward. No before/after system-header attestation is claimed.

Raw evidence is under `native-evidence-v1/curated/results`, with commands, logs, include hashes and results. Twelve curated text files were fetched; object/PDB/SDK snapshots remain private. The successful worker object's hash and COFF machine were reread on the guest and agree with the compiler receipt. This is not link, x64, SDK64 or runtime evidence.

Manifest: `949d56d8a0d23efe1e4f0ed9461a2e19cdafd36d7849469fdc66f4f259e1c2e1`. Runner: `a0ec2996dd06364697e975665f698f6b95b009f4e2403b2ca0a0952c72b02a31`. Curated ZIP: `01f04817d6fc586e257f2ceca131912e9a3fdb2977a885ec51d43a222d7baa4a`.

Frozen31 failure and32 source identities remain unchanged. Product remains clean49d0. Compiler/tooling work has stopped. No link, engine execution, DLL invocation, Audio/ExitChain workload or product adoption occurred.
