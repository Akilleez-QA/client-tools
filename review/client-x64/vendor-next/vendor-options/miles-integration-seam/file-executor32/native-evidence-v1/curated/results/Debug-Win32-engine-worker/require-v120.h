#if !defined(_MSC_VER) || _MSC_VER != 1800
#error Native VS2013 v120 required
#endif
#define EXEC32_TEXT_INNER(x) #x
#define EXEC32_TEXT(x) EXEC32_TEXT_INNER(x)
#pragma message("EXEC32 _MSC_FULL_VER=" EXEC32_TEXT(_MSC_FULL_VER))
