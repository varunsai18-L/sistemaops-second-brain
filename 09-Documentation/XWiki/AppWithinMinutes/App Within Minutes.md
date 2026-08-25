---
id: xwiki-AppWithinMinutes.WebHome
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906782000
sync_date: 2026-08-25 21:13:50
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# App Within Minutes

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906782000
- **Source:** [App Within Minutes](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.WebHome)

---

{{velocity}}
$services.localization.render('platform.appwithinminutes.description')

#if($hasCreateSpace)
  (% class="buttonwrapper" %)[[$services.localization.render('platform.appwithinminutes.createAppButtonLabel')>>CreateApplication||class="button" queryString="wizard=true"]]

#end
= $services.localization.render('platform.appwithinminutes.appsLiveTableHeading') =##
#set($columnsProperties = {
  'doc.title': {'type': 'text', 'link': 'view', 'size': 10, 'filterable': true, 'sortable': true},
  'doc.author': {'type': 'text', 'link': 'author', 'size': 10, 'filterable': true, 'sortable': true},
  'doc.date': {'type': 'date', 'size': 10, 'filterable': true, 'sortable': true},
  '_actions': {'html': true, 'sortable': false, 'actions': ['edit', 'delete']}
})
#set($options = {
  'className': 'AppWithinMinutes.LiveTableClass',
  'resultPage' : 'AppWithinMinutes.AppsLiveTableResults',
  'translationPrefix': 'platform.appwithinminutes.appsLiveTable.',
  'tagCloud': true,
  'rowCount': 15,
  'maxPages': 10,
  'selectedColumn': 'doc.title',
  'defaultOrder': 'asc'
})
#set($columns = ['doc.title', 'doc.author', 'doc.date', '_actions'])
#livetable('livetable' $columns $columnsProperties $options)
#set ($displayDocExtra = false)
{{/velocity}}
