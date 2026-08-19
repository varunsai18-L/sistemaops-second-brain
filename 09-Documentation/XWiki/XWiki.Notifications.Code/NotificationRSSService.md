---
id: xwiki-XWiki.Notifications.Code.NotificationRSSService
type: XWiki Page
space: "XWiki.Notifications.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906578000
sync_date: 2026-08-19 20:22:33
tags:
  - xwiki/documentation
  - space/xwiki.notifications.code
---
# NotificationRSSService

- **Space:** XWiki.Notifications.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906578000
- **Source:** [NotificationRSSService](https://wiki.systemaops.in/bin/view/XWiki.Notifications.Code/XWiki.Notifications.Code.NotificationRSSService)

---

{{velocity}}
#set ($feedContent = $services.notification.notifiers.getFeed(20))
#if ($xcontext.action == 'get' && "$request.outputSyntax" == 'plain')
  #rawResponse($feedContent, 'application/xml')
#else
  {{code language="xml" source="script:feedContent" /}}
#end
{{/velocity}}

