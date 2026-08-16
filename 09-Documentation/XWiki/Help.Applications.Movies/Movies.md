---
id: xwiki-Help.Applications.Movies.WebHome
type: XWiki Page
space: "Help.Applications.Movies"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781909449000
sync_date: 2026-08-16 20:02:20
tags:
  - xwiki/documentation
  - space/help.applications.movies
---
# Movies

- **Space:** Help.Applications.Movies
- **Author:** XWiki.superadmin
- **Last Modified:** 1781909449000
- **Source:** [Movies](https://wiki.systemaops.in/bin/view/Help.Applications.Movies/Help.Applications.Movies.WebHome)

---

{{velocity}}
#set ($columnsProperties = {
  'longText1': {"type":"text","filterable":false,"sortable":false,"html":true},
  'doc.title': {"type":"text","size":20,"displayName":"Title","link":"view"},
  'staticList1': {"type":"list","size":10},
  'date1': {"type":"text","size":10,"html":true},
  'databaseList1': {"type":"list","size":10},
  'boolean1': {"type":"text","size":10},
  '_actions': {"sortable":false,"filterable":false,"html":true,"actions":["edit","delete"]}
})
#set ($options = {
  'className': 'Help.Applications.Movies.Code.MoviesClass',
  'translationPrefix': 'movies.livetable.',
  'tagCloud': true,
  'rowCount': 15,
  'maxPages': 10,
  'selectedColumn': 'longText1',
  'defaultOrder': 'asc'
})
#set ($columns = ['longText1', 'doc.title', 'staticList1', 'date1', 'databaseList1', 'boolean1', '_actions'])
#livetable('movies' $columns $columnsProperties $options)
{{/velocity}}
