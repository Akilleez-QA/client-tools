Independent bounded source review test plan:
- Compile actual prepared ResourceRegistry header with standard portable C++11.
- Check reserve/publish/cancel, null publication, foreign registry rejection, 64 slot reuse cycles, parent isolation/retirement, and finite generation exhaustion.
- Verify frozen manifest hashes and archive members match prepared files.
- Do not compile fake SDK, execute Backend/vendor/host/VM/engine, modify frozen inputs, or use broad fault injection.
