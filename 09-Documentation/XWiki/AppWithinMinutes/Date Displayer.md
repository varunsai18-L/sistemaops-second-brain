---
id: xwiki-AppWithinMinutes.DateDisplayer
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906757000
sync_date: 2026-08-25 21:13:45
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Date Displayer

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906757000
- **Source:** [Date Displayer](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.DateDisplayer)

---

{{velocity}}
#set ($MAGIC_DATE = $datetool.toDate('yyyy-MM-dd', '9999-12-31'))
#if ($xcontext.action == 'edit' && $field.classType == 'Date' && $field.getValue('emptyIsToday') == 1 && $MAGIC_DATE.equals($value))
  #set ($value = $NULL)
#end
{{html}}#template('displayer_date.vm'){{/html}}
{{/velocity}}

