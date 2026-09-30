#include "LiveChannel.h"
#include "../../live-bridge-candidate/common.h"

namespace {
std::string frameDigest(const std::vector<unsigned char> &frame) {
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    require(CryptAcquireContextA(&provider, 0, 0, PROV_RSA_AES, CRYPT_VERIFYCONTEXT) != 0,
            "reply hash provider");
    require(CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash) != 0, "reply hash");
    require(CryptHashData(hash, &frame[0], static_cast<DWORD>(frame.size()), 0) != 0,
            "reply hash bytes");
    unsigned char digest[32];
    DWORD size = 32;
    require(CryptGetHashParam(hash, HP_HASHVAL, digest, &size, 0) != 0 && size == 32,
            "reply digest");
    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    std::string text;
    const char hex[] = "0123456789abcdef";
    for (unsigned i = 0; i != 32; ++i) {
        text += hex[digest[i] >> 4];
        text += hex[digest[i] & 15];
    }
    return text;
}

class LiveChannel : public ClientMilesPipe::Channel {
  public:
    LiveChannel(const char *hostExecutable, const char *originalDll) : next_(0) {
        std::string random = nonce();
        std::string base = "\\\\.\\pipe\\swg-facade24-" + random;
        std::string commandName = base + "-cmd", callbackName = base + "-cb";
        PSECURITY_DESCRIPTOR descriptor = userDescriptor();
        SECURITY_ATTRIBUTES attributes = {sizeof attributes, descriptor, FALSE};
        ServerPipe command(commandName, attributes), callback(callbackName, attributes);
        LocalFree(descriptor);
        char pid[32];
        sprintf_s(pid, "%lu", GetCurrentProcessId());
        std::string args = "\"" + std::string(hostExecutable) + "\" --host " + commandName + " " +
                           callbackName + " " + random + " " + pid + " \"" + originalDll + "\"";
        std::vector<char> line(args.begin(), args.end());
        line.push_back(0);
        child_.create(hostExecutable, &line[0]);
        child_.assignAndResume(child_.job);
        command.connected();
        callback.connected();
        ULONG actual = 0;
        require(GetNamedPipeClientProcessId(command.pipe, &actual) &&
                    actual == child_.info.dwProcessId,
                "child command PID binding");
        require(GetNamedPipeClientProcessId(callback.pipe, &actual) &&
                    actual == child_.info.dwProcessId,
                "child callback PID binding");
        command_.reset(new Endpoint(command.take(), 23));
        callback_.reset(new Endpoint(callback.take(), 29));
        StartupBridge::OwnedReply hello =
            exchange(MilesWire::Hello, MilesWire::Call(),
                     MilesTransport::Bytes(random.data(), random.size()), MilesTransport::Bytes());
        require(hello.result.transport_status == StartupBridge::Success, "Hello accepted");
    }

    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                   MilesTransport::Bytes text) override {
        // Known validated refusals reach the facade; only fixture probes compare
        // an expected status. Do not inherit Client.call's default-success throw.
        return exchange(opcode, fields, MilesTransport::Bytes(), text);
    }

    void finish() override {
        drainSession(*command_, *callback_, true);
        require(WaitForSingleObject(child_.info.hProcess, 10000) == WAIT_OBJECT_0,
                "host exit wait");
        DWORD code = 99;
        require(GetExitCodeProcess(child_.info.hProcess, &code) && code == 0, "host clean exit");
        child_.close();
    }

  private:
    ChildProcess child_;
    std::unique_ptr<Endpoint> command_, callback_;
    uint64_t next_;

    StartupBridge::OwnedReply exchange(uint32_t opcode, const MilesWire::Call &fields,
                                       MilesTransport::Bytes payload, MilesTransport::Bytes text) {
        MilesWire::Header header = {};
        header.magic = MilesWire::Magic;
        header.version = MilesWire::Version;
        header.kind = MilesWire::Request;
        header.opcode = opcode;
        header.request = ++next_;
        header.lane = 1;
        std::vector<unsigned char> frame;
        require(MilesTransport::encodeCall(header, fields, payload, text, frame), "encode call");
        require(command_->send(bytes(frame)), "send call");
        frame = receive(*command_, callback_.get(), opcode == MilesWire::SessionClose);
        std::vector<unsigned char> unexpected;
        require(!callback_->takeFrame(unexpected), "no callback traffic");
        StartupBridge::OwnedReply out;
        require(StartupBridge::decodeReply(bytes(frame), header, out), "typed reply/context");
        printf("reply request=%I64u opcode=%u status=%u bytes=%u sha256=%s return_bits=%u "
               "value3=%u null_mask=%u text_hex=",
               next_, opcode, out.result.transport_status, static_cast<unsigned>(frame.size()),
               frameDigest(frame).c_str(), out.result.return_bits, out.result.value[3],
               out.result.null_mask);
        if (out.text.empty())
            printf("-");
        else
            for (size_t i = 0; i != out.text.size(); ++i)
                printf("%02x", static_cast<unsigned>(out.text[i]));
        puts("");
        return out;
    }
    LiveChannel(const LiveChannel &);
    LiveChannel &operator=(const LiveChannel &);
};
} // namespace

namespace ClientMilesPipe {
std::unique_ptr<Channel> connect(const char *hostExecutable, const char *originalDll) {
    return std::unique_ptr<Channel>(new LiveChannel(hostExecutable, originalDll));
}
} // namespace ClientMilesPipe
