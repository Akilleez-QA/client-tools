#if !defined(_MSC_VER) || _MSC_VER != 1800
#error Native VS2013 v120 required
#endif
#define EXEC31_TEXT_INNER(x) #x
#define EXEC31_TEXT(x) EXEC31_TEXT_INNER(x)
#pragma message("EXEC31 _MSC_FULL_VER=" EXEC31_TEXT(_MSC_FULL_VER))
