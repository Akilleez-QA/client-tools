#include <pcre.h>
#include <stdio.h>
#include <string.h>
#include "capacity.h"
typedef char pointer_width_check[sizeof(void *) * 8 == EXPECT_BITS ? 1 : -1];
int main(void)
{
    int counts[] = {0, 1, 10, 11, 20};
    unsigned int k;
    int checks = 0;
    const char *version = pcre_version();
    printf("PROVIDER %s\n", version);
    if (strncmp(version, "4.1 ", 4) != 0) return 10;
    for (k = 0; k < sizeof(counts) / sizeof(counts[0]); ++k)
    {
        char pattern[128], subject[32];
        int i, errorOffset, result, at = 0;
        const char *error = 0;
        pcre *expression;
        struct { int before; int slots[CAPTURE_SLOTS]; int after; } output;
        pattern[at++] = '^';
        for (i = 0; i < counts[k]; ++i)
        {
            pattern[at++] = '('; pattern[at++] = 'a'; pattern[at++] = ')';
            subject[i] = 'a';
        }
        pattern[at++] = '$'; pattern[at] = 0; subject[i] = 0;
        output.before = 1234567; output.after = 7654321;
        expression = pcre_compile(pattern, 0, &error, &errorOffset, 0);
        if (!expression) return 11;
        result = pcre_exec(expression, 0, subject, (int)strlen(subject), 0, 0, output.slots, CAPTURE_SLOTS);
        if (result != (counts[k] <= 10 ? counts[k] + 1 : 0)) return 12;
        ++checks;
        if (output.before != 1234567 || output.after != 7654321) return 13;
        ++checks;
        if (output.slots[0] != 0 || output.slots[1] != counts[k]) return 14;
        ++checks;
        result = pcre_exec(expression, 0, "b", 1, 0, 0, output.slots, CAPTURE_SLOTS);
        if (result != PCRE_ERROR_NOMATCH) return 15;
        ++checks;
        if (output.before != 1234567 || output.after != 7654321) return 16;
        ++checks;
        pcre_free(expression);
    }
    printf("PASS %d bounded correct-count checks\n", checks);
    return checks == 25 ? 0 : 17;
}
