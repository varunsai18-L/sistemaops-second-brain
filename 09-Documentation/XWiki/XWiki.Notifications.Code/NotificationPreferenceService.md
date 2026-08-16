---
id: xwiki-XWiki.Notifications.Code.NotificationPreferenceService
type: XWiki Page
space: "XWiki.Notifications.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906578000
sync_date: 2026-08-16 20:01:36
tags:
  - xwiki/documentation
  - space/xwiki.notifications.code
---
# NotificationPreferenceService

- **Space:** XWiki.Notifications.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906578000
- **Source:** [NotificationPreferenceService](https://wiki.systemaops.in/bin/view/XWiki.Notifications.Code/XWiki.Notifications.Code.NotificationPreferenceService)

---

{{velocity}}
#set($isActionAllowed = false)
#if ("$!request.user" != "")
    #if ($request.user.contains("."))
      #set ($targetUser = $request.user)
    #else
      #set ($targetUser = "XWiki." + $request.user)
    #end
#end
#if ("$!request.target" == 'wiki')
  #set ($targetDoc = $xwiki.getDocument($services.model.createDocumentReference('', ['XWiki', 'Notifications', 'Code'], 'NotificationAdministration')))
  #set ($targetRef = $services.wiki.getCurrentWikiReference())
  #set($isActionAllowed = $hasAdmin)
#elseif ("$!request.target" == 'user')
  #set ($targetDoc = $xwiki.getDocument($targetUser))
  #set ($targetRef = $services.model.resolveDocument($targetUser))
  #set($isActionAllowed = ("$!request.action" == 'watchUser' || "$!request.action" == 'unwatchUser' || $services.security.authorization.hasAccess('admin', $requestedUserDocRef) || $xcontext.userReference.equals($targetRef)))
#end
#if ("$!request.action" == "" && $request.method.equalsIgnoreCase('get'))
  This is a technical page for Notifications macro.
#elseif (!$services.csrf.isTokenValid($request.csrf))
  #set ($discard = $response.sendError(401, $services.localization.render('notifications.settings.error.badCSRF')))
#elseif (!$isActionAllowed)
  #set ($discard = $response.sendError(401))
#elseif ("$!request.action" == "" || "$!request.target" == "" || ("$!request.target" == 'user' && "$!request.user" == ""))
  #set ($discard = $response.sendError(400, $services.localization.render('notifications.settings.error.badParameters')))
#elseif ("$!request.action" == "setInterval")
  #if ("$!request.interval" == '')
    #set ($discard = $response.sendError(400, $services.localization.render('notifications.settings.error.badParameters')))
  #end
  #set ($prefObj = $targetDoc.getObject('XWiki.Notifications.Code.NotificationEmailPreferenceClass', true))
  #set ($discard = $prefObj.set('interval', $request.interval))
  #set ($discard = $targetDoc.save('Update Notification Email Interval'))
#elseif ("$!request.action" == "setDiffType")
  #if ("$!request.diffType" == '')
    #set ($discard = $response.sendError(400, $services.localization.render('notifications.settings.error.badParameters')))
  #end
  #set ($prefObj = $targetDoc.getObject('XWiki.Notifications.Code.NotificationEmailPreferenceClass', true))
  #set ($discard = $prefObj.set('diffType', $request.diffType))
  #set ($discard = $targetDoc.save('Update Notification Email Diff Type'))
#elseif ("$!request.action" == 'savePreferences')
  #try()
    #if ("$!request.target" == 'wiki')
      $services.notification.preferences.saveNotificationPreferencesForCurrentWiki($request.json)
    #else
      $services.notification.preferences.saveNotificationPreferences($request.json, $targetRef)
    #end
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#elseif ("$!request.action" == 'deleteFilterPreference')
  #try()
    #if ("$!request.target" == 'wiki')
      $services.notification.filters.deleteWikiFilterPreference($request.filterPreferenceId, $targetRef)
    #else
      $services.notification.filters.deleteFilterPreference($request.filterPreferenceId, $targetRef)
    #end
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#elseif ("$!request.action" == 'setFilterPreferenceEnabled')
  #try()
    #if ("$!request.target" == 'wiki')
      $services.notification.filters.setWikiFilterPreferenceEnabled($request.filterPreferenceId, $stringtool.equals("$!request.enabled", 'true'), $targetRef)
    #else
      $services.notification.filters.setFilterPreferenceEnabled($request.filterPreferenceId, $stringtool.equals("$!request.enabled", 'true'), $targetRef)
    #end
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#elseif ("$!request.action" == 'createScopeFilterPreference')
  #try()
    #macro (saveScopeFilterPreference $reference)
      #if ("$!request.target" == 'wiki')
        $services.notification.filters.createWikiScopeFilterPreference($request.filterType, $request.filterFormats.split(','), $request.eventTypes.split(','), $reference, $targetRef)
      #else
        $services.notification.filters.createScopeFilterPreference($request.filterType, $request.filterFormats.split(','), $request.eventTypes.split(','), $reference, $targetRef)
      #end
    #end
    #if ("$!request.wiki" != "")
      #foreach ($wikiRequest in $request.getParameterValues('wiki'))
        #set ($reference = $services.model.createWikiReference($wikiRequest))
        #saveScopeFilterPreference($reference)
      #end
    #end
    #if ("$!request.space" != "")
      #foreach ($spaceRequest in $request.getParameterValues('space'))
        #set ($reference = $services.model.resolveSpace($spaceRequest))
        #saveScopeFilterPreference($reference)
      #end
    #end
    #if ("$!request.page" != "")
      #foreach ($pageRequest in $request.getParameterValues('page'))
        #set ($reference = $services.model.resolveDocument($pageRequest))
        #saveScopeFilterPreference($reference)
      #end
    #end
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#elseif ("$!request.action" == 'setAutoWatchMode')
  #try()
    #set ($obj = $targetDoc.getObject('XWiki.Notifications.Code.AutomaticWatchModeClass', true))
    #set ($discard = $obj.set('automaticWatchMode', $request.mode))
    #set ($discard = $targetDoc.save('Update the automaticWatchMode.'))
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#elseif ("$!request.action" == 'watchUser' || "$!request.action" == 'unwatchUser')
  #try()
    #if ($request.action == 'watchUser')
      #set ($discard = $services.notification.watch.watchUser($request.user))
    #else
      #set ($discard = $services.notification.watch.unwatchUser($request.user))
    #end
  #end
  #if ("$!exception" != '')
    $response.sendError(500, "$!exceptiontool.getStackTrace($exception)")
  #end
#end
{{/velocity}}

