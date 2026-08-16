---
id: xwiki-WikiManager.WebHome
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906680000
sync_date: 2026-08-16 19:45:14
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Browse Wikis

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906680000
- **Source:** [Browse Wikis](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.WebHome)

---

{{velocity}}
{{html}}
#set ($createWikiDocReference = $services.model.createDocumentReference($services.wiki.mainWikiId, 
  'WikiManager', 'CreateWiki'))
#if ($hasCreateWiki && $xwiki.exists($createWikiDocReference) 
  && $services.security.authorization.hasAccess('view', $createWikiDocReference))
  <p>
    <a href="$xwiki.getURL('WikiManager.CreateWiki')" class="button button-success" id="tmCreateWiki">
      $services.icon.renderHTML('add') $services.localization.render('platform.wiki.create.button')
    </a>
  </p>
#end
{{/html}}
#set($columns = ['wikiprettyname', 'description', 'owner', 'doc.creationDate', 'membershipType'])
#if(!$isGuest)
  #set($discard = $columns.add('_actions'))
#end

#set ($liveDataConfig = {
  'meta': {
    'propertyDescriptors': [
      { 'id': 'wikiprettyname', 'displayer': { 'id': 'link', 'propertyHref': 'wikiprettyname_url' } },
      { 'id': 'owner', 'editable': false},
      { 'id': 'membershipType', 'sortable': false, 'filterable': false, 'editable': false },
      { 
        'id': '_actions',
        'displayer': {
          'id': 'actions', 
          'actions': ['join', 'leave', 'requestJoin', 'cancelJoinRequest', 'viewInvitation', 'edit', 'delete']
        }
      }
    ],
    'actions': [
      { 
        'id': 'join',
        'icon': 'user_add',
        'allowProperty': 'doc.hasjoin',
        'urlProperty': 'doc.join_url'
      },
      {
        'id': 'leave',
        'icon': 'user_delete',
        'allowProperty': 'doc.hasleave',
        'urlProperty': 'doc.leave_url'
      },
      {
        'id': 'requestJoin',
        'icon': 'bell',
        'allowProperty': 'doc.hasrequestJoin',
        'urlProperty': 'doc.requestJoin_url'
      },
      {
        'id': 'cancelJoinRequest',
        'icon': 'bell_delete',
        'allowProperty': 'doc.hascancelJoinRequest',
        'urlProperty': 'doc.cancelJoinRequest_url'
      },
      {
        'id': 'viewInvitation',
        'icon': 'envelope',
        'allowProperty': 'doc.hasviewInvitation',
        'urlProperty': 'doc.viewInvitation_url'
      }
    ]
  }
})
#set ($sourceParameters = $escapetool.url({
  'className' : 'XWiki.XWikiServerClass',
  'resultPage' : 'WikiManager.WikisLiveTableResults',
  'translationPrefix' : 'platform.wiki.browse.',
  '$doc' : $doc.fullName
}))
{{liveData
  id='wikis'
  source='liveTable'
  sourceParameters="$sourceParameters"
  properties="$stringtool.join($columns, ',')"
  limit=10
}}$jsontool.serialize($liveDataConfig){{/liveData}}
#set($docextras=[])
{{/velocity}}
