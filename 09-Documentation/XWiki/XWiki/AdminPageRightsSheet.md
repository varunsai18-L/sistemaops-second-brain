---
id: xwiki-XWiki.AdminPageRightsSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905889000
sync_date: 2026-08-25 21:13:15
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminPageRightsSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905889000
- **Source:** [AdminPageRightsSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminPageRightsSheet)

---

{{velocity}}
{{info}}
#set($webHomeRef = $services.model.resolveDocument('WebHome'))
## For the children link, we do not use 'viewer=children' because the WebHome might not exist and the viewer shows a
## 404 error in that case. Instead, we use 'xpage=children' because it always works, and because children document
## could exist even if the parent document does not.
$services.localization.render('admin.pagerights.info') **$services.localization.render('admin.pagerights.infoNonTerminalDoc', ['[[', ">>path:$xwiki.getURL($webHomeRef, 'view', 'xpage=children')]]"])**
{{/info}}

### Administrate the rights in a wiki (globally or per space).
{{html}}
#template('rightsUI.vm')
{{/html}}
{{/velocity}}
