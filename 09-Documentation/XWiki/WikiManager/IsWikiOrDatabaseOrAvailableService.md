---
id: xwiki-xwiki:WikiManager.IsWikiOrDatabaseOrAvailableService
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906673000
sync_date: 2026-07-21 11:02:05
tags:
  - xwiki/documentation
  - space/wikimanager
---
# IsWikiOrDatabaseOrAvailableService

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906673000
- **Source:** [IsWikiOrDatabaseOrAvailableService](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.IsWikiOrDatabaseOrAvailableService)

---

{{velocity}}
#if ($request.wikiname)
  #if (!$services.wiki.idAvailable($request.wikiname))
    #if (!$services.wiki.exists($request.wikiname))
database
    #else
wiki
    #end
  #else
true
  #end
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
