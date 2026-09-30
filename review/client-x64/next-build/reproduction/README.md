# Native diagnostic recipes

These scripts retain the tested Windows VM paths and require VS2013/v120, repository sources and the real referenced libraries. They are not a portable installer or a hosted CI job. Read ../RESULTS.md before interpreting a probe.

The UI formatter runtime probe did not link; it is retained as a failed experiment, not an acceptance test that passed. Socket tests exercise real headers and native APIs, not the entire game networking lifecycle. Memory tests compile the actual translation unit but do not run the allocator. The memmove probe reproduces the helper contract separately; the native product build is separate evidence.
