# Portable result

V2 passed: 1267 scripted-framed seven-operation checks; 202 existing backend24 checks; fixed stereo/fresh-observations sample check. All executed code was authored portable test code with ASan/UBSan. The expected negative link failed on absent ClientMiles::set_file_callbacks, showing that pipe callback registration has no success stub.

Request/reply codecs and the staged decoder were used. Frozen input source hashes and authored patch/check-script identities stayed unchanged. No vendor or native Windows execution occurred. Host dispatcher reuse is source-only pending a separate native compile gate. See PLAN.md for remaining integration limits and independent patch boundaries.
