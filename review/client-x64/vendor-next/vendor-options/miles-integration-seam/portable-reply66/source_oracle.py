"""Source-order sensor only, no claim of executing real LiveChannel."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent
text=(root/'LiveChannel64-source-only.cpp').read_text()
start=text.index('StartupBridge::OwnedReply exchange(')
body=text[start:text.index('LiveChannel(const LiveChannel &)',start)]
checks={
 'dedicated_install_decode_before_owner':body.index('decodeInstallReply(')<body.index('replyOwner->validateReply('),
 'generic_decode_before_owner':body.index('StartupBridge::decodeReply(')<body.index('replyOwner->validateReply('),
 'owner_before_returned':body.index('replyOwner->validateReply(')<body.index('runtime_->returned('),
 'one_returned_site':body.count('runtime_->returned(')==1,
 'failure_requests_fail':'catch(...){runtime_->fail();throw;}' in body,
 'hello_excluded':'if(opcode!=MilesWire::Hello){' in body,
 'actual_session_supplies_self':'verifiedResources(fields), *this)' in (root/'tree/backend-boundary24/pipe/ClientMilesPipe.cpp').read_text(),
}
print(json.dumps({'scope':'text order oracle, not execution or CFG proof','checks':checks},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
