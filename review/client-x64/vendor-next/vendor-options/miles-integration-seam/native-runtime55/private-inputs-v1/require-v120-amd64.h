#if !defined(_MSC_VER) || _MSC_VER != 1800 || !defined(_M_X64) || !defined(_WIN64)
#error Requires actual v120 AMD64 object gate
#endif
static_assert(sizeof(void *) == 8, "AMD64 pointer width");
