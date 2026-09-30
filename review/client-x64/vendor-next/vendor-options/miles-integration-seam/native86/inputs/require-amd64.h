#if _MSC_VER != 1800 || !defined(_M_X64)
#error Actual v120 amd64 compiler required
#endif
static_assert(sizeof(void *) == 8, "native pointer width");
