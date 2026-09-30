#include <stdio.h>
#include <string.h>
struct Guarded { unsigned char before[8]; char path[512]; unsigned char after[8]; };
int main()
{
    char const *names[] = { "NPClient.dll", "NPClient64.dll" };
    unsigned checks = 0, failures = 0;
    for (unsigned name = 0; name != 2; ++name) {
        size_t const capacity = sizeof(Guarded().path) - strlen(names[name]) - 2;
        size_t const lengths[] = { 0, capacity - 1, capacity, capacity + 1 };
        for (unsigned sample = 0; sample != 4; ++sample) {
            Guarded g;
            memset(&g, 0xa5, sizeof(g));
            memset(g.path, 'x', lengths[sample]);
            // Model RegistryKey's explicit terminator after the returned bytes,
            // including a REG_SZ that did not contain a terminator itself.
            g.path[lengths[sample]] = 0;
            bool const accepted = strlen(g.path) <= capacity;
            if (accepted) { strcat(g.path, "\\"); strcat(g.path, names[name]); }
            ++checks; if (accepted != (sample != 3)) ++failures;
            ++checks; if (accepted && (strlen(g.path) != lengths[sample] + strlen(names[name]) + 1 || strcmp(g.path + lengths[sample] + 1, names[name]))) ++failures;
            for (unsigned i = 0; i != 8; ++i) { ++checks; if (g.before[i] != 0xa5 || g.after[i] != 0xa5) ++failures; }
        }
    }
    printf("checks=%u failures=%u expected=80\n", checks, failures);
    return failures || checks != 80;
}
