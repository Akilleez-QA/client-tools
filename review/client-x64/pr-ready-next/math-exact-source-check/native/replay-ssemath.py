"""Replay two recorded x64 TU builds; require exact historical record identity.

The native commands retain every flag and input. Only object, executable and map
outputs (and the linker's matching object inputs) move into --output. No SDK,
production source, historical record or historical command is modified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def execute(argv, cwd, env, folder, label, timeout=120):
    write_json(folder / (label + "-command.json"), argv)
    try:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout)
        (folder / (label + ".log")).write_bytes(result.stdout)
        return result.returncode
    except subprocess.TimeoutExpired as exc:
        (folder / (label + ".log")).write_bytes((exc.stdout or b"") + b"\nTIMEOUT\n")
        return -999


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--vcvars", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "results.json").exists(), "Do not overwrite a previous run"
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    source = Path(contract["source"])
    header = Path(contract["header"])
    probe = Path(contract["probe"])
    comparator = Path(contract["comparator"])
    identity = {"source": {"path": str(source), "sha256": digest(source)},
                "header": {"path": str(header), "sha256": digest(header)},
                "probe": {"path": str(probe), "sha256": digest(probe)},
                "comparator": {"path": str(comparator), "sha256": digest(comparator)}}
    write_json(out / "input-identity.json", identity)
    for name in ("source", "header", "probe", "comparator"):
        assert identity[name]["sha256"] == contract[name + "_sha256"], name + " mismatch"

    # Read the vcvars output in memory only; never save the environment dump.
    setup = out / "native-environment.cmd"
    setup.write_text('@echo off\ncall "' + str(args.vcvars) + '" amd64 >nul\n'
                     'if errorlevel 1 exit /b %errorlevel%\nset\n', encoding="utf-8")
    setup_result = subprocess.run(["cmd", "/d", "/c", str(setup)],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
    assert setup_result.returncode == 0, "Native environment unavailable"
    env = {k.upper(): v for k, v in os.environ.items()}
    for line in setup_result.stdout.decode(errors="replace").splitlines():
        if "=" in line and not line.startswith("="):
            key, value = line.split("=", 1)
            env[key.upper()] = value

    results = {"contract_sha256": digest(args.contract), "runner_sha256": digest(__file__),
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "qualification": "Existing integrated client dependency environment; native x64 TU only",
               "input_identity": identity, "configurations": []}
    write_json(out / "results.json", results)
    for config in ("Debug", "Release"):
        old = args.historical_root / (config + "-x64-candidate")
        folder = out / (config + "-x64-candidate")
        folder.mkdir(exist_ok=False)
        row = {"configuration": config, "architecture": "x64", "okay": False}
        results["configurations"].append(row)
        try:
            historical = (old / "records.bin").read_bytes()
            historical_sha = hashlib.sha256(historical).hexdigest()
            assert historical_sha == contract["historical_records_sha256"][config], "Historical oracle changed"
            expected_header = tuple(contract["record_header"])
            assert struct.unpack_from("<8I", historical) == expected_header
            expected_size = 32 + 33280 * 56 * 4
            assert len(historical) == expected_size
            original = {label: json.loads((old / (label + "-command.json")).read_text())
                        for label in ("production", "probe", "link")}
            redirected = {}
            changes = []
            for label, command in original.items():
                adjusted = []
                for token in command:
                    mapped = token
                    if label in ("production", "probe") and token.startswith("/Fo"):
                        mapped = "/Fo" + str(folder / (label + ".obj"))
                    elif label == "link":
                        if token in (str(old / "production.obj"), str(old / "probe.obj")):
                            mapped = str(folder / Path(token).name)
                        elif token.startswith("/OUT:"):
                            mapped = "/OUT:" + str(folder / "probe.exe")
                        elif token.startswith("/MAP:"):
                            mapped = "/MAP:" + str(folder / "probe.map")
                    if mapped != token:
                        changes.append({"command": label, "before": token, "after": mapped})
                    adjusted.append(mapped)
                redirected[label] = adjusted
            assert len(changes) == 6, "Only two object outputs and four linker paths may change"
            write_json(folder / "original-commands.json", original)
            write_json(folder / "allowed-command-redirections.json", changes)
            row["original_command_sha256"] = {label: digest(old / (label + "-command.json")) for label in original}
            row["historical_records_sha256"] = historical_sha
            row["compiler"] = {"path": original["production"][0], "sha256": digest(original["production"][0])}
            row["linker"] = {"path": original["link"][0], "sha256": digest(original["link"][0])}
            compiler_include = Path(original["production"][0]).parents[2] / "include"
            row["intrinsic_headers"] = [{"path": str(compiler_include / name), "sha256": digest(compiler_include / name)}
                                        for name in ("intrin.h", "xmmintrin.h")]
            guard = Path(next(token[3:] for token in original["production"] if token.startswith("/FI")))
            row["v120_guard"] = {"path": str(guard), "sha256": digest(guard)}
            row["direct_project_headers"] = []
            for relative in contract["direct_project_headers"]:
                path = source.parents[7] / relative
                row["direct_project_headers"].append({"path": str(path), "sha256": digest(path)})
            for label in ("production", "probe", "link"):
                code = execute(redirected[label], args.project, env, folder, label)
                row[label + "_exit"] = code
                assert code == 0, label + " failed"
                if label != "link":
                    obj = folder / (label + ".obj")
                    assert struct.unpack_from("<H", obj.read_bytes())[0] == 0x8664
                    row[label + "_object_sha256"] = digest(obj)
            mapping = (folder / "probe.map").read_text(errors="replace")
            row["symbol_owners"] = {}
            for symbol in ("canDoSseMath", "rotateTranslateScale_l2p", "rotateScale_l2p",
                           "skinPositionNormal_l2p", "skinPositionNormalAdd_l2p"):
                owners = [line.strip() for line in mapping.splitlines()
                          if "?" + symbol + "@SseMath@@" in line and "production.obj" in line]
                assert owners, "Production symbol binding missing: " + symbol
                row["symbol_owners"][symbol] = owners
            libraries = sorted(set(re.findall(r"\s([A-Za-z0-9_.-]+):[^\s]+\s*$", mapping, re.M)))
            row["linked_libraries"] = []
            for name in libraries:
                filename = name if name.lower().endswith(".lib") else name + ".lib"
                candidates = [Path(p) / filename for p in env.get("LIB", "").split(";") if p]
                resolved = next((p for p in candidates if p.is_file()), None)
                assert resolved is not None, "Cannot resolve mapped library: " + name
                row["linked_libraries"].append({"map_name": name, "path": str(resolved), "sha256": digest(resolved)})
            assert row["linked_libraries"], "Map library inventory empty"
            row["run_exit"] = execute([str(folder / "probe.exe"), str(folder / "records.bin")],
                                      args.project, env, folder, "run", timeout=90)
            assert row["run_exit"] == 0, "Probe execution failed"
            fresh = (folder / "records.bin").read_bytes()
            actual_header = struct.unpack_from("<8I", fresh)
            first_differences = []
            mismatched = 0
            for offset, (before, after) in enumerate(zip(historical, fresh)):
                if before != after:
                    mismatched += 1
                    if len(first_differences) < 32:
                        first_differences.append({"byte_offset": offset, "historical": before, "fresh": after})
            comparison = {"oracle": "Fresh corrected records must equal historical candidate records byte-for-byte",
                          "historical_sha256": historical_sha, "fresh_sha256": hashlib.sha256(fresh).hexdigest(),
                          "historical_bytes": len(historical), "fresh_bytes": len(fresh),
                          "header": list(actual_header), "expected_header": list(expected_header),
                          "record_count": actual_header[2], "words_per_record": actual_header[3],
                          "mismatched_bytes_in_common_length": mismatched,
                          "length_difference": len(fresh) - len(historical), "first_differences": first_differences,
                          "byte_identical": fresh == historical,
                          "schema_and_count_match": actual_header == expected_header and len(fresh) == expected_size}
            write_json(folder / "raw-comparison.json", comparison)
            row["raw_comparison"] = comparison
            row["schema_comparator_exit"] = execute([sys.executable, str(comparator), str(old / "records.bin"),
                                                     str(folder / "records.bin")], args.project, env, folder,
                                                    "schema-comparison", timeout=30)
            row["executable_sha256"] = digest(folder / "probe.exe")
            row["map_sha256"] = digest(folder / "probe.map")
            assert comparison["schema_and_count_match"], "Schema/count failure"
            assert comparison["byte_identical"], "Exact historical record comparison failed"
            assert row["schema_comparator_exit"] == 0, "Recorded schema comparator rejected output"
            for name, path in (("source", source), ("header", header), ("probe", probe), ("comparator", comparator)):
                assert digest(path) == contract[name + "_sha256"], name + " changed during run"
            row["okay"] = True
        except Exception as exc:
            row["error"] = str(exc)
        finally:
            write_json(out / "results.json", results)
            print(json.dumps({key: row[key] for key in row if key in ("configuration", "okay", "error", "production_exit", "probe_exit", "link_exit", "run_exit")}))
    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results["okay"] = len(results["configurations"]) == 2 and all(row["okay"] for row in results["configurations"])
    write_json(out / "results.json", results)
    return 0 if results["okay"] else 1


if __name__ == "__main__":
    sys.exit(main())
