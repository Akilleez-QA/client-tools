POODO_CONTINUATION_V3_0
schema: POODO_CONTINUATION/3.0
capsule_id: PC-nativesample27-2
revision: 2
parent_capsule: PC-nativesample27-1
generated_at: '2026-09-30T14:34:28.445378+00:00'
objective: Prepare five native-Miles-shaped sample operations and object-only gate under incomplete parent
  faithful-x64 goal.
acceptance:
- id: AC-nativesample27-1
  criterion: Minimal typed header/direct SDK forwarding/example prepared; portable object checks pass;
    stop before VM pending root review.
authority:
  allowed: One parent-reviewed v120 AMD64 object gate and text-only evidence collection, now completed.
  prohibited: No link/PE/vendor/engine execution, product/frozen edits, retry or automatic repair.
constraints: Five sample operations only; opaque allocated identity, exact extent and signed output types;
  no playback claim.
user_directives: Match native Miles64 shape first; avoid original helper release-on-bind-failure leak
  in sample.
current_head: D-nativesample27-2
claims:
- id: O-nativesample27-1
  state: observed
  status: active
  text: Two portable objects compile first attempt, all five facade references unresolved, no link/execution
    and unchanged recorded inputs.
  source_type: artifact
  locator: evidence-portable-v1/receipt.json; sample-symbols.log
  observed_at: '2026-09-30T14:27:24.086428+00:00'
  freshness: Named snapshot only
  evidence_family: EF-nativesample27-portable
  rehydration_status: checked
  supports:
  - AC-nativesample27-1
  limits: Actual SDK assertions and native object/import gate remain unrun; no lifetime or playback outcome.
- id: O-nativesample27-2
  state: observed
  status: active
  text: Single v120 AMD64 object gate passed actual header assertions, three COFF machines and exactly
    five unresolved SDK imports; inputs unchanged, no link/execution.
  source_type: artifact
  locator: evidence-native-v1/receipt.json; native-symbols.log
  observed_at: '2026-09-30T14:34:28.445378+00:00'
  freshness: Named snapshot and compile only
  evidence_family: EF-nativesample27-native
  rehydration_status: checked
  supports:
  - AC-nativesample27-1
  limits: Object/type/import proof only; actual x64 DLL availability, input lifetime and playback remain
    unobserved.
evidence_bundles:
- id: E-nativesample27-1
  request: Portable header/type/example object compilation and unresolved reference inspection.
  material_inputs:
  - A-nativesample27-source
  result_or_locator: evidence-portable-v1/
  completeness: complete
  artifacts:
  - A-nativesample27-portable
  supports_claims:
  - O-nativesample27-1
- id: E-nativesample27-2
  request: Authorized prepared driver --approved-compile-only at fresh C:/native-sample27, actual v120
    AMD64 and private pinned header.
  material_inputs:
  - A-nativesample27-source
  result_or_locator: evidence-native-v1/
  completeness: complete
  artifacts:
  - A-nativesample27-native
  supports_claims:
  - O-nativesample27-2
orientations:
- id: OR-nativesample27-1
  text: Five direct native operations are prepared; native gate requires parent review.
  depends_on:
  - O-nativesample27-1
  confidence:
    artifact_identity: high
    test_path: high
    causal_model: medium
    outcome: low
  strongest_rival: H-nativesample27-1
- id: OR-nativesample27-2
  text: Native source shape now compiles against possessed SDK; runtime and pipe remain separate gates.
  depends_on:
  - O-nativesample27-2
  confidence:
    artifact_identity: high
    test_path: high
    causal_model: medium
    outcome: high
  strongest_rival: H-nativesample27-1
alternatives:
- id: H-nativesample27-1
  status: discriminated within compile/type scope
  text: Native forwarding differs in actual SDK types or fails the intended v120 build.
  discriminator: Prepared actual-header /Zs and /c, AMD64 COFF and exactly five unresolved imports.
decisions:
- id: D-nativesample27-1
  text: Freeze source and hand off for root/CLI review; no VM work.
  depends_on:
  - O-nativesample27-1
  reversible: true
  reverse_if: Review or later authorized compile finds a shape/ownership defect.
- id: D-nativesample27-2
  text: Freeze new native evidence without altering original preparation/source packet.
  depends_on:
  - O-nativesample27-2
  reversible: true
  reverse_if: Review reveals attribution or shape mismatch.
predictions:
- id: P-nativesample27-native
  kind: prospective
  created_at: '2026-09-30T14:21:16.388145+00:00'
  created_before_observation: true
  observable: Three native v120 AMD64 objects with all actual SDK assertions and exactly five unresolved
    imports.
  acceptance: Pinned header/sources/tools unchanged; no link or PE.
  failure_means: Preserve first failure, make reviewed new revision rather than edit frozen snapshot.
  oracle: A-nativesample27-source
  oracle_version: PLAN and prepared build-native.py
  artifact: A-nativesample27-source
  environment: Future C:/native-sample27, actual v120 amd64 and private pinned7.2a header.
  status: passed
  status_history:
  - pending
  - passed
  outcome_evidence:
  - E-nativesample27-2
outcomes:
- id: OUT-nativesample27-1
  state: passed
  evidence:
  - E-nativesample27-2
contradictions: []
artifacts:
- id: A-nativesample27-source
  locator: source-v1.tar
  identity_method: sha256
  identity: 34dd35b74995f1166d6b4ba68391feaa53e8e367812e0ea7b1a7aab23351eb82
  mutable: false
  captured_at: '2026-09-30T14:27:24.086428+00:00'
  role: input
- id: A-nativesample27-portable
  locator: evidence-portable-v1/receipt.json
  identity_method: sha256
  identity: da9beebfb82ed64790635f56c2cf734c42679274e29e9965140305c32d7d06b1
  mutable: false
  captured_at: '2026-09-30T14:27:24.086428+00:00'
  role: evidence
- id: A-nativesample27-native
  locator: evidence-native-v1/receipt.json
  identity_method: sha256
  identity: 6bd45d43d5d6e4a7430eafa1d360db2c3bd7d0caa40db908eb6452c01f10ca1c
  mutable: false
  captured_at: '2026-09-30T14:34:28.445378+00:00'
  role: evidence
rehydration:
  status: complete
  losses: []
delivery_state: built
outcome_state: passed
highest_justified_claim: Five sample source operations compile under actual v120/Win64 SDK declarations
  with three AMD64 objects and five unresolved real imports.
required_runtime_observation: None for this compile-only gate; vendor/sample runtime outside authorization.
who_controls_next_test: Parent /root
next_step: Parent reviews the frozen native evidence and selects the next bounded implementation gate.
END_POODO_CONTINUATION_V3_0
