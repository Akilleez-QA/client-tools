#if !defined(_MSC_VER) || _MSC_VER != 1800 || !defined(_M_IX86) || defined(_WIN64)
#error Requires actual v120 Win32 object gate
#endif
static_assert(sizeof(void *) == 4, "Win32 pointer width");
