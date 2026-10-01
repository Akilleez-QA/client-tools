# Server memory-move PR: full legacy build

Exact submitted source: `1481143ca4f033ef979faff52a4d03bb8d636292` (SWG-Source/src #37). On 2026-10-01 a fresh disposable archive of that revision completed the full legacy server build locally: exit 0, 7 minutes 38 seconds. All 7,925 tracked input hashes were unchanged afterward. Six database source/header files were generated, and all 20 inspected executable outputs were ELF32.

The container was `cekisswg/swg-vm3.01-i386@sha256:115f4900a398b2cd585c02020d2667b252e51b9932e3dd3eabc77912723ed674`. Its image architecture is amd64; the generated compile flags and inspected binaries establish the 32-bit build. Mount the source at `/home/swg/swg-main/src`, set `CMAKE_INCLUDE_PATH=/usr/include/oracle/18.3/client`, and run `ant -Dbits=32 -Dnproc=2 clean build_src` there. The source mount must be writable because this upstream base generates database files inside it.

[Build log](build.log), [source revision](revision.txt), [summary](summary.json), [compiler flags](flags.make.txt), [executable identities](elf-identities.json), and [generated-file hashes](generated.json) are retained. No vendor binaries or SDK headers are included. The unchanged-input comparison was independently inspected locally; its original full manifests are retained privately.

Three linker warnings report the legacy Oracle library's missing `libaio.so.1` dependency. This is a compile/link result, not a runtime test of these artifacts, an LP64 full-server result, or proof that the existing upstream CI job is green. The separately proposed workflow repair addresses that job; the PR's portable/native regression evidence remains in the parent directory.
