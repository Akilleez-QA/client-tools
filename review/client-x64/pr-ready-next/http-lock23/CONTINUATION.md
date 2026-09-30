POODO_CONTINUATION_V3_0
schema: POODO_CONTINUATION/3.0
capsule_id: PC-http23-handoff-1
revision: 1
parent_capsule: null
generated_at: '2026-09-30T12:58:22.127201+00:00'
objective: Prepare an independently reviewable local HTTP lock x64 candidate serving the parent's full-client goal.
acceptance:
  - id: AC-http23-1
    criterion: Isolated upstream-based commit with a real-header native recursion, exclusion, release and payload matrix plus stock and broken controls.
authority:
  allowed: Own local branch, fixture, native VM lock checks and evidence packet.
  prohibited: Push, PR, integration branch edits, engine/audio/allocator fault workloads or owner-field race redesign.
constraints: Preserve base 949451032647e45e42c3aaef3f41b132c8af36e3; use C:/http-candidate23 only; no descendant capacity assigned.
user_directives: Parent delegation requests a small commit and packet for later blind review; full-client conversion remains the parent objective.
current_head: D-http23-1
claims:
  - id: O-http23-1
    state: observed
    status: active
    text: Final actual-header matrix meets every predeclared native behavior and control outcome.
    source_type: artifact
    locator: results-v2/results.json and each lane's build.log/run.log
    observed_at: '2026-09-30'
    freshness: immutable final receipt
    evidence_family: EF-http23-native-v120
    rehydration_status: verified
    supports: [AC-http23-1]
    limits: Single VM and author-owned fixture; no full-TU scheduler, HTTP integration or race-freedom proof.
evidence_bundles:
  - id: E-http23-1
    request: Native VS2013 compile/run of real VeCritsec.hpp with unmodified upstream FoundationTypes in four configurations and four baseline/two mutation lanes.
    material_inputs: [pretest-manifest-v2.json, tools/test-http-lock/probe.cpp, tools/test-http-lock/run.py]
    result_or_locator: results-v2/
    completeness: complete
    artifacts: [A-http23-1]
    supports_claims: [O-http23-1]
orientations:
  - id: OR-http23-1
    text: x64-only intrinsics remove the assembly compile barrier at the header surface without an integration prerequisite.
    depends_on: [E-http23-1]
    confidence: {artifact_identity: high, test_path: high, causal_model: high, outcome: high}
    strongest_rival: H-http23-1
alternatives:
  - id: H-http23-1
    status: bounded
    text: Surrounding integration prerequisites might make the fix inseparable.
    discriminator: Base header/cpp match integration parent; clean real-header matrix runs, while whole-project dependency claims remain excluded.
decisions:
  - id: D-http23-1
    text: Hand off the clean local commit and evidence to the parent for blind review.
    depends_on: [O-http23-1]
    reversible: true
    reverse_if: Review or reproduction finds a regression or unmet component oracle.
predictions:
  - id: P-http23-1
    kind: prospective
    created_at: '2026-09-30T12:53:10.508298Z'
    created_before_observation: true
    observable: Candidate matrix and stock Win32 pass 27 checks; stock x64 fails C4235; no-acquire/no-release fail their named checks.
    acceptance: All ten expected lane outcomes; 10 s event waits, 45 s run deadlines, 120 s compile deadlines.
    failure_means: Component readiness is not established for the failed lane; retain raw evidence and investigate.
    oracle: A-http23-oracle
    oracle_version: v1, unchanged behavioral criterion through final runner v2
    artifact: A-http23-1
    environment: Native Windows VM; MSVC 18.00.40629/v120; Python 3.12.10; explicit /volatile:ms.
    status: passed
    status_history: [pending, passed]
    outcome_evidence: [E-http23-1]
outcomes:
  - id: OUT-http23-1
    text: Four candidate lanes and two stock Win32 lanes pass; two stock x64 compile failures and both specific mutation failures observed.
contradictions: []
artifacts:
  - id: A-http23-1
    locator: /home/akilleez/Work/swg-source/client-http-candidate23
    identity_method: git_commit
    identity: 283f6bffb9b5db76e4fd15bca922b8bedeedf8c8
    mutable: false
    captured_at: '2026-09-30'
    role: output
  - id: A-http23-oracle
    locator: input.zip member POODO.md, Prospective oracle v1
    identity_method: sha256
    identity: 2bb0bdc8f5d8a0f77a91efd889e8d3fbbe1fe90d2f83cda119554253bbec5177
    mutable: false
    captured_at: '2026-09-30T12:53:10.508298Z'
    role: input
rehydration:
  status: complete
  losses: []
delivery_state: built
outcome_state: passed
highest_justified_claim: Native v120 actual-header trylock/unlock matrix and discriminating controls passed within the documented MSVC scope.
required_runtime_observation: None for this component matrix; production lock/yield_thread, full HTTP and full client remain outside the fixture.
who_controls_next_test: parent agent
next_step: Parent performs blind review of the commit and packet before deciding any remote action.
END_POODO_CONTINUATION_V3_0
