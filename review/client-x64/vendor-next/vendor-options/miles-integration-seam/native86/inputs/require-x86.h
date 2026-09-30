#if _MSC_VER != 1800 || !defined(_M_IX86)
#error Actual v120 x86 compiler required
#endif
static_assert(sizeof(void *) == 4, "native pointer width");
