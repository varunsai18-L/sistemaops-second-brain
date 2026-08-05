---
id: xwiki-xwiki:Menu.MenuSheet
type: XWiki Page
space: "Menu"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907308000
sync_date: 2026-07-21 11:03:19
tags:
  - xwiki/documentation
  - space/menu
---
# MenuSheet

- **Space:** Menu
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907308000
- **Source:** [MenuSheet](https://wiki.systemaops.in/bin/view/Menu/xwiki:Menu.MenuSheet)

---

{{velocity}}
{{html wiki='true'}}
#set ($discard = $doc.use('Menu.MenuClass'))
(% class='xform' %)
(((
  ; <label#if ($xcontext.action=='edit') for='Menu.MenuClass_0_content1'#end>$escapetool.xml($doc.displayPrettyName('content1', false, false))</label>
  : $doc.display('content1')
)))
{{/html}}
{{/velocity}}

{{include reference="Menu.UIExtensionSheet" /}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
