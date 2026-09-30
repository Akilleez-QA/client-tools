#ifndef MILES_HOST_RETAINED_BUFFERS_H
#define MILES_HOST_RETAINED_BUFFERS_H
#include <stdint.h>
#include <stddef.h>
#include <map>
#include <vector>
namespace MilesHost {
// One dispatch-thread-owned store per resource. No vendor lifecycle is inferred.
// Before retire/destruction, caller must establish no vendor/callback references.
// A successful commit alone is NOT evidence the previous vendor reference ended.
// Tokens are process-local identifiers, never pointers or cross-process authority.
class RetainedBuffers {
public:
    typedef uint64_t Token;
    enum Kind { Binary, Text, NullText };
    struct View { Kind kind; const unsigned char *data; uint32_t size; };
    RetainedBuffers(size_t byteLimit, size_t entryLimit);
    bool stage(Kind kind, const void *frame, size_t frameSize,
               size_t offset, size_t length, Token &out);
    bool view(Token token, View &out) const;
    bool commit(Token token); // No allocation; never retires the previous copy.
    bool retire(Token token); // Active token is protected; caller proves quiescence.
    void deactivate(); // Caller proves active vendor reference has ended.
    Token active() const { return activeToken; }
    size_t bytes() const { return used; }
private:
    struct Entry { Kind kind; std::vector<unsigned char> bytes; };
    typedef std::map<Token, Entry> Entries;
    Entries entries;
    size_t limit, maxEntries, used;
    Token activeToken;
    RetainedBuffers(const RetainedBuffers &);
    RetainedBuffers &operator=(const RetainedBuffers &);
};
}
#endif
