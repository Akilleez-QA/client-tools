#if !defined(_MSC_VER) || _MSC_VER != 1800
#error Native VS2013 v120 required
#endif
#define SEAM29_TEXT_INNER(x) #x
#define SEAM29_TEXT(x) SEAM29_TEXT_INNER(x)
#pragma message("SEAM29 _MSC_FULL_VER=" SEAM29_TEXT(_MSC_FULL_VER))
