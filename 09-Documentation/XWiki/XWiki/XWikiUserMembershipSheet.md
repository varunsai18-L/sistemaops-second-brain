---
id: xwiki-XWiki.XWikiUserMembershipSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906367000
sync_date: 2026-08-16 19:45:04
tags:
  - xwiki/documentation
  - space/xwiki
---
# XWikiUserMembershipSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906367000
- **Source:** [XWikiUserMembershipSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.XWikiUserMembershipSheet)

---

{{velocity}}
      #set($obj = $doc.getObject('XWiki.XWikiUsers'))
      #if(!$obj)
      {{info}}{{translation key="xe.admin.users.applyonusers"/}}{{/info}}##
      #elseif ($xcontext.action == 'get')
  #if ($xcontext.isMainWiki())
    ## Main wiki users can be located in any wiki
    #set($groups = $services.user.group.getGroupsFromAllWikis($doc.documentReference))
  #else
    ## Subwiki users are usually located only in the local wiki
    #set($groups = $services.user.group.getGroupsFromMemberWiki($doc.documentReference))
  #end
  ## Filter
  #set($filterValue = "$!{request.get('group')}")
  #if ($filterValue != '')
    #set ($filteredGroups = [])
    #foreach($group in $groups)
      #set($groupString = $services.model.serialize($group, 'default'))
      #if ($groupString.toLowerCase().contains($filterValue.toLowerCase()))
        #set($void = $filteredGroups.add($group))
      #end
    #end
  #else
    #set ($filteredGroups = $groups)
  #end
  #if ($filteredGroups.size() > 0)
    #set ($filteredGroups = $collectiontool.sort($filteredGroups))
    #set($order = "$!request.sort")
    #if ($order == 'group' && $request.get('dir').toLowerCase() == 'desc')
      ## Reverse order
      #set($descGroups = [])
      #set($max = $filteredGroups.size() - 1)
      #foreach($i in [ $max ..  0 ])
        #set($void = $descGroups.add($filteredGroups[$i]))
      #end
      #set($filteredGroups = $descGroups)
    #end
    #set($offset = $numbertool.toNumber($request.get('offset')).intValue())
    ## Offset starts from 0 in velocity and 1 in javascript
    #set($offset = $offset - 1)
    #if (!$offset || $offset < 0)
      #set($offset = 0)
    #end
    #set($limit = $numbertool.toNumber($request.get('limit')).intValue())
    #if (!$limit || $limit < 0)
      #set ($limit = 15)
    #end
    #set($toIndex = $offset + $limit)
    #if ($toIndex > $filteredGroups.size())
      #set($toIndex = $filteredGroups.size())
    #end
    #set($subGroups = $filteredGroups.subList($offset, $toIndex))
  #else
    #set($subGroups = [])
  #end
  #set($rows = [])
  #foreach ($group in $subGroups)
    #set ($title = $xwiki.getDocument($group).title)
    #if ("$!title" == '')
      #set ($title = $group.name)
    #end
    #set($void = $rows.add({
        'doc_viewable' : true,
        'group' : $title,
        'group_url' : $xwiki.getURL($group)
      }))
  #end
  #set($result = {
      'totalrows' : $filteredGroups.size(),
      'returnedrows' : $subGroups.size(),
      'offset' : $mathtool.add($offset, 1),
      'reqNo' : $numbertool.toNumber($request.reqNo),
      'rows': $rows
    })
  $jsontool.serialize($result)
  $response.setContentType('application/json')
#else
  (% id="user.profile.groups.title" %)
  == {{translation key="user.profile.groups.title"/}}

  {{translation key="user.profile.groups.description"/}}

  #set ($liveDataConfig = {
    'meta': {
      'propertyDescriptors': [
        { 'id': 'group', 'displayer': { 'id': 'link', 'propertyHref': 'group_url' } }
      ],
      'entryDescriptor': {
        'idProperty': "group"
      }
    }
  })
  #set ($sourceParameters = $escapetool.url({
    'translationPrefix' : 'user.profile.groups.table.',
    '$doc' : $doc.fullName,
    'resultPage': 'XWiki.XWikiUserMembershipSheet'
  }))

  {{liveData
    id='user.profile.group.table'
    source='liveTable'
    sourceParameters="$sourceParameters"
    properties="group"
    }}$jsontool.serialize($liveDataConfig){{/liveData}}
#end## User object exists
{{/velocity}}
