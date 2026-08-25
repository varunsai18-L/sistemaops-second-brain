---
id: xwiki-XWiki.Notifications.Code.NotificationsPreferencesMacros
type: XWiki Page
space: "XWiki.Notifications.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906507000
sync_date: 2026-08-25 21:13:28
tags:
  - xwiki/documentation
  - space/xwiki.notifications.code
---
# NotificationsPreferencesMacros

- **Space:** XWiki.Notifications.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906507000
- **Source:** [NotificationsPreferencesMacros](https://wiki.systemaops.in/bin/view/XWiki.Notifications.Code/XWiki.Notifications.Code.NotificationsPreferencesMacros)

---

{{velocity output="false"}}
#if (!$XWikiNotificationsCodeNotificationsPreferencesMacrosIncluded)
#set ($XWikiNotificationsCodeNotificationsPreferencesMacrosIncluded = true)
##
## Get all event types and group them by applications
##
#set ($types = [])
#foreach ($descriptor in $services.eventstream.getRecordableEventDescriptors($xcontext.isMainWiki()))
  #set ($discard = $types.add({
    'applicationName' : "$!services.localization.render($descriptor.applicationName)",
    'applicationIcon' : "$!services.icon.renderHTML($descriptor.applicationIcon)",
    'description'     : "$!services.localization.render($descriptor.description)",
    'eventType'       : "$!descriptor.eventType",
    'filter'          : "$!descriptor.filter",
    'applicationId'   : "$!descriptor.applicationId"
  }))
#end
#set ($apps = [])
#set ($lastAppId = '')
#foreach ($type in $collectiontool.sort($types, ['applicationName', 'eventType']))
  #if ($lastAppId != $type.applicationId)
    #set ($lastAppId = $type.applicationId)
    #set ($lastApp = [])
    #set ($discard = $apps.add($lastApp))
  #end
  #set ($discard = $lastApp.add($type))
#end
#end

##
## Check that the macro preferences parameters are ok and the current user have proper permissions.
##
#macro (checkMacroNotificationPreferencesParameters $checkResult)
  #set ($checkResult = false)
  #if (!$xcontext.userReference && $wikimacro.parameters.target == 'user')
    {{info}}
      {{translation key="notifications.settings.applications.forGuest" /}}
    {{/info}}
  #elseif ($wikimacro.parameters.target == 'wiki' && !$services.security.authorization.hasAccess('admin', $services.model.createWikiReference($services.wiki.currentWikiId)))
    {{error}}
      {{translation key="notifications.settings.error.notAdmin" /}}
    {{/error}}
  #elseif ($wikimacro.parameters.target == 'user' && "$!wikimacro.parameters.user" != ""  && $wikimacro.parameters.user.class.simpleName != 'DocumentUserReference')
    {{error}}
      {{translation key="notifications.settings.error.userReferenceNotSupported" /}}
    {{/error}}
  #elseif ($wikimacro.parameters.target == 'user' && "$!wikimacro.parameters.user" != "" && !$services.security.authorization.hasAccess('admin', $wikimacro.parameters.user.reference) && !$xcontext.userReference.equals($wikimacro.parameters.user.reference))
    {{error}}
      {{translation key="notifications.settings.error.userReferenceAdminForbidden" /}}
    {{/error}}
  #else
    #set ($checkResult = true)
  #end
#end
{{/velocity}}
