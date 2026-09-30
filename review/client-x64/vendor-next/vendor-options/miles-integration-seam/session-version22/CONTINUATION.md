POODO_CONTINUATION_V3_0
schema: POODO_CONTINUATION/3.0
capsule_id: PC-session-version22-1
revision: 2
parent_capsule: PC-session-version21-1
generated_at: 2026-09-30T12:35:35Z
objective: Targeted parent-owned SessionVersion design correction; root faithful x64 goal remains active under parent.
acceptance:
  - id: AC-session-version22-1
    criterion: Direct held-original-HMODULE resource query, macro-output equality, failure-preserving owned wire response and x64 consumption.
authority:
  allowed: New session-version22 sources, v120 builds, bounded original DLL resource probes, two exact copies as data mappings.
  prohibited: Prior revision or product edits, SDK body/vendor publication, startup/device/playback/allocator/engine fixture, PR/push.
constraints: Preserve revision21 source and evidence; exact original DLL and fixture SDK hashes in PLAN.md; C:/session-version22 only.
user_directives: Parent correction assignment 2026-09-30; use direct resource1 HMODULE query and retain original macro only as restricted oracle.
current_head: D-session-version22-1
claims:
  - id: O-session-version22-0
    state: observed
    status: invalidated
    text: Prior inference that revision21 basename equality guaranteed supplied-module identity across all admitted held-module states.
    source_type: artifact
    locator: ../session-version21/REVIEW-senior22.md
    observed_at: 2026-09-30 senior22 source/specification review
    freshness: preserved finding
    evidence_family: EF-session-version22-review
    rehydration_status: checked
    supports: []
    limits: Does not contradict prior single-module runtime observations; no old wrong-version native reproduction.
  - id: O-session-version22-1
    state: observed
    status: active
    text: Direct supplied-handle adapter passed macro comparison, missing-resource preservation and two basename-independent data mappings; x64 consumers retained 7.2a.
    source_type: artifact
    locator: evidence-v1/runtime-v1/results.json
    observed_at: native build-v1/runtime-v1 2026-09-30
    freshness: exact recorded artifacts only
    evidence_family: EF-session-version22-native
    rehydration_status: checked
    supports: [AC-session-version22-1]
    limits: Identical-copy mapping test cannot distinguish different version contents; no live transport/product/lifetime concurrency proof.
evidence_bundles:
  - id: E-session-version22-0
    request: Blind predecessor review
    material_inputs: []
    result_or_locator: ../session-version21/REVIEW-senior22.md
    completeness: complete
    artifacts: []
    supports_claims: [O-session-version22-0]
  - id: E-session-version22-1
    request: Eight native builds and twelve native runs with exact original DLL copies
    material_inputs: [A-session-version22-1]
    result_or_locator: evidence-v1/
    completeness: complete
    artifacts: [A-session-version22-2, A-session-version22-3]
    supports_claims: [O-session-version22-1]
orientations:
  - id: OR-session-version22-1
    text: Direct API handle flow removes the reviewed basename dependency; bounded tests support handoff for separate review.
    depends_on: [O-session-version22-1]
    confidence: {artifact_identity: high, test_path: high, causal_model: high, outcome: high}
    strongest_rival: H-session-version22-1
alternatives:
  - id: H-session-version22-1
    status: discriminated
    text: Adapter still uses a basename or compile-time constant.
    discriminator: Source directly passes HMODULE to LoadStringA; poison value and data mappings absent from normal basename lookup both return resource bytes.
decisions:
  - id: D-session-version22-1
    text: Freeze this targeted correction and hand off evidence; parent owns review disposition and future integration.
    depends_on: [O-session-version22-1]
    reversible: true
    reverse_if: Reviewer finds a contract defect or integrated intended-use observation contradicts this scope.
predictions:
  - id: P-session-version22-1
    kind: prospective
    created_at: 2026-09-30T12:31:43Z
    created_at_basis: Source snapshot timestamp, upper bound on PLAN recording.
    created_before_observation: true
    observable: PLAN P1-P5 native build/resource/error/x64 outcomes pass.
    acceptance: Exact original resource, unchanged frame on errors, basename-independent mappings, immutable receipts.
    failure_means: Repair prediction failed; preserve attempt and stop dependent work.
    oracle: A-session-version22-1
    oracle_version: source-v1
    artifact: A-session-version22-1
    environment: Native Windows VM, v120, C:/session-version22, original DLL hash in PLAN.md.
    status: passed
    status_history: [pending, passed]
    outcome_evidence: [E-session-version22-1]
outcomes:
  - id: OUT-session-version22-1
    state: passed
    evidence: [E-session-version22-1]
contradictions:
  - id: C-session-version22-1
    target: O-session-version22-0
    evidence: [E-session-version22-0]
    scope: General held-module identity inference from basename equality
    effect: narrow
    affected_ids: []
    disposition: repaired
    repaired_by: [P-session-version22-1]
    note: Revision21 remains unchanged and conditionally limited; parent independent review decides final finding disposition.
artifacts:
  - id: A-session-version22-1
    locator: source-v1.tar
    identity_method: sha256
    identity: 74edc78ad96434eb6daf44b584a66096c037462370cbba1f4e75059c67e4f01c
    mutable: false
    captured_at: 2026-09-30T12:31:43Z
    role: input
  - id: A-session-version22-2
    locator: evidence-v1/build-v1/receipt.json
    identity_method: sha256
    identity: b278f8582d5f5d6d4d77d3b8436403668f909a39331470d1f31e15b05c78e30e
    mutable: false
    captured_at: 2026-09-30T12:32:33Z
    role: evidence
  - id: A-session-version22-3
    locator: evidence-v1/runtime-v1/results.json
    identity_method: sha256
    identity: fe65820abe560d592c9304967809187b17273f01be8d3e01d7c54f83a82d000d
    mutable: false
    captured_at: 2026-09-30T12:32:57Z
    role: evidence
rehydration:
  status: complete
  losses: []
delivery_state: built
outcome_state: passed
highest_justified_claim: Supplied-held-module resource query matches original macro's actual 256-byte result and preserves checked owned x64 copying without basename resolution.
required_runtime_observation: Integrated live transport/client call and module-session lifetime/failure policy; none remains for planned component probes.
who_controls_next_test: Parent integration agent; senior23 independent review already in progress.
next_step: Parent reconciles senior23 review and chooses later live composition; no product adoption here.
END_POODO_CONTINUATION_V3_0
