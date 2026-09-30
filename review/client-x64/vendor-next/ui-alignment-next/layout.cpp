#include "_precompile.h"
#include "UIBaseObject.h"
#include "UIWidget.h"
#include "UIButton.h"
#include "UIPage.h"
#include "UIText.h"
#pragma section(".layout", read)
__declspec(allocate(".layout")) extern const unsigned int swg_ui_layout[] = {
 sizeof(void*),sizeof(size_t),
 sizeof(UIBaseObject),__alignof(UIBaseObject),
 sizeof(UIWidget),__alignof(UIWidget),
 sizeof(UIButton),__alignof(UIButton),
 sizeof(UIPage),__alignof(UIPage),
 sizeof(UIText),__alignof(UIText)
};
