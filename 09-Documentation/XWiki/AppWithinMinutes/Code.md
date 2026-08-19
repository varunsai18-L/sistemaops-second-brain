---
id: xwiki-AppWithinMinutes.CodeSpaceTemplate
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906781000
sync_date: 2026-08-19 20:23:08
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Code

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906781000
- **Source:** [Code](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.CodeSpaceTemplate)

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
