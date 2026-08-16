---
id: xwiki-XWiki.AdminLocalizationSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905903000
sync_date: 2026-08-16 20:01:23
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminLocalizationSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905903000
- **Source:** [AdminLocalizationSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminLocalizationSheet)

---

{{velocity output="false"}}
### Administer localization wiki preferences, at global level
#set ($params = {
  'language': ['multilingual', 'languages' , 'default_language'],
  'date': ['dateformat', 'timezone']
})
## Used to display nicer inputs for the languages
#set ($discard = $xwiki.jsx.use('XWiki.AdminLocalizationSheet'))
#set ($discard = $xwiki.ssx.use('XWiki.AdminLocalizationSheet'))
{{/velocity}}

{{include reference="XWiki.AdminFieldsDisplaySheet" /}}
