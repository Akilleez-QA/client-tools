#!/usr/bin/env python3
"""Create only private source snapshots and patches; no product mutation/compiler."""
from pathlib import Path
import difflib, hashlib, json, subprocess
ROOT = Path(__file__).resolve().parent
PRODUCT = Path('/home/akilleez/Work/swg-source/client-build-next')
SEAM = ROOT.parent / 'reverse-file-seam20'
COMMIT = '49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
AUDIO = 'src/engine/client/library/clientAudio/src/win32/Audio.cpp'
HEADER = 'src/engine/client/library/clientAudio/src/win32/ClientAudioFileCallbacks.h'
PUBLIC = 'src/engine/client/library/clientAudio/include/public/clientAudio/ClientAudioFileCallbacks.h'
PATHS = [AUDIO, HEADER, PUBLIC]
def digest(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git', '-C', str(PRODUCT), *args])
assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
original = git('show', COMMIT + ':' + AUDIO)
assert (PRODUCT / AUDIO).read_bytes() == original
assert digest(original) == 'c729174ada8104331702422879ecbfa4986a6c4bba49bc3d763ab62a2e401406'
base = ROOT / 'baseline'
(base / AUDIO).parent.mkdir(parents=True, exist_ok=True)
(base / AUDIO).write_bytes(original)
seam = ROOT / 'seam20'
(seam / AUDIO).parent.mkdir(parents=True, exist_ok=True)
(seam / AUDIO).write_bytes(original)
assert not (seam / HEADER).exists(), 'Use a fresh output directory; source already prepared'
subprocess.run(['git', 'apply', '--check', str(SEAM / 'Audio-file-callbacks.patch')], cwd=seam, check=True)
subprocess.run(['git', 'apply', str(SEAM / 'Audio-file-callbacks.patch')], cwd=seam, check=True)
text = (seam / AUDIO).read_text()
TLS = '\tif (once && !Os::isMainThread())\n\t{\n\t\tonce = false;\n\t\tPerThreadData::threadInstall(false);\n\t}\n\n'
COMMON_COMMENT = '// Shared file operations only. Callers own TLS admission and serialization.\n'
checks = {}
for stem, result, args in [('Open','U32','fileName, fileHandle'), ('Close','void','fileHandle'), ('Seek','S32','fileHandle, offset, type'), ('Read','U32','fileHandle, buffer, bytes')]:
    name = 'file' + stem + 'CallBack'
    common = 'file' + stem + 'Common'
    start = text.index(result + ' __stdcall ' + name + '(', text.index('static int once = true;'))
    end = text.index('\n//-----------------------------------------------------------------------------', start)
    block = text[start:end]
    signature, remainder = block.split('\n{\n', 1)
    assert remainder.count(TLS) == 1
    prefix, body = remainder.split(TLS)
    common_signature = 'static ' + signature.replace('__stdcall ', '').replace(name, common)
    # Everything after the legacy TLS block is copied verbatim, including the
    # closing brace and comments/disabled code in the operation body.
    extracted = COMMON_COMMENT + common_signature + '\n{\n' + body
    invoke = ('\t' if result == 'void' else '\treturn ') + common + '(' + args + ');\n}\n'
    trampoline = signature + '\n{\n' + prefix + TLS + invoke
    text = text[:start] + extracted + '\n//-----------------------------------------------------------------------------\n' + trampoline + text[end:]
    # Namespace wrappers occur later in the source, independent of SDK names.
    adapter_start = text.index('ClientAudioFileCallbacks::OpenResult ClientAudioFileCallbacks::open')
    text = text[:adapter_start] + text[adapter_start:].replace(name + '(', common + '(')
    checks[stem] = {'operation_body_sha256': digest(body.encode()), 'legacy_prefix_sha256': digest((prefix + TLS).encode())}
text = text.replace('// the original callback bodies and their single AudioNamespace file map.', '// the shared operation bodies and their single AudioNamespace file map.\n// Admission guarantees installed engine TLS; these calls bypass legacy TLS setup.')
header = (seam / HEADER).read_text().replace('// The coordinator must first establish engine/TLS lifetime, compatible thread\n// context, serialization with ALL original file callbacks, and operation pins.\n// This interface neither installs threads nor schedules callbacks. It must not', '// The caller must have known, already-installed engine TLS and hold engine/file\n// lifetime and operation pins. Calls bypass the SDK callbacks\' legacy TLS setup.\n// The coordinator must serialize these calls with ALL original file callbacks;\n// this interface supplies no concurrency guarantee, lock, or admission check.\n// It neither installs threads nor schedules callbacks. It must not')
header = header.replace('// Original callback alone closes/deletes.', '// Shared original operation alone closes/deletes.')
candidate = ROOT / 'candidate'
for path, content in [(AUDIO,text),(HEADER,header),(PUBLIC,(seam/PUBLIC).read_text())]:
    (candidate/path).parent.mkdir(parents=True, exist_ok=True)
    (candidate/path).write_text(content)
for filename, old in [('Audio-file-executor.patch',base), ('Audio-file-executor-from-seam20.patch',seam)]:
    chunks=[]
    for path in PATHS:
        before=(old/path).read_text() if (old/path).exists() else ''
        after=(candidate/path).read_text()
        chunks.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+path if before else '/dev/null',tofile='b/'+path))
    (ROOT/filename).write_text(''.join(chunks))
(ROOT/'ClientAudioFileCallbacks.h').write_text(header)
manifest={'product_commit':COMMIT,'original_audio_sha256':digest(original),'operation_identity':checks,'sha256':{}}
for folder in [base,seam,candidate]:
    for path in PATHS:
        p=folder/path
        if p.exists(): manifest['sha256'][str(p.relative_to(ROOT))]=digest(p.read_bytes())
for name in ['Audio-file-executor.patch','Audio-file-executor-from-seam20.patch','ClientAudioFileCallbacks.h','prepare-source.py']:
    manifest['sha256'][name]=digest((ROOT/name).read_bytes())
(ROOT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Private source and two patches prepared; no product changes or compilation.')
