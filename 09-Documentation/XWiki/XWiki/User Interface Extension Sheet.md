---
id: xwiki-XWiki.UIExtensionSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906688000
sync_date: 2026-08-16 20:01:46
tags:
  - xwiki/documentation
  - space/xwiki
---
# User Interface Extension Sheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906688000
- **Source:** [User Interface Extension Sheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.UIExtensionSheet)

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
