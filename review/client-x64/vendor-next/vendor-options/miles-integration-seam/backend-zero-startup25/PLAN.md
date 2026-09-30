# Pure zero-startup observation 25

Before implementation, 2026-09-30. Parent explicitly requests a separate test-only supplement using frozen backend-boundary24 without source changes. This is the zero-result branch selected in backend-live25/PLAN.md; the same research/20-path preparation gate applies. No vendor, Wine, native executable, engine, allocator fault or SDK substitute is involved.

Prediction: a scripted, structurally valid startup reply with return_bits0 is returned as0. Current facade state remains started=false/stopped=false. Calling shutdown and private Session.close produces WrongState with no additional channel request. finish is not called, and scope destruction destroys the test channel. Capture source/compiler hashes, command and result; preserve any first failure. This demonstrates the current known missing graceful-close path only. It neither fixes the path nor establishes what the real SDK should do after startup0.
