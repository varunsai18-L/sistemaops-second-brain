---
id: xwiki-AppWithinMinutes.Title
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906788000
sync_date: 2026-08-16 19:45:33
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Title

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906788000
- **Source:** [Title](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.Title)

---

{{velocity}}
#if ($type == 'edit')
  #set ($className = $object.getxWikiClass().name)
  #if ($doc.fullName == $className)
    ## We are editing the class so the title must be read from / written to the template document.
    #set ($name = 'templateTitle')
    #set ($value = $xwiki.getDocument("$stringtool.removeEnd($className, 'Class')Template").title)
  #else
    ## We are editing an application entry so the title must be read from / written to the current document.
    #set ($name = 'title')
    #set ($value = $tdoc.title)
    #if ("$!value" == '')
      #set ($value = $tdoc.documentReference.name)
    #end
  #end
  {{html clean="false"}}
  <input type="text" name="$name" value="$!escapetool.xml($value)"
    ## The default value for an AppWithinMinutes field should be optional so we make only the actual page title
    ## mandatory and not the template title, which holds the default title value.
    #if ($name == 'title' && $xwiki.getSpacePreference('xwiki.title.mandatory') == 1)required #end
    data-validation-value-missing="$escapetool.xml($services.localization.render('core.validation.required.message'))"/>
  {{/html}}
#elseif ("$!type" != '')
  ## Render the title of the current document.
  {{html}}$tdoc.getRenderedTitle('xhtml/1.0'){{/html}}
#else
  The display mode is not specified!
#end
{{/velocity}}
