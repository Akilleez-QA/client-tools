"""Complete evidence collection and execute already-built probes exactly once.

Earlier collectors misread map section 0001 and column heading Lib:Object as
archives. No probe ran. This repair reads only addressed symbol rows. It never invokes
a compiler or linker and preserves the original collector failure separately.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    spec = importlib.util.spec_from_file_location("recorded_replay", out / "replay-ssemath.py")
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    digest, write_json, execute = replay.digest, replay.write_json, replay.execute
    contract = json.loads((out / "precommitted-contract.json").read_text())
    result_path = out / "results.json"
    results = json.loads(result_path.read_text())
    assert not (out / "results-after-first-inventory-repair.json").exists()
    assert len(results["configurations"]) == 2
    for row in results["configurations"]:
        assert row.get("error") == "Cannot resolve mapped library: Lib"
        assert all(row.get(label + "_exit") == 0 for label in ("production", "probe", "link"))
        assert "run_exit" not in row
    (out / "results-after-first-inventory-repair.json").write_bytes(result_path.read_bytes())
    results["collector_repair"] = {
        "reason": "Only addressed symbol rows identify archives; exclude section 0001 and heading Lib:Object",
        "prior_results": ["results-before-inventory-repair.json", "results-after-first-inventory-repair.json"],
        "native_probe_executions_before_repair": 0,
        "compiler_or_linker_replays_during_repair": 0,
        "repair_sha256": digest(__file__),
        "python_runtime": {"path": sys.executable, "sha256": digest(sys.executable)},
    }
    setup_result = subprocess.run(["cmd", "/d", "/c", str(out / "native-environment.cmd")],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
    assert setup_result.returncode == 0
    env = {k.upper(): v for k, v in os.environ.items()}
    for line in setup_result.stdout.decode(errors="replace").splitlines():
        if "=" in line and not line.startswith("="):
            key, value = line.split("=", 1)
            env[key.upper()] = value
    project = Path("C:/client-next-build/src/engine/shared/library/sharedMath/build/win32")
    old_root = Path("C:/ssemath-reload-control-v1")
    expected_header = tuple(contract["record_header"])
    expected_size = 32 + 33280 * 56 * 4
    for row in results["configurations"]:
        config = row["configuration"]
        folder = out / (config + "-x64-candidate")
        old = old_root / (config + "-x64-candidate")
        row["second_pre_execution_inventory_error"] = row.pop("error")
        try:
            assert not (folder / "records.bin").exists(), "Do not rerun a probe"
            for label in ("production", "probe"):
                assert digest(folder / (label + ".obj")) == row[label + "_object_sha256"]
            for name in ("source", "header", "probe", "comparator"):
                assert digest(contract[name]) == contract[name + "_sha256"]
            mapping = (folder / "probe.map").read_text(errors="replace")
            library_tokens = [line.split()[-1] for line in mapping.splitlines() if re.match(r"^\s+[0-9a-fA-F]{4}:[0-9a-fA-F]{8}\s+", line)]
            libraries = sorted({token.split(":", 1)[0] for token in library_tokens if re.match(r"^[A-Za-z_][A-Za-z0-9_.-]*:", token)})
            row["linked_libraries"] = []
            for name in libraries:
                filename = name if name.lower().endswith(".lib") else name + ".lib"
                resolved = next((Path(p) / filename for p in env.get("LIB", "").split(";")
                                 if p and (Path(p) / filename).is_file()), None)
                assert resolved is not None, "Cannot resolve mapped library: " + name
                row["linked_libraries"].append({"map_name": name, "path": str(resolved), "sha256": digest(resolved)})
            assert row["linked_libraries"]
            historical = (old / "records.bin").read_bytes()
            assert hashlib.sha256(historical).hexdigest() == contract["historical_records_sha256"][config]
            assert struct.unpack_from("<8I", historical) == expected_header and len(historical) == expected_size
            row["executable_sha256"] = digest(folder / "probe.exe")
            row["map_sha256"] = digest(folder / "probe.map")
            row["run_exit"] = execute([str(folder / "probe.exe"), str(folder / "records.bin")],
                                      project, env, folder, "run", timeout=90)
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
            comparison = {"oracle": contract["oracle"],
                          "historical_sha256": contract["historical_records_sha256"][config],
                          "fresh_sha256": hashlib.sha256(fresh).hexdigest(),
                          "historical_bytes": len(historical), "fresh_bytes": len(fresh),
                          "header": list(actual_header), "expected_header": list(expected_header),
                          "record_count": actual_header[2], "words_per_record": actual_header[3],
                          "mismatched_bytes_in_common_length": mismatched,
                          "length_difference": len(fresh) - len(historical), "first_differences": first_differences,
                          "byte_identical": fresh == historical,
                          "schema_and_count_match": actual_header == expected_header and len(fresh) == expected_size}
            write_json(folder / "raw-comparison.json", comparison)
            row["raw_comparison"] = comparison
            row["schema_comparator_exit"] = execute([sys.executable, contract["comparator"],
                                                     str(old / "records.bin"), str(folder / "records.bin")],
                                                    project, env, folder, "schema-comparison", timeout=30)
            assert comparison["schema_and_count_match"], "Schema/count failure"
            assert comparison["byte_identical"], "Exact historical record comparison failed"
            assert row["schema_comparator_exit"] == 0, "Recorded schema comparator rejected output"
            for name in ("source", "header", "probe", "comparator"):
                assert digest(contract[name]) == contract[name + "_sha256"]
            row["okay"] = True
        except Exception as exc:
            row["error"] = str(exc)
        finally:
            write_json(result_path, results)
            print(json.dumps({key: row[key] for key in row if key in ("configuration", "okay", "error", "run_exit")}))
    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results["okay"] = all(row["okay"] for row in results["configurations"])
    write_json(result_path, results)
    return 0 if results["okay"] else 1


if __name__ == "__main__":
    sys.exit(main())
