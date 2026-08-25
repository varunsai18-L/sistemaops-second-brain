---
id: xwiki-WikiManager.AdminWikisTemplatesSheet
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906675000
sync_date: 2026-08-25 21:13:35
tags:
  - xwiki/documentation
  - space/wikimanager
---
# AdminWikisTemplatesSheet

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906675000
- **Source:** [AdminWikisTemplatesSheet](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.AdminWikisTemplatesSheet)

---

{{velocity}}
(% class="noitems" %)
{{translation key="admin.wikis.templates.hint" /}}

#set($columns = ['wikiprettyname', 'description', 'owner', 'membershipType'])
#if(!$isGuest)
  #set($discard = $columns.add('_actions'))
#end

#set ($liveDataConfig = {
  'meta': {
    'propertyDescriptors': [
      { 'id': 'wikiprettyname', 'displayer': { 'id': 'link', 'propertyHref': 'wikiprettyname_url' } },
      { 'id': 'membershipType', 'sortable': false, 'filterable': false }
    ]
  }
})
#set ($sourceParameters = $escapetool.url({
  'className': 'XWiki.XWikiServerClass',
  'resultPage': 'WikiManager.WikisLiveTableResults',
  'translationPrefix': 'platform.wiki.browse.',
  'onlyTemplates': '1',
  '$doc' : $doc.fullName
}))
{{liveData
  id='wikis'
  source='liveTable'
  sourceParameters="$sourceParameters"
  properties="$stringtool.join($columns, ',')"
  limit=10
}}$jsontool.serialize($liveDataConfig){{/liveData}}
{{/velocity}}
