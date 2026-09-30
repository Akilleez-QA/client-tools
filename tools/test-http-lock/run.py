"""Native VS2013 checks of the checkout's real VeCritsec header; Python 3.8+."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quoted(path):
    return '"' + str(path) + '"'


def execute(command, cwd, log, timeout):
    started = time.monotonic()
    try:
        run = subprocess.run(command, cwd=str(cwd), stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=timeout)
        code, output = run.returncode, run.stdout
    except subprocess.TimeoutExpired as error:
        code, output = "timeout", error.stdout or b""
    log.write_bytes(output)
    return code, output.decode(errors="replace"), time.monotonic() - started


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, required=True, help="New output directory")
    parser.add_argument("--stock-header", type=Path, help="Optional unmodified baseline header")
    parser.add_argument("--vcvarsall", type=Path, default=Path(
        "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat"))
    args = parser.parse_args()
    root, out = args.checkout.resolve(), args.out.resolve()
    header = root / "src/engine/client/library/clientGame/src/shared/HTTPpost/VeCritsec.hpp"
    probe = root / "tools/test-http-lock/probe.cpp"
    types = root / "src/engine/shared/library/sharedFoundationTypes"
    inputs = [header, probe, Path(__file__).resolve(), args.vcvarsall]
    inputs += [types / "include/public/sharedFoundationTypes/FoundationTypes.h",
               types / "src/shared/FoundationTypes.h", types / "src/win32/FoundationTypesWin32.h"]
    if args.stock_header:
        args.stock_header = args.stock_header.resolve()
        inputs.append(args.stock_header)
    hashes = {str(path): digest(path) for path in inputs}
    out.mkdir(parents=True, exist_ok=False)
    (out / "inputs.json").write_text(json.dumps(hashes, indent=2))
    results = []
    for config in ("Debug", "Release"):
        for platform, arch, expected_machine in (("Win32", "x86", 0x14c), ("x64", "amd64", 0x8664)):
            modes = ["candidate"] + (["stock"] if args.stock_header else [])
            if (config, platform) == ("Release", "x64"):
                modes += ["broken-acquire", "broken-release"]
            for mode in modes:
                directory = out / (config + "-" + platform + "-" + mode)
                directory.mkdir()
                content = (args.stock_header if mode == "stock" else header).read_bytes()
                failure = None
                if mode == "broken-acquire":
                    old, new = b"_interlockedbittestandset( &m_iLock, 0 )", b"0"
                    failure = "other thread excluded while nested"
                elif mode == "broken-release":
                    old, new = b"_InterlockedExchange( &m_iLock, 0 );", b"/* diagnostic: no release */"
                    failure = "final unlock permits retry acquisition"
                if failure:
                    if content.count(old) != 1:
                        raise RuntimeError("Mutation site is missing or ambiguous: " + mode)
                    content = content.replace(old, new)
                local_header = directory / "VeCritsec.hpp"
                local_header.write_bytes(content)
                shutil.copyfile(probe, directory / "probe.cpp")
                flags = ["/EHsc", "/W4", "/Y-", "/DWIN32", "/volatile:ms", "/Gy",
                         "/MTd" if config == "Debug" else "/MT",
                         "/Od" if config == "Debug" else "/O2",
                         "/I" + quoted(root / "src"), "/I" + quoted(directory),
                         quoted(directory / "probe.cpp"), "/Fo" + quoted(directory / "probe.obj"),
                         "/Fe" + quoted(directory / "probe.exe"), "/link",
                         "/MAP:" + quoted(directory / "probe.map"), "kernel32.lib"]
                # cl forwards only the remainder of /link's response-file line.
                (directory / "build.rsp").write_text(" ".join(flags))
                script = directory / "build.cmd"
                script.write_text("@echo off\ncall " + quoted(args.vcvarsall) + " " + arch +
                                  " >nul\nif errorlevel 1 exit /b %errorlevel%\nwhere cl\ncl @" +
                                  quoted(directory / "build.rsp") + "\nexit /b %errorlevel%\n")
                compile_code, build_log, compile_seconds = execute(
                    ["cmd.exe", "/d", "/c", str(script)], directory, directory / "build.log", 120)
                run_code, run_log, run_seconds, machine = None, "", None, None
                if compile_code == 0:
                    image = (directory / "probe.exe").read_bytes()
                    pe_offset = struct.unpack_from("<I", image, 0x3c)[0]
                    if image[pe_offset:pe_offset + 4] != b"PE\0\0":
                        raise RuntimeError("Not a PE executable")
                    machine = struct.unpack_from("<H", image, pe_offset + 4)[0]
                    run_code, run_log, run_seconds = execute(
                        [str(directory / "probe.exe")], directory, directory / "run.log", 45)
                if mode == "stock" and platform == "x64":
                    passed = compile_code not in (0, "timeout") and "C4235" in build_log
                elif failure:
                    passed = (compile_code == 0 and machine == expected_machine and run_code == 1
                              and ("FAIL " + failure + " error=") in run_log)
                else:
                    passed = (compile_code == 0 and machine == expected_machine and run_code == 0
                              and run_log.splitlines().count("SUMMARY 27/27") == 1
                              and sum(line.startswith("PASS ") for line in run_log.splitlines()) == 27)
                result = dict(name=directory.name, passed=passed, compile=compile_code, run=run_code,
                              machine=machine, compile_seconds=compile_seconds, run_seconds=run_seconds,
                              header_sha256=digest(local_header))
                results.append(result)
                (out / "results.json").write_text(json.dumps(results, indent=2))
                print(json.dumps(result), flush=True)
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
