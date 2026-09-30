#if !defined(_MSC_VER) || _MSC_VER != 1800
#error Native VS2013 v120 required
#endif
#define EXEC33_TEXT_INNER(x) #x
#define EXEC33_TEXT(x) EXEC33_TEXT_INNER(x)
#pragma message("EXEC33 _MSC_FULL_VER=" EXEC33_TEXT(_MSC_FULL_VER))
