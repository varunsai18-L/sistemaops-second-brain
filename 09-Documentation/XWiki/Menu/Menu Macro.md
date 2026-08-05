---
id: xwiki-xwiki:Menu.MenuMacro
type: XWiki Page
space: "Menu"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907323000
sync_date: 2026-07-21 11:03:24
tags:
  - xwiki/documentation
  - space/menu
---
# Menu Macro

- **Space:** Menu
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907323000
- **Source:** [Menu Macro](https://wiki.systemaops.in/bin/view/Menu/xwiki:Menu.MenuMacro)

---

{{toc/}}

= Horizontal Menu =

{{velocity}}
#set ($menuTemplateDoc = $xwiki.getDocument('MenuTemplate'))
{{code language="none"}}
{{menu type="horizontal fixedWidth"}}
## No way to escape content in the code macro, so just remove {, see https://jira.xwiki.org/browse/XRENDERING-13.
$menuTemplateDoc.content.replace('{', '')
{{/menu}}
{{/code}}
{{/velocity}}

{{menu type="horizontal fixedWidth"}}
{{include reference="MenuTemplate" /}}
{{/menu}}

= Vertical Menu =

{{velocity}}
{{code language="none"}}
{{menu type="vertical"}}
...
{{/menu}}
{{/code}}
{{/velocity}}

{{menu type="vertical"}}
{{include reference="MenuTemplate" /}}
{{/menu}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
