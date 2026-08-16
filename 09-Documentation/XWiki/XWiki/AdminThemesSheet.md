---
id: xwiki-XWiki.AdminThemesSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905838000
sync_date: 2026-08-16 20:01:14
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminThemesSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905838000
- **Source:** [AdminThemesSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminThemesSheet)

---

{{velocity output="false"}}
$xwiki.jsx.use('XWiki.AdminThemesSheet')
### Change the skin, color theme and icon theme, at global or space level.
#set ($params = {
  'colortheme': ['colorTheme'],
  'icontheme' : ['iconTheme'],
  'skin': ['skin']
})
{{/velocity}}

{{include reference="XWiki.AdminFieldsDisplaySheet" /}}
