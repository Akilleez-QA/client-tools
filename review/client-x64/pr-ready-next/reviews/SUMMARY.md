# Independent Astra reviews and revisions

Two fresh history-free Astra agents reviewed the same code/evidence from different roles. Initial verdicts preceded all implementation revisions and peer-report exchange. Follow-ups retain their own context but remain independent of the other reviewer's reports. Neither reviewer executed the native tests; they inspected raw artifacts and checked source identity. Scores are engineering judgments, not calibrated probabilities or runtime proofs.

| Candidate | Initial maintainer: engineering / readiness | Initial senior: engineering / readiness | Revised maintainer | Revised senior |
|---|---:|---:|---:|---:|
| ByteOrder | 8.5 / 6 | 9 / 7 | 9.5 / 9 | 9.5 / 9 |
| Socket/IOCP | 7.5 / 5 | 8 / 5.5 | 9.5 / 9.5 | 9.3 / 9 |
| PCRE count | 8.5 / 6 | 9 / 6.5 | 9 / 9 | 9.5 / 9 |

## Closed substantive review requests

- Reproducers now run from a checkout with explicit dependencies and fresh outputs, preserve raw logs and identities, and fail on missing/failed cases.
- ByteOrder retains the independent byte oracle, real-TU symbol/architecture binding, stock control and deliberately broken implementation control. A fresh isolated compile exposed the common-header prerequisite; it is declared as a separate dependency, with the failed attempt preserved.
- Network tests compile the actual changed implementations. Independent key reversions trigger real x64 SDK errors, so a successful raw IOCP demo can no longer stand in for implementation compilation. All three handle headers and include orders are covered. Consumer rebuild requirements are explicit.
- PCRE tests now detect reversal of the actual production argument through a labeled lexical assertion before any provider execution. Runtime cases use a real, identified provider and safe bounded storage. Output reuse is rejected without overwriting evidence.
- Final metadata separates production revisions from later commits containing exactly the tested tool bytes. Absolute evidence URLs are present in the PR drafts.

## Still separate

The imemmove prerequisite is being validated and must receive its own review. ByteOrder/network readiness scores are conditional on it, not an approval of its other callers. None of these fixtures establishes full-client startup or gameplay fidelity. The PCRE caller's four TU compiles use separately identified development headers/configurations; the master-based candidate is not a standalone x64 build.

No new production defect was demonstrated in the three patches. The revisions address evidence/test quality and explicit dependencies. No score has been rounded up to10, and no PR was opened.
