---
id: xwiki-xwiki:XWiki.AccountValidation
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905828000
sync_date: 2026-07-21 11:00:22
tags:
  - xwiki/documentation
  - space/xwiki
---
# AccountValidation

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905828000
- **Source:** [AccountValidation](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.AccountValidation)

---

{{velocity}}
#if("$!{request.validkey}" != '' && "$!{request.xwikiname}" != '')
  #if($xwiki.validateUser(true) == 0)
    #set($loginURL = $xwiki.getURL('XWiki.XWikiLogin', 'login'))
    {{info}}{{html clean="false"}}$services.localization.render('xe.admin.accountvalidation.success', [${loginURL}]){{/html}}{{/info}}
  #else
    {{warning}}{{translation key="xe.admin.accountvalidation.failure"/}}{{/warning}}
  #end
#else
  $response.sendRedirect($xwiki.getURL($services.model.resolveDocument('', 'default', $doc.documentReference.extractReference('WIKI'))))
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
