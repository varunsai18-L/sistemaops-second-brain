---
id: xwiki-xwiki:XWiki.AdminLocalizationSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905903000
sync_date: 2026-07-21 11:01:11
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminLocalizationSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905903000
- **Source:** [AdminLocalizationSheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.AdminLocalizationSheet)

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

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
