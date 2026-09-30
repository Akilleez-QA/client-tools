# Current integration snapshot

Immutable source base3c172d1b1 plus all working candidates captured in snapshot.json.
Includes13-path allocator-statistics candidate, Audio callback candidate, renderer
DxErr/source-dependency candidate and generated build settings. The exact snapshot
hashes20,533 tracked/candidate files; no __pycache or arbitrary scratch files added.

VM tree is Q:/repo mapped privately to C:/integration-current-v1/workspace.
Legacy relative outputs escaping the repo remain on private Q:, not old C:/dev or
C:/compile.268 evaluated project/config output audits run before product compilation.
Native tools: VS2013/v120, real Windows8.1SDK, DirectX June2010 C:/SDKs/DXSDK,
official SHA-pinned JPEG6b archive C:/allocator-next/jpegsrc.v6b.tar.gz, Python at
C:/ci-dpvs-review/python/python.exe. Renderer dependency builder builds real source;
no third-party replacement/stubs or SDK downloads are part of the run.

Order: ReleaseWin32, Releasex64, DebugWin32, Debugx64, sequential /m:2. Raw command
JSON, logs, exits and grouped diagnostics retained under VM results directory.
Previous C:/client-next-build and older evidence are never modified.

Status: snapshot verified; output audits underway. No new full-product pass/fail
claim yet. Parent owns source fixes/commits; this agent owns isolated build control.

Parent subsequently committed/pushed statistics as cf828 (reported by parent).
Active snapshot does not change. Parent is separately addressing a newly found
minimum-free-block invariant: untracked x64 tiny allocations may be48bytes while
a free node requires64. The old tracked probes use larger headers and do not
establish this untracked invariant. Finish this snapshot's matrix before a new
candidate; no targeted fault reproduction is part of this build lane.

## Completed immutable matrix

[
  {
    "configuration": "Release-Win32",
    "counts": {
      "Warning": 170,
      "Error": 0
    },
    "error_projects": []
  },
  {
    "configuration": "Release-x64",
    "counts": {
      "Warning": 4861,
      "Error": 24
    },
    "error_projects": [
      "Q:\\repo\\src\\external\\3rd\\library\\libMozilla\\build\\win32\\libMozilla.vcxproj"
    ]
  },
  {
    "configuration": "Debug-Win32",
    "counts": {
      "Warning": 219,
      "Error": 0
    },
    "error_projects": []
  },
  {
    "configuration": "Debug-x64",
    "counts": {
      "Warning": 4731,
      "Error": 27
    },
    "error_projects": [
      "Q:\\repo\\src\\engine\\client\\library\\clientAudio\\build\\win32\\clientAudio.vcxproj",
      "Q:\\repo\\src\\external\\3rd\\library\\libMozilla\\build\\win32\\libMozilla.vcxproj",
      "Q:\\repo\\src\\external\\ours\\library\\crypto\\build\\win32\\crypto.vcxproj"
    ]
  }
]

Win32 Debug preserves existing /FORCE project setting; no unresolved-symbol warnings observed. No x64 product linked. Direct source blockers: libMozilla x86-only SDK macro selection, crypto Debug packing warning treated as error, clientAudio Debug narrowing warnings treated as error. 268 output audits passed. Later minimum-free-block repair is not in this snapshot.

Current matrix explicitly excludes later minimum-free-block and TrackIR changes. No giant-allocation or product startup evidence claimed. Debug crypto C2220 is caused by STLport C4103 pack transitions. Debug clientAudio C2220 appears in two TUs with Archive.h:311 size_t narrowing plus local Audio preference/count narrowing warnings; these are separate source causes, not 27 independent roots.

Follow-up Mozilla proof now completed in a separate diagnostic phase: Win32 Release and Debug whole executables normalized equal after removing only browser explicit inputs and SwgClient scheduling dependency. See mozilla-link-proof-v2/comparison.json and member-extraction.json; no source modules deleted, other tools unchanged. Private files restored.
