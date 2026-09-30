# Prospective v2 dependency completion

V1 is a failed gate, not invalid evidence: GCC compilation reached link, which failed with undefined MilesStartup::signedValue references from actual ClientMilesPipe.cpp. The test did not run. V1 source, manifest, runner and raw portable-evidence-v1 remain unchanged; hashes are recorded in composition-provenance-v2.json.

V2 adds exactly the real unchanged stream-native38/private-source-v1/startup-metadata-v4/metadata_wire.cpp to the 24-source/header v1 tree and translation-unit list. Its only quoted include is metadata.h; this dependency already exists in v1 and matches38 byte for byte. No replacement definition, section garbage collection, weakened flags, source/test changes or protocol changes. All existing v1 composition files copy byte-for-byte, including Version2 selection evidence.

The v2 runner differs only in four private manifest/evidence/source/provenance path labels, as shown in runner-v2.patch. Exact same strict sanitizer/pthread compile/run and first-failure rules. Seven translation units, no SDK inputs. Parent must review the v2 freeze before authorizing one new attempt. No compiler/test has run for v2.
