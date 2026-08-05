---
id: xwiki-xwiki:Panels.PanelSheet
type: XWiki Page
space: "Panels"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906883000
sync_date: 2026-07-21 11:02:52
tags:
  - xwiki/documentation
  - space/panels
---
# PanelSheet

- **Space:** Panels
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906883000
- **Source:** [PanelSheet](https://wiki.systemaops.in/bin/view/Panels/xwiki:Panels.PanelSheet)

---

{{velocity output="false"}}
#macro(displayPanelProperty $obj $propName)
  ; <label#if ($xcontext.action == 'edit') for="${class.getName()}_${obj.number}_${propName}"#end>$services.localization.render("${class.getName()}_${propName}")</label>
  : $doc.display($propName, $obj)
#end

#set ($paneldoc = $doc)
{{/velocity}}

{{velocity}}
#set ($obj = $doc.getObject('Panels.PanelClass'))
#if ($obj)
  #set($class = $obj.xWikiClass)
  {{html wiki="true"}}
  (% class="xform" %)
  (((
    #displayPanelProperty($obj 'name')
    #displayPanelProperty($obj 'type')
    #displayPanelProperty($obj 'category')
    #displayPanelProperty($obj 'description')
    #displayPanelProperty($obj 'content')
    #displayPanelProperty($obj 'async_enabled')
    #displayPanelProperty($obj 'async_cached')
    #displayPanelProperty($obj 'async_context')
  )))
  {{/html}}
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
