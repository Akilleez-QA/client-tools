# Independent review — FileManifest entry ownership

No introduced blocker found. Reviewed master 949451032647e45e42c3aaef3f41b132c8af36e3 to 514498397a9ead2518ab11d5894a785ef877b82d by explicit refs: one file, +2/−2. Candidate SHA-256 matches the receipt and changed lines exactly match original 4953206a26de0b46221693e900eaa59b93297a98.

Both insertion functions put an allocated FileManifestEntry pointer into s_manifest. On successful insertion the map must retain that pointer until remove traverses and deletes it. addNewManifestEntry already deletes the rejected duplicate inside its failure branch; removing the unconditional second delete fixes both the successful-insertion dangling pointer and duplicate double-delete. addStoredManifestEntry now deletes only its rejected candidate, leaving the existing map entry untouched. Access-count and replacement-size updates operate through insertReturn.first as before. Deleting a rejected candidate does not invalidate the map iterator because that candidate was never inserted.

The existing removal paths delete retained entries and null their mapped pointers. This repair does not redesign map reuse after removal, exceptional insertion cleanup, CRC identity or concurrent access; those existing limitations are not introduced blockers. No x64, configuration or media dependency is needed for the ownership correction.

I read the original repair commit record. It supports the stated sharedFile builds and integrated product close observation under GE-Proton, while explicitly retaining the compositor failure after game exit and six narrowing warnings. The PR does not claim a clean whole-harness run, isolated master build, native Windows qualification or whole-client heap safety. Its bounded evidence wording is appropriate.

Only this report was written. No source edits, tests, builds, runtime, remote actions or descendant agents. Public URL reachability was not rechecked.
