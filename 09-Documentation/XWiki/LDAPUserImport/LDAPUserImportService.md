---
id: xwiki-LDAPUserImport.LDAPUserImportService
type: XWiki Page
space: "LDAPUserImport"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907358000
sync_date: 2026-08-25 21:14:18
tags:
  - xwiki/documentation
  - space/ldapuserimport
---
# LDAPUserImportService

- **Space:** LDAPUserImport
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907358000
- **Source:** [LDAPUserImportService](https://wiki.systemaops.in/bin/view/LDAPUserImport/LDAPUserImport.LDAPUserImportService)

---

{{velocity wiki="false"}}
#if ($xcontext.action == 'get')
  #set ($statusCode = 500)
  #if ($services.csrf.isTokenValid($request.form_token))
    ## Exclude some helper fields from being displayed in the feedback list.
    #set ($excludedFields = ['exists', 'uid', 'dn', 'userProfile', 'userProfileURL'])
    #try('ldapUserImportException')
      #if ($request.action == 'importUsers')
        #set ($noResultsMessage = $services.localization.render('importUsers.modal.fieldValue.noResults'))
        #set ($users = $services.ldapuserimport.importUsers($request.parameterMap.user, $request.groupReference))
        #foreach ($user in $users.entrySet())
          #set ($params = [])
          #foreach ($item in $user.value.entrySet())
            #if (!$excludedFields.contains($item.key))
              #set ($discard = $params.add($item.value))
            #end
          #end
          #set ($message = $services.localization.render('importUsers.modal.user.created', [$stringtool.join($params, ', ')]))
          #set ($user.value.displayMessage = $message)
        #end
        $jsontool.serialize({
          'noResults': $noResultsMessage,
          'users': $users
        })
      #elseif ($request.action == 'getMappedXWikiGroups')
        $jsontool.serialize({'mappedXWikiGroups': $services.ldapuserimport.xWikiMappedGroups})
      #elseif ($request.action == 'getGroupMemberSize')
        #set ($groupMemberSize = $services.ldapuserimport.getGroupMemberSize($request.xWikiGroupName))
        $jsontool.serialize({
          'groupMemberSize': $groupMemberSize,
          'groupMemberSizeInfo': $services.localization.render('importUsers.groupUpdate.confirmationModal.info', [$groupMemberSize])
        })
      #elseif ($request.action == 'updateGroup')
        #set ($message = $services.localization.render('importUsers.groupUpdate.updatingGroup.success'))
        #if ($services.ldapuserimport.updateGroup($request.xWikiGroupName))
          #set ($message = $services.localization.render('importUsers.groupUpdate.updatingGroup.fail'))
        #end
        $jsontool.serialize({'message': $message})
      #elseif ($request.action == 'getLDAPGroups' || $request.action == 'getLDAPOus')
        #set ($noResultsMessage = $services.localization.render('importUsers.associateGroups.modal.fieldValue.noResults'))
        #set ($isFullSearch = false)
        #if ($request.searchType=="1")
          #set ($isFullSearch = true)
        #end
        #if ($request.action == 'getLDAPOus')
          #set ($groups = $services.ldapuserimport.getLDAPGroups($request.searchInput, $request.xWikiGroupName, $isFullSearch, true))
          #set ($idKey = 'ou')
        #else
          #set ($groups = $services.ldapuserimport.getLDAPGroups($request.searchInput, $request.xWikiGroupName, $isFullSearch))
          #set ($idKey = 'cn')
        #end
        #foreach ($group in $groups.entrySet())
          #set ($description = $group.value.description)
          #if ("$!description" == '')
            #set ($description = $group.value.dn)
          #end
          #if ($group.value.isAssociated == true)
            #set ($message = $services.localization.render('importUsers.associateGroups.modal.alreadyAssociated', ["$!description", "$!group.value.get($idKey)"]))
          #else
            #set ($message = $services.localization.render('importUsers.associateGroups.modal.toAssociate', ["$!description", "$!group.value.get($idKey)"]))
          #end
          #set ($group.value.displayMessage = $message)
        #end
        $jsontool.serialize({
          'noResults': $noResultsMessage,
          'groups': $groups,
          'displayedMax': $services.ldapuserimport.displayedMax($groups.size())
        })
      #elseif ($request.action == 'associateGroups')
        #set ($status = 'fail')
        #set ($message = $services.localization.render('importUsers.associateGroups.modal.associationFail'))
        #if ($services.ldapuserimport.associateGroups($request.parameterMap.group, $request.xWikiGroupName))
          #set ($message = $services.localization.render('importUsers.associateGroups.modal.associationSuccess'))
          #set ($status = 'success')
        #end
        $jsontool.serialize({'message': $message, 'status': $status})
      #elseif ($request.action == 'searchUsers')
        #set ($isFullSearch = false)
        #if ($request.searchType=="1")
          #set ($isFullSearch = true)
        #end
        #set ($users = $services.ldapuserimport.getUsers($request.singleField, $request.allFields, $request.searchInput, $isFullSearch))
        #set ($noResultsMessage = $services.localization.render('importUsers.modal.fieldValue.noResults'))
        #foreach ($user in $users.entrySet())
          #set ($params = [])
          #foreach ($item in $user.value.entrySet())
            #if (!$excludedFields.contains($item.key))
              #set ($discard = $params.add($item.value))
            #end
          #end
          #if ($user.value.exists == true)
            #set ($message = $services.localization.render('importUsers.modal.user.alreadyImported', [$stringtool.join($params, ', ')]))
          #else
            #set ($message = $services.localization.render('importUsers.modal.user.toImport', [$stringtool.join($params, ', ')]))
          #end
          #set ($user.value.displayMessage = $message)
        #end
        $jsontool.serialize({
          'noResults': $noResultsMessage,
          'users': $users,
          'displayedMax': $services.ldapuserimport.displayedMax($users.size())
        })
      #end
      #set ($statusCode = 200)
      #if ($request.outputSyntax == 'plain')
        #set ($discard = $response.setContentType('application/json'))
      #end
    #end
    #if ("$!ldapUserImportException" != '')
      <div class="xwikirenderingerror" title="$services.localization.render('importUsers.error.expand')">
        $exceptiontool.getRootCauseMessage($ldapUserImportException)
      </div>
      <div class="xwikirenderingerrordescription hidden">
        <pre>$exceptiontool.getStackTrace($ldapUserImportException)</pre>
      </div>
    #end
  #else
    <div class="xwikirenderingerror">
      $services.localization.render('importUsers.error.invalidCSRF')
    </div>
  #end
  #set ($discard = $response.setStatus($statusCode))
#end
{{/velocity}}
