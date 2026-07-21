---
id: xwiki-xwiki:XWiki.Notifications.Code.NotificationsDisplayerUIX
type: XWiki Page
space: "XWiki.Notifications.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906409000
sync_date: 2026-07-21 11:01:50
tags:
  - xwiki/documentation
  - space/xwiki.notifications.code
---
# NotificationsDisplayerUIX

- **Space:** XWiki.Notifications.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906409000
- **Source:** [NotificationsDisplayerUIX](https://wiki.systemaops.in/bin/view/XWiki.Notifications.Code/xwiki:XWiki.Notifications.Code.NotificationsDisplayerUIX)

---

{{velocity wiki="true"}}
#********************************************************
Get the actual notifications.
********************************************************###
## We use POST since we are sending the reference of the document and we want to avoid special characters in the URL.
#if ('get' == $xcontext.action && 'POST' == $request.method && 'getNotifications' == $request.action)
  #set ($requestedDocumentReference = $services.model.resolveDocument($request.document))
  {{html clean="false"}} ## we need clean="false" because we want to display the raw content
  #if ("$!xcontext.userReference" != '' && $services.notification.isEnabled())
    <div class="notifications-header">
      <div class="clearfix">
        <div class="col-xs-4">
          <p><strong>$escapetool.xml($services.localization.render('notifications.menu.header'))</strong></p>
        </div>
        <div class="col-xs-8 text-right">
          <p>
            <span class="notifications-header-link">
              <a href="$xwiki.getURL('XWiki.Notifications.Code.NotificationRSSService', 'get', 'outputSyntax=plain')"
                  class="notifications-header-link notifications-rss-link" rel="nofollow external">
                $services.icon.renderHTML('rss')&nbsp;$escapetool.xml($services.localization.render('notifications.rss.feedLink'))
              </a>
            </span>
            <span class="notifications-header-link">
              <a href="$xwiki.getURL($xcontext.userReference, 'view', 'category=notifications')" class="notifications-settings" rel="nofollow">
                $services.icon.renderHTML('cog')&nbsp;$escapetool.xml($services.localization.render('notifications.menu.header.settings'))
              </a>
            </span>
          </p>
        </div>
      </div>
      <div class="notifications-header-uix col-xs-12">
      </div>
    </div>
    <div class="notifications-area clearfix">
  {{/html}}

  {{notifications displayReadStatus="true" useUserPreferences="true" count="10" displayRSSLink="false" /}}

  {{html clean="false"}}
  </div>
  {{/html}}
  #end
#end
{{/velocity}}

{{velocity wiki="false"}}
#********************************************************
    Get the number of unread notifications as JSON
********************************************************###
#if ('get' == $xcontext.action && 'GET' == $request.method && 'getUnreadCount' == $request.action)
  #set ($discard = $response.setHeader('Cache-Control', 'no-cache'))
    #set ($discard = $response.setHeader('Content-Type', 'application/json'))
    $jsontool.serialize({'unread': $services.notification.sources.getEventsCount(21)})
#********************************************************
             Mark a notification as read
********************************************************###
#elseif('get' == $xcontext.action && 'POST' == $request.method && 'read' == $request.action)
  #set ($eventIds = $request.eventIds.split(','))
  #set ($read = "$!request.read")
  #if ($eventIds.length == 0 || $read.isEmpty())
    #set ($discard = $response.setStatus(400))
  #else
    #foreach ($eventId in $eventIds)
      #set ($discard = $services.notification.saveEventStatus($eventId, $read.equals('true')))
    #end
  #end
#********************************************************
           Change the start date of the user
********************************************************###
#elseif('get' == $xcontext.action && 'POST' == $request.method && 'setStartDate' == $request.action)
  #set ($startDate = $datetool.date)
  #if ("$!request.date" != '')
    #set ($startDate = $xwiki.jodatime.getDateTime($numbertool.toNumber($request.date).longValue()).toDate())
  #end
  #set ($discard = $services.notification.preferences.setStartDate($startDate))
  #set ($discard = $services.notification.filters.setStartDate($startDate))
#********************************************************
           Clear all event status until a specific date for the user
********************************************************###
#elseif('get' == $xcontext.action && 'POST' == $request.method && 'clear' == $request.action)
  #set ($startDate = $datetool.date)
  #if ("$!request.date" != '')
    #set ($startDate = $xwiki.jodatime.getDateTime($numbertool.toNumber($request.date).longValue()).toDate())
  #end
  #set ($discard = $services.notification.preferences.setStartDate($startDate))
  #set ($discard = $services.notification.filters.setStartDate($startDate))
  #set ($discard = $services.notification.clearAllStatus($startDate))
#********************************************************
             Watch/Unwatch a location
********************************************************###
#elseif('get' == $xcontext.action && 'POST' == $request.method && ('watchLocation' == $request.action || 'unwatchLocation' == $request.action))
  #if ("$!request.type" == 'space')
    #set ($location = $services.model.resolveSpace($request.location))
  #elseif ("$!request.type" == 'wiki')
    #set ($location = $services.model.createWikiReference($request.location))
  #else
    #set ($location = $services.model.resolveDocument($request.location))
  #end
  #if ('watchLocation' == $request.action)
    #set ($discard = $services.notification.watch.watchLocation($location))
  #else
    #set ($discard = $services.notification.watch.unwatchLocation($location))
  #end
  ## Display the new states
  #if ("$!request.currentDoc" != '')
    #set ($currentDoc = $services.model.resolveDocument($request.currentDoc))
    #set ($states = {
      'document': $services.notification.watch.getLocationWatchedStatus($currentDoc),
      'space': $services.notification.watch.getLocationWatchedStatus($currentDoc.lastSpaceReference),
      'wiki': $services.notification.watch.getLocationWatchedStatus($currentDoc.wikiReference)
    })
    #set ($discard = $response.setContentType('application/json'))
    $jsontool.serialize($states)
  #end
#end
{{/velocity}}

