// Link against the newly built real ui.lib. No substitute stream/report objects.
#include <cstdio>
#include <climits>
#include <cstring>
#include "_precompile.h"
#include "UIOutputStream.h"

int main()
{
    FILE *existing = fopen("ui.log", "rb");
    if (existing) {
        fclose(existing);
        fprintf(stderr, "FAIL run in a new empty directory; ui.log already exists\n");
        return 2;
    }
    size_t values[5];
    char const *expected[5];
    unsigned count = 0;
    values[count] = 0; expected[count++] = "0\n";
    values[count] = static_cast<size_t>(INT_MAX); expected[count++] = "2147483647\n";
    values[count] = static_cast<size_t>(UINT_MAX); expected[count++] = "4294967295\n";
#ifdef _WIN64
    values[count] = static_cast<size_t>(0x100000001ULL); expected[count++] = "4294967297\n";
    values[count] = static_cast<size_t>(-1); expected[count++] = "18446744073709551615\n";
#else
    values[count] = static_cast<size_t>(-1); expected[count++] = "4294967295\n";
#endif
    {
        UIOutputStream output; // actual constructor opens ui.log
        for (unsigned i = 0; i < count; ++i)
            output << values[i] << '\n'; // explicitly size_t overload
        output.flush();
    } // actual destructor closes the stream
    FILE *file = fopen("ui.log", "r");
    if (!file) {
        fprintf(stderr, "FAIL production constructor did not create ui.log\n");
        return 1;
    }
    unsigned passed = 0;
    for (unsigned i = 0; i < count; ++i) {
        char line[128] = {0};
        if (!fgets(line, sizeof(line), file) || strcmp(line, expected[i]) != 0) {
            fprintf(stderr, "FAIL size_t case %u expected=%s actual=%s", i, expected[i], line);
            fclose(file);
            return 1;
        }
        ++passed;
    }
    if (fgetc(file) != EOF || ferror(file)) {
        fprintf(stderr, "FAIL extra output or read failure\n");
        fclose(file);
        return 1;
    }
    fclose(file);
    printf("PASS actual UIOutputStream cases=%u pointer_bytes=%u\n", passed, static_cast<unsigned>(sizeof(void *)));
    return 0;
}
