# Reproduce the Win32 Release link-input comparison

This native Windows runner performs a clean baseline product rebuild, replaces only
SwgClient's project file with the candidate revision, relinks in the same directory,
and compares complete executables. Only PE timestamps and PDB age are normalized;
PDB identity, paths, executable instructions and other data are not ignored.

Prerequisites: Python 3.12+, native VS2013 v120/MSBuild12, the Win32 SDK and
DirectX dependencies required by stock SwgClient, and a prepared build environment
with the same per-user property settings used by a successful stock build. Supply
that tree as `--environment-template`. Its ignored dependencies/configuration files
are copied into a new disposable output directory; tracked source is replaced by
an archive of the specified Git base and compiled outputs are rebuilt. No SDK,
game assets, credentials or prebuilt test executables are distributed here.

Create archives on a Git-equipped host (no Git installation is needed in the Windows build VM):

```sh
git archive --format=tar 949451032647e45e42c3aaef3f41b132c8af36e3 -o baseline.tar
git archive --format=tar HEAD -o candidate.tar
```

Copy those archives to the native build machine, then run:

```powershell
python tools/test-link-inputs/run.py --base-archive C:\baseline.tar `
  --candidate-archive C:\candidate.tar `
  --environment-template C:\prepared-client-environment --output C:\link-proof-new `
  --msbuild 'C:\Program Files (x86)\MSBuild\12.0\Bin\MSBuild.exe'
```

The output directory must not exist. The candidate archive may alter only the SwgClient
project and this test directory; other production changes are rejected rather
than compared under a misleading cleanup claim. Source trees supplied to the
runner are not edited. Each build's executable is removed before execution to
prevent a stale output being accepted. `run.json` records full base/candidate SHAs from Git archive PAX headers,
archive digest, commands and outcome; logs and `.exit` files accompany the two
executables and `comparison.json`.

To inspect an existing pair independently:

```sh
python tools/test-link-inputs/compare.py product-before.exe product-after.exe --output comparison.json
```

This proves only the supplied Win32 Release pair. Different configurations require
their own evidence. The full product prerequisites are not present on standard
GitHub-hosted runners: this entrypoint does not claim an automated hosted v120
product build, resolve vendor licensing, or prove dynamic libraries are unused.
