# Parent reply-boundary result

A fresh Linux C++11 build of the worker's actual OwnedReply decoder, original codec and SessionVersion consumer passes23 behavior/preservation assertions plus one exact-count guard (24/24) under ASan/UBSan, with no diagnostics. Checked source/header hashes before and after match in inputs-before.json/inputs-after.json. This was independent fixture authorship, not independent vendor execution.

Covered: owned text after encoded-frame replacement, cleared borrowed spans, null versus empty text, incorrect pending request/lane, ambiguous status4, embedded or missing final NUL, unexpected scalar/resource outputs, nonempty error response, and unknown null-mask bits. Every rejected reply leaves pre-existing destination scalar/text untouched.

A copied-header mutation that admits status4 compiles, then exits1 at exactly `unknown ambiguous status rejected`. The worker header was not changed. mutation-result.json records the control. These observations bind to the recorded header hash; later edits need assessment before transferring this result.

No Windows build, vendor load, audio/engine execution or complete transport result is claimed. The only initial tooling error was attempting to launch a command in a directory before it existed; no files or tests ran from that rejected launch. The subsequent authored build and its first execution passed. No workload was retried after a behavioral failure.
