---
id: xwiki-xwiki:XWiki.UIExtensionSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906688000
sync_date: 2026-07-21 11:02:15
tags:
  - xwiki/documentation
  - space/xwiki
---
# User Interface Extension Sheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906688000
- **Source:** [User Interface Extension Sheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.UIExtensionSheet)

---

{{velocity}}
#set ($class = $doc.getObject('XWiki.UIExtensionClass').xWikiClass)
#foreach ($uix in $doc.getObjects('XWiki.UIExtensionClass'))
  = UIExtension $uix.number =
  #foreach ($prop in $class.properties)
    ; $prop.prettyName
    #if ($prop.getType() == 'TextAreaClass')
      : (% class="box" %)((({{{$uix.getProperty($prop.getName()).getValue()}}})))
    #else
      : $doc.display($prop.getName(), $uix)
    #end
  #end
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
