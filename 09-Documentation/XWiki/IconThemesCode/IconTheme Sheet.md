---
id: xwiki-xwiki:IconThemesCode.IconThemeSheet
type: XWiki Page
space: "IconThemesCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905626000
sync_date: 2026-07-21 11:00:45
tags:
  - xwiki/documentation
  - space/iconthemescode
---
# IconTheme Sheet

- **Space:** IconThemesCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905626000
- **Source:** [IconTheme Sheet](https://wiki.systemaops.in/bin/view/IconThemesCode/xwiki:IconThemesCode.IconThemeSheet)

---

{{velocity}}
#if($doc.fullName != 'IconThemesCode.IconThemeSheet')
{{info}}
This document is an Icon Theme.
{{/info}}

(%class="code"%)(((
$services.rendering.escape($doc.content, 'xwiki/2.1')
)))
#else
Sheet of [[IconThemesCode.IconThemeClass]]
#end
{{/velocity}}
