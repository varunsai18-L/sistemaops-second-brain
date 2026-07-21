---
id: xwiki-xwiki:Help.Applications.Movies.Code.WebHome
type: XWiki Page
space: "Help.Applications.Movies.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781909447000
sync_date: 2026-07-21 11:03:53
tags:
  - xwiki/documentation
  - space/help.applications.movies.code
---
# Code

- **Space:** Help.Applications.Movies.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781909447000
- **Source:** [Code](https://wiki.systemaops.in/bin/view/Help.Applications.Movies.Code/xwiki:Help.Applications.Movies.Code.WebHome)

---

{{translation key="appWithinMinutes.codeSpace.description" /}}

{{velocity}}
#if ("$xwiki.getUserPreference('displayHiddenDocuments')" != '1')
  {{info}}
    {{translation key="appWithinMinutes.codeSpace.hiddenPagesInfo" /}}
  {{/info}}
#end

#set ($escapedDocumentReference = $services.rendering.escape($services.model.serialize($doc.documentReference,
  'default'), 'xwiki/2.1'))
{{documentTree showTranslations="false" showAttachments="false"
  filterHiddenDocuments="false" root="document:$escapedDocumentReference" /}}
{{/velocity}}
