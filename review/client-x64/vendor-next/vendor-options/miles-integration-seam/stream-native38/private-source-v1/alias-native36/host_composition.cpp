// Object-only anchor for the actual staged host composition. No entry point,
// vendor substitute, callback fixture or runtime invocation is supplied.
#include "../live-bridge-candidate/common.h"
#include "../startup-bridge23/backend.h"
#if !defined(_M_IX86) || _MSC_VER != 1800
#error The original-vendor host composition requires actual v120 x86.
#endif
StartupBridge::OwnedReply compileHostComposition36(Backend &backend,
                                                  MilesWire::Header const &header,
                                                  MilesWire::Call const &call,
                                                  std::vector<unsigned char> const &frame) {
    return backend.execute(header, call, frame);
}
