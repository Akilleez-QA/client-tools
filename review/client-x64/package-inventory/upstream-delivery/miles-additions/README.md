# Miles source packages on master

These five proposed upstream branches contain only the new files from their previously reviewed incremental fork packages. Contracts are submitted in upstream client PR41. Every patch and introduced Git blob is identical to its reviewed counterpart; existing game source, build selection and workflow files are unchanged.

The branches target maintained master so each upstream review shows only its own additions. They require predecessor modules to compile; independent base branches do not remove those dependencies. They remain drafts until their dependencies are available. Existing native/provider/test observations apply to their recorded integrated configurations, not to these incomplete standalone source closures.

A local merge of contracts and all five additions completed without conflicts. Its whole Git tree is `b913a8b4f09d48e9c5331bba33032d6f5008ed22`, identical to the reviewed pipe-session head `3430934cedf230e7c5c2a77ae8b9e6f607fb1fe8`. This verifies source composition only; no executable was built or run for this packaging check. The verification merge branch is local and is not proposed for upstream.

The five preflights record master base, new and reviewed heads, exact commits, source/test counts and all introduced blobs. `composition.json` records the acceptance condition and result.
