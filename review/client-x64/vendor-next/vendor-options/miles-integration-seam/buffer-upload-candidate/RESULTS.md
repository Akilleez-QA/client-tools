# Upload assembly mechanism

Current source passes29checks under nativev120 Win32/x64 Debug/Release (/W4 /WX) and parent ASan/UBSan. In every native configuration, the premature-seal mutant builds and exits1 as required. Exact native source hashes match the current implementation/header/tests; source hash path separators were normalized only for manifest lookup. The first collector stopped after all successful runs because Windows manifest keys use backslashes; no tests were rerun to repair that collector.

Historical first build failed /WX on test macro do/while(0), C4127; preserved under history-v1. Test helper was made a function plus if macro; implementation unchanged. No vendor DLL, game allocator or device executed. Both owned native scratch directories were removed after logs/hash checks.

The component requires exact sequential coverage, seals only complete uploads and publishes a separate owned byte vector. A test assembles an image larger than1MiB from frame-bounded chunks; this is assembly evidence, not a tested actual wire handler. Caller-validated input spans, session identity, registry ownership and aggregate accounting are external requirements. Copying temporarily duplicates input and must be budgeted. An empty or sealed image is not proof of valid media. No production integration or fidelity result.
