---
id: xwiki-XWiki.ClassTemplate
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906698000
sync_date: 2026-08-16 20:01:45
tags:
  - xwiki/documentation
  - space/xwiki
---
# Class Template

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906698000
- **Source:** [Class Template](https://wiki.systemaops.in/bin/view/XWiki/XWiki.ClassTemplate)

---

{{velocity}}
## Replace the default space with the space where you want your documents to be created.
## Replace the default parent with the one of your choice and save the document.
##
#set ($defaultSpace = $doc.space)
#set ($defaultParent = $doc.fullName)
{{/velocity}}
