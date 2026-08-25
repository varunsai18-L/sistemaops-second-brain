---
id: xwiki-Main.Search
type: XWiki Page
space: "Main"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781909931000
sync_date: 2026-08-25 21:14:33
tags:
  - xwiki/documentation
  - space/main
---
# Search

- **Space:** Main
- **Author:** XWiki.superadmin
- **Last Modified:** 1781909931000
- **Source:** [Search](https://wiki.systemaops.in/bin/view/Main/Main.Search)

---

{{include reference="XWiki.SearchCode"/}}

{{velocity}}
## If no Search UI Extension exist then don't display the Search page.
#if ("$!searchPage" != '')
  {{include reference="$searchPage"/}}
#else
  ## Display a message explaining that there's no Search UI Extension.
  $services.localization.render('search.page.noimplementation')
#end
{{/velocity}}
