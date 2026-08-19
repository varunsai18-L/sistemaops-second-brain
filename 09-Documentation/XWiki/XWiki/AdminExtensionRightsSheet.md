---
id: xwiki-XWiki.AdminExtensionRightsSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905853000
sync_date: 2026-08-19 20:22:36
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminExtensionRightsSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905853000
- **Source:** [AdminExtensionRightsSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminExtensionRightsSheet)

---

{{velocity}}
### Sheet used to generically display the XWikiPreferences object fields in the administration sheets.
{{html}}
  <form method="post" action="$xwiki.getURL($currentDoc, 'saveandcontinue')" class="xform">
    ############################################################################################
    ## RIGHTS
    ############################################################################################
    <fieldset>
      #template('rightsUI.vm')
    </fieldset>
  </form>
{{/html}}
{{/velocity}}
