#include "file_channel.h"

namespace MilesFileChannel26
{
FileServices canonicalServices()
{
    FileServices services = {
        &ClientAudioFileCallbacks::open,
        &ClientAudioFileCallbacks::close,
        &ClientAudioFileCallbacks::seek,
        &ClientAudioFileCallbacks::read
    };
    return services;
}
}
