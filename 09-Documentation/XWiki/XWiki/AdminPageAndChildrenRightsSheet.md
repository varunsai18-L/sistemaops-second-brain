---
id: xwiki-XWiki.AdminPageAndChildrenRightsSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905822000
sync_date: 2026-08-19 20:22:34
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminPageAndChildrenRightsSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905822000
- **Source:** [AdminPageAndChildrenRightsSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminPageAndChildrenRightsSheet)

---

{{velocity}}
{{info}}
  #set($webHomeRef = $services.model.resolveDocument('WebHome'))
  ## For the children link, we do not use 'viewer=children' because the WebHome might not exist and the viewer shows a
  ## 404 error in that case. Instead, we use 'xpage=children' because it always works, and because children document
  ## could exist even if the parent document does not.
  $services.localization.render('admin.pageandchildrenrights.info', ['**', '[[', ">>path:$xwiki.getURL($webHomeRef, 'view', 'xpage=children')]]", '**'])
{{/info}}

### Administrate the rights in a space (page + children = space).
{{html}}
#template('rightsUI.vm')
{{/html}}
{{/velocity}}
