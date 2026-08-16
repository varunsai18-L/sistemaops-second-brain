---
id: xwiki-WikiManager.AdminWikisRightsSheet
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906621000
sync_date: 2026-08-16 20:01:39
tags:
  - xwiki/documentation
  - space/wikimanager
---
# AdminWikisRightsSheet

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906621000
- **Source:** [AdminWikisRightsSheet](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.AdminWikisRightsSheet)

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
