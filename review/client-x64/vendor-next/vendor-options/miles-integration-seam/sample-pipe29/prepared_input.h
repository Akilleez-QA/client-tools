#ifndef SAMPLE_PIPE28_PREPARED_INPUT_H
#define SAMPLE_PIPE28_PREPARED_INPUT_H
#include "../buffer-upload-candidate/buffer_upload.h"
#include "../host-candidate/retained_buffers.h"
#include <stdexcept>
#include <cstring>

namespace SamplePipe28 {
// Preparation only: neither a bind operation nor a vendor retirement policy.
// Views remain valid while this owner exists. A future binder must establish
// when ALL vendor references end before destroying it, including failed binds.
class PreparedInput {
    MilesHost::RetainedBuffers storage;
    MilesHost::RetainedBuffers::Token imageToken, suffixToken;
public:
    PreparedInput(const MilesHost::BufferUpload &upload, const char *suffix, size_t limit)
        : storage(limit, 2), imageToken(0), suffixToken(0) {
        if (!suffix) throw std::invalid_argument("null suffix");
        size_t n=0;
        while (n<512 && suffix[n]) ++n;
        if (n==512) throw std::invalid_argument("suffix limit");
        if (upload.size()>limit || n+1>limit-upload.size())
            throw std::length_error("image/suffix aggregate budget");
        std::vector<unsigned char> bytes;
        if (!upload.copySealed(bytes) || bytes.empty())
            throw std::invalid_argument("nonempty sealed upload required");
        if (!storage.stage(MilesHost::RetainedBuffers::Binary, &bytes[0], bytes.size(),
                           0, bytes.size(), imageToken) ||
            !storage.stage(MilesHost::RetainedBuffers::Text, suffix, n+1, 0, n+1, suffixToken))
            throw std::length_error("retained preparation budget");
    }
    MilesHost::RetainedBuffers::View image() const {
        MilesHost::RetainedBuffers::View out;
        if (!storage.view(imageToken, out)) throw std::logic_error("missing image");
        return out;
    }
    MilesHost::RetainedBuffers::View suffix() const {
        MilesHost::RetainedBuffers::View out;
        if (!storage.view(suffixToken, out)) throw std::logic_error("missing suffix");
        return out;
    }
private:
    PreparedInput(const PreparedInput &);
    PreparedInput &operator=(const PreparedInput &);
};
}
#endif
