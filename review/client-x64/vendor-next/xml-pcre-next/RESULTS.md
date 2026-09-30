# Genuine PCRE/libxml native provider spike

2026-09-30. No production edits, commits, mappings or provider stubs. Scratch native v120 builds only. Root diagnosis: inherited libpcre.a and libxml2-win32-release.lib are x86 providers; x64 unresolved names cannot be satisfied by them. sharedRegex uses PCRE_STATIC and wants direct pcre_malloc/free. sharedXml deliberately has DLL-mode XML declarations, including imported xmlFree data; keeping an authentic DLL/import provider avoids an unnecessary static consumer policy change.

## Source identity

PCRE4.1 from official project's SourceForge release URL https://downloads.sourceforge.net/project/pcre/pcre/4.1/pcre-4.1.tar.gz SHA2569ac01a6c5763120732c560ac26890c79c6ec0f8df4f5d42c2a6f0cae50c25575. Its pcre.in differs from repo public pcre.h only by the three expected version substitutions. This archive hash records download identity; no independent signed digest was available in this experiment.

libxml2 2.6.7 from GNOME https://download.gnome.org/sources/libxml2/2.6/libxml2-2.6.7.tar.gz SHA256785dec9ef48babf65f06c2dd98d6ef2ab2da09259af8f41c913c014046d5a39b, verified against adjacent official .sha256sum.43 public headers match repo after newline normalization; xmlversion.h is generated feature configuration. Repository's other complete libxml source is2.4.28 and was NOT substituted. Licenses retained in original extracted archives.

## Builds and negative discoveries

PCRE genuine source static archive:4/4 Win32/x64 Release/Debug native compile/archive/test success. Uses upstream NON-UNIX-USE recipe, generated C-locale tables, /MT or/MTd, PCRE_STATIC, HAVE_CONFIG_H, upstream POSIX_MALLOC_THRESHOLD10. Initial v1 omitted this makefile-configured threshold and failed compiler; retained. Initial v2 default omitted UTF8, and was rejected after a **real stock Win32 archive probe** reported UTF8=1. Final v3 adds SUPPORT_UTF8 and reports version4.1, newline10, link-size2, UTF8=1 exactly like stock. Production Win32 provider is unchanged.

XML genuine source DLL/import library:4/4 native builds. Uses repo's original libxml-configure-win32.bat feature options and CRT choices. The historical /OPT:NOWIN98 is unsupported by v120 linker; scratch v3 removes only that option from upstream Makefile.msvc. Earlier command quoting/v2 Release failures retained. Debug feature configuration matches repo header; Release differs solely by the original batch's xml_debug=no/mem_debug=no vs bundled Debug-generated header (LIBXML_DEBUG_ENABLED, DEBUG_MEMORY_LOCATION). No feature option invented to make the build green.

## Runtime checks and limits

Final combined probe compile/link/run4/4 exits0 against genuine providers: installs PCRE malloc/free hooks, compiles and matches an ordinary capture expression, verifies hooks used; installs XML allocator callbacks, parses a small document, reads root, dumps and xmlFree's buffer, creates a document/root/property/text child and cleans up. Also runs against original Win32 PCRE archive in both CRT configurations to query actual baseline features. No game shutdown, whole-client XML/regex acceptance or complete API/configuration equivalence claimed.

PCRE upstream testinput1 output matches supplied testoutput1 on all4 builds, with CRLF→LF normalization only. It includes original high-byte test data; runner's first attempt incorrectly decoded as cp1252 and was repaired to binary comparison, retaining failure. Other upstream test files and UTF8-specific runtime corpus remain unrun; query proves compiled feature availability, not all UTF8 behavior.

Provider paths for exact isolated link replay:
- C:/pcre-native-v3/amd64-{Release,Debug}/pcre-4.1/pcre.lib
- C:/xml-pcre-next-v3/amd64-{Release,Debug}/libxml2-2.6.7/win32/bin.msvc/libxml2.lib plus real libxml2.dll there.

Native evidence.zip contains logs/configs/hashes, not generated binaries. Full product link replay remains build worker's separate evidence. Production reproducible builder integration is still a proposal, not implemented; must preserve pinned sources/configuration, runtime XML DLL deployment and unchanged Win32 inputs.
