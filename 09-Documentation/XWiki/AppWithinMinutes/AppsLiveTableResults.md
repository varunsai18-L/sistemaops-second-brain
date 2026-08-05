---
id: xwiki-xwiki:AppWithinMinutes.AppsLiveTableResults
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906770000
sync_date: 2026-07-21 11:02:29
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# AppsLiveTableResults

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906770000
- **Source:** [AppsLiveTableResults](https://wiki.systemaops.in/bin/view/AppWithinMinutes/xwiki:AppWithinMinutes.AppsLiveTableResults)

---

{{include reference="XWiki.LiveTableResultsMacros" /}}

{{velocity wiki="false"}}
#if($xcontext.action == 'get' && "$!{request.outputSyntax}" == 'plain')
  $response.setContentType('application/json')
  #set($map = {})
  #gridresult_buildJSON("$!request.classname" $request.collist.split(',') $map)
  ## Change the URL and permission for the edit and delete actions:
  ## * edit action must trigger the AppWithinMinutes wizard.
  ## * delete action must delete the application space.
  #foreach($row in $map.get('rows'))
    #set($rowDocRef = $services.model.resolveDocument($row.get('doc_fullName')))
    #set($rowDoc = $xwiki.getDocument($rowDocRef))
    #set($classFullName = $rowDoc.getObject('AppWithinMinutes.LiveTableClass').getProperty('class').value)
    #set($classRef = $services.model.resolveDocument($classFullName))
    ## Edit action
    #if($row.get('doc_hasedit'))
      ## Make sure to test edit rights on the application's class and not its homepage.
      #set($discard = $row.put('doc_hasedit', $services.security.authorization.hasAccess('edit', $classRef)))
    #end
    #set($appQueryString = "appName=$escapetool.url($row.get('doc_space'))&resolve=true")
    #set($discard = $row.put('doc_edit_url', $xwiki.getURL('AppWithinMinutes.CreateApplication', 'view',
      $appQueryString)))
    ## Delete action
    #if($row.get('doc_hasdelete'))
      ## Deleting an application requires space administration rights on both data and code spaces.
      #set($hasDeleteData = $services.security.authorization.hasAccess('admin', $rowDocRef.lastSpaceReference))
      #set($hasDeleteCode = $services.security.authorization.hasAccess('admin', $classRef.lastSpaceReference))
      #set($hasDeleteApplication = $hasDeleteData && $hasDeleteCode)
      #set($discard = $row.put('doc_hasdelete', $hasDeleteApplication))
    #end
    #set($discard = $row.put('doc_delete_url', $xwiki.getURL('AppWithinMinutes.DeleteApplication', 'view',
      $appQueryString)))
  #end
  $jsontool.serialize($map)
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
