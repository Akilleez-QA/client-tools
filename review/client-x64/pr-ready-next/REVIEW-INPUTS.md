# Local candidate review inputs, round 1

No PR has been opened. These are working drafts. Production branches are based on upstream master 949451032647e45e42c3aaef3f41b132c8af36e3; candidate identities are in candidates-v1.json. Review each actual diff against that base and inspect neighboring code. Do not assume a small diff is safe.

Evidence/source locations (historical runs, not new-head runs):
- ByteOrder: ../assembly-next/byteorder-probe.cpp and run-byteorder.py; published packet ../../swg-source/client-pr-evidence/review/client-x64/assembly-next/.
- Network: ../next-build/socket-probe.cpp and run-socket.py; ../allocator-next/integration-current-v2/run-tcpclient-iocp.py and tcpclient-iocp-probe.cpp.
- PCRE: ../regex-count-next/count-probe.c, run.py, compile-tu.py.

Score engineering and submission quality separately, 0–10. A 10 requires demonstrated correctness within scope, regression discrimination, reproducibility, exact artifact identity, clear dependencies, and a concise accurate reviewer narrative. Missing evidence is a gap, not evidence of a code defect. Identify concrete fixes and distinguish required fixes from optional improvements. Do not read sibling reviewer reports or ASTRA-SPLIT-REVIEW.md before writing your initial verdict.
