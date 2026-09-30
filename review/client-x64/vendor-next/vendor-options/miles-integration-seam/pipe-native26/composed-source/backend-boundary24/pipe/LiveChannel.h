#ifndef CLIENT_MILES_PRIVATE_LIVE_CHANNEL_H
#define CLIENT_MILES_PRIVATE_LIVE_CHANNEL_H
#include "Channel.h"
#include <memory>

namespace ClientMilesPipe {
// Composition root only. Creates the existing private pipes/process and performs
// Hello. Public ClientMiles.h has no process configuration or bootstrap calls.
std::unique_ptr<Channel> connect(const char *hostExecutable, const char *originalDll);
} // namespace ClientMilesPipe
#endif
