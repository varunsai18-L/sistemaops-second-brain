---
id: xwiki-XWiki.AdminPresentationSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905848000
sync_date: 2026-08-16 19:44:53
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminPresentationSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905848000
- **Source:** [AdminPresentationSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminPresentationSheet)

---

{{velocity output="false"}}
### Choose the page elements to display, globally and at space level.
#set ($params = {
  'docextra': ['showannotations', 'showcomments', 'showattachments', 'showhistory', 'showinformation'],
  'header': ['title', 'meta']
})
#if ("$!editor" == 'globaladmin')
  #set ($params.footer = ['webcopyright', 'version'])
#end
{{/velocity}}

{{include reference="XWiki.AdminFieldsDisplaySheet" /}}
