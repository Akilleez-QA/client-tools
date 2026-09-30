# Combined77 source-only snapshot

Exact74 base plus75 Backend routing and76 scalar diagnostics; from74.patch and provenance.json specify the whole change. Backend is merged, not replaced by one overlay. Public header stays exact70; all other source files remain exact74 except the five76 target files (Backend includes both overlays). Frozen inputs are preserved.

The source inventory is now50 of62 public definitions. Twelve unresolved definitions remain: MSS_version, WAV_info, file_type, last_error, lock, register_EOS_callback, register_stream_callback, set_file_callbacks, set_named_sample_file, set_redist_directory, set_sample_file, unlock. Six stream controls and five borrowed sample controls now have outer host routing, but no host stream open/close/alias creation exists. EOS, file callback public/TLS adoption, locks, image/text ownership and normal paired shutdown still block operational adoption. A running-session scalar route is not a completed Audio install path.

No compiler/test/VM/link/runtime or product edit was performed. This snapshot does not incorporate an unreported74 compiler outcome and no next native runner is prepared. Portable decoder tests are a separate proposed gate using actual production bodies only, without SDK/runtime suppliers.
