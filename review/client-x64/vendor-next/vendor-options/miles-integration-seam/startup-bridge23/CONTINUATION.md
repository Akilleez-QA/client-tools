POODO_CONTINUATION_V3_0
schema: POODO_CONTINUATION/3.0
capsule_id: PC-startup23-1
revision: 1
parent_capsule: null
generated_at: '2026-09-30T13:02:09.369262+00:00'
objective: Bounded startup metadata composition under parent faithful-x64 goal; no child native goal is
  exposed and root goal is not complete.
acceptance:
- id: AC-startup23-1
  criterion: One pinned Release live x64/x86 no-sample23-request metadata/startup run, owned replies,
    one lifecycle, named errors and cleanup.
authority:
  allowed: New startup-bridge23 sources, native compilation and one owned Wine/null-sink genuine DLL slice.
  prohibited: Product edits, commit/push, vendor publication, Audio/ExitChain/allocator-fault run, playback,
    samples, streams or callbacks.
constraints: Keep frozen components/old21 packet unchanged; exact source, SDK, DLL and executable hashes;
  no automatic runtime retry.
user_directives: Parent assignment 2026-09-30 and approved PLAN; one Backend owner, fixture-only oracle,
  retained paths, explicit status mapping.
current_head: D-startup23-1
claims:
- id: O-startup23-1
  state: observed
  status: active
  text: v2 Release pair compiled; exactly23 live no-sample requests and cleanup passed with genuine original
    DLL and owned text.
  source_type: artifact
  locator: evidence-runtime-v1/results.json
  observed_at: '2026-09-30T12:58:35Z'
  freshness: exact recorded artifacts only
  evidence_family: EF-startup23-live
  rehydration_status: checked
  supports:
  - AC-startup23-1
  limits: One Wine run; no full startup/product/callback/Bink/fidelity claim; direct same-vendor fixture
    is not an independent implementation.
evidence_bundles:
- id: E-startup23-0
  request: First Release pair build
  material_inputs:
  - A-startup23-0
  result_or_locator: evidence-native-v1/
  completeness: complete
  artifacts:
  - A-startup23-1
  supports_claims: []
- id: E-startup23-1
  request: Separately planned compile repair and single23-request run
  material_inputs:
  - A-startup23-2
  result_or_locator: evidence-native-v2/ and evidence-runtime-v1/
  completeness: complete
  artifacts:
  - A-startup23-3
  - A-startup23-4
  supports_claims:
  - O-startup23-1
orientations:
- id: OR-startup23-1
  text: The selected components compose within this bounded live path; parent owns wider runtime acceptance.
  depends_on:
  - O-startup23-1
  confidence:
    artifact_identity: high
    test_path: high
    causal_model: high
    outcome: high
  strongest_rival: H-startup23-1
alternatives:
- id: H-startup23-1
  status: discriminated
  text: Composition loses reply text or confuses metadata and lifecycle errors.
  discriminator: Owned copies survive later replies/shutdown; pure status4/5 rejection and live4097 refusal;
    exact logged contexts.
decisions:
- id: D-startup23-1
  text: Freeze source/runtime evidence and hand off narrow result; no further runtime work in this packet.
  depends_on:
  - O-startup23-1
  reversible: true
  reverse_if: Independent review finds load-bearing defect or a later authorized integration contradicts
    this bounded claim.
predictions:
- id: P-startup23-0
  kind: prospective
  created_at: '2026-09-30T12:43:01Z'
  created_before_observation: true
  observable: PLAN P1 both Release builds pass /W4 /WX.
  acceptance: Both architectures compile with unchanged receipt inputs.
  failure_means: Compile prediction failed; no runtime authorized by a failed build.
  oracle: A-startup23-0
  oracle_version: source-v1
  artifact: A-startup23-0
  environment: Native Windows v120 C:/startup-bridge23
  status: failed
  status_history:
  - pending
  - failed
  outcome_evidence:
  - E-startup23-0
- id: P-startup23-1
  kind: prospective
  created_at: '2026-09-30T12:57:07Z'
  created_before_observation: true
  observable: BUILD-REPAIR-v2 passes both Release builds and original PLAN23-request scope.
  acceptance: Exact hashes/order/status/oracles/ownership and independent cleanup gates.
  failure_means: Stop and preserve failure; no automatic retry.
  oracle: A-startup23-2
  oracle_version: source-v2
  artifact: A-startup23-2
  environment: Native v120 build; one owned Wine prefix/null sink, original DLL hash in PLAN.
  status: passed
  status_history:
  - pending
  - passed
  outcome_evidence:
  - E-startup23-1
outcomes:
- id: OUT-startup23-1
  state: passed
  evidence:
  - E-startup23-1
contradictions:
- id: C-startup23-1
  target: P-startup23-0
  evidence:
  - E-startup23-0
  scope: x86 fixture implicit assignment warning C4512 with /WX
  effect: invalidate
  affected_ids: []
  disposition: repaired
  repaired_by:
  - P-startup23-1
artifacts:
- id: A-startup23-0
  locator: source-v1.tar
  identity_method: sha256
  identity: 2c75741f746e980294a785bc63185b0657c582d08da88e6f17f5d5ee623be27f
  mutable: false
  captured_at: '2026-09-30T12:55:39.028013+00:00'
  role: input
- id: A-startup23-1
  locator: evidence-native-v1/receipt.json
  identity_method: sha256
  identity: 272083988e82c98411eb08760059fd6b619c9b660e8fcf953b65d0720f74344b
  mutable: false
  captured_at: '2026-09-30T12:55:56.358749+00:00'
  role: evidence
- id: A-startup23-2
  locator: source-v2.tar
  identity_method: sha256
  identity: 8e7849382825d6d98734d38b1718b654b2d68452fed0c008785ce7aa4a1b78e8
  mutable: false
  captured_at: '2026-09-30T12:57:22.633004+00:00'
  role: input
- id: A-startup23-3
  locator: evidence-native-v2/receipt.json
  identity_method: sha256
  identity: 94d2e537b1b85e49a505cb6d9bddc04c001ecaedce75ad62f9d472b0de8755e5
  mutable: false
  captured_at: '2026-09-30T12:57:41.327506+00:00'
  role: evidence
- id: A-startup23-4
  locator: evidence-runtime-v1/results.json
  identity_method: sha256
  identity: bc8a6a32adc18fcc214d6c528d40ec301d3b90e8c3dfc191f58904fb0bd344d8
  mutable: false
  captured_at: '2026-09-30T12:58:35.354438+00:00'
  role: evidence
rehydration:
  status: complete
  losses: []
delivery_state: built
outcome_state: passed
highest_justified_claim: One exact23-request original-DLL metadata/startup composition passed across x64/x86
  with held-module version, owned text and one lifecycle.
required_runtime_observation: None for this gate E-startup23-1; product Audio, real TreeFile scheduling,
  callbacks/retirement, Bink and failure policy remain open.
who_controls_next_test: Parent/user within existing authorization; engine and allocator-fault workloads
  remain prohibited.
next_step: Parent reconciles independent review and uses RESULTS.md scope/frontiers for next integration
  decision.
END_POODO_CONTINUATION_V3_0
