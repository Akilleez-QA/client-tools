# Retain inserted FileManifest entries until removal

A successful manifest insertion transfers the new entry to the map, but both insertion paths deleted it immediately. The recording path also deleted duplicate candidates twice. Keep successful entries alive for the existing removal path, and delete only rejected duplicate candidates.

One source commit on master `949451032647e45e42c3aaef3f41b132c8af36e3`: `FileManifest.cpp`, +2/−2. No configuration, x64 or media-bridge prerequisite; the original two-site patch is unchanged.

The [original repair record](https://github.com/Akilleez-QA/client-tools/commit/4953206a26de0b46221693e900eaa59b93297a98) documents the actual product close failure in FileManifest entry destruction, successful Debug-x64/Release-Win32 sharedFile builds and the subsequent normal product exit. Its first compositor failure and six remaining narrowing warnings are retained limitations, not hidden passes. These observations used the integrated development product under Proton, not an isolated master-based build or native Windows qualification.

No builds or runtime were repeated during packaging. The change repairs this ownership error; it does not establish general manifest thread safety, CRC collision behavior or whole-client heap safety.
