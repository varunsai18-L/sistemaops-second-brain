---
id: xwiki-PanelsCode.ApplicationsPanelConfigurationSheet
type: XWiki Page
space: "PanelsCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907249000
sync_date: 2026-08-25 21:14:11
tags:
  - xwiki/documentation
  - space/panelscode
---
# ApplicationsPanelConfiguration Sheet

- **Space:** PanelsCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907249000
- **Source:** [ApplicationsPanelConfiguration Sheet](https://wiki.systemaops.in/bin/view/PanelsCode/PanelsCode.ApplicationsPanelConfigurationSheet)

---

{{velocity}}
##########################
## JAVASCRIPT/CSS
##########################
#set($discard = $xwiki.jsx.use('PanelsCode.ApplicationsPanelConfigurationSheet'))
#set($discard = $xwiki.ssx.use('PanelsCode.ApplicationsPanelConfigurationSheet'))
##########################
## First, we split the applications in 2 categories (white listed/black listed)
##########################
#set($displayedApps = [])
#set($blacklistedApps = [])
#if($doc.fullName == 'XWiki.XWikiPreferences')
  #set($configDoc = $xwiki.getDocument($services.model.createDocumentReference('', 'PanelsCode', 'ApplicationsPanelConfiguration')))
#else
  #set($configDoc = $doc)
#end
#foreach($uix in $services.uix.getExtensions('org.xwiki.platform.panels.Applications', {'sortByParameter' : 'label'}))
  #if("$!configDoc.getObject('PanelsCode.ApplicationsPanelBlackListClass', 'applicationId', $uix.id)" != '')
    #set($discard = $blacklistedApps.add({'uix': $uix}))
  #else
    #set ($app = {'uix': $uix})
    #set ($orderObj = $configDoc.getObject('PanelsCode.ApplicationsPanelOrderClass', 'applicationId', $uix.id))
    #if ($orderObj)
      #set ($discard = $app.put('order', $orderObj.getValue('order')))
    #else
      ## if order is not set, set MAX_INTEGER
      #set ($discard = $app.put('order', 2147483647))
    #end
    #set ($discard = $displayedApps.add($app))
  #end
#end
## Sort the displayedApp
#set ($displayedApps = $collectiontool.sort($displayedApps, 'order'))
##########################
## Macro to display an application panel
##########################
#macro(showAppPanel $id $title $class $apps)

  {{html}}
    <div class="col-xs-12 col-md-6">
      <div class="panel-width-Small panel $!class appsPanel" id="$id">
        <div class="panel-heading">
          <h2>$title</h2>
        </div>
        <div class="panel-body">
          <ul class="nav nav-pills applicationsPanel">
            #foreach($app in $apps)
              #set($params = $app.uix.getParameters())
              #set($normalizedIcon = $stringtool.substringBefore($!params.icon, ' '))
              #if("$!normalizedIcon" != '' && "$!params.label" != '' && "$!params.target" != '' && $xwiki.hasAccessLevel('view', $xcontext.user, $params.target))
                #if ($normalizedIcon.startsWith('icon:'))
                  #set($icon = $services.icon.renderHTML($normalizedIcon.substring(5)))
                #else
                  #set($icon = $services.rendering.render($services.rendering.parse("image:${normalizedIcon}", 'xwiki/2.1'), 'xhtml/1.0'))
                #end
                <li class="draggableApp" id="$escapetool.xml($app.uix.id)">
                  <a><span class="application-img">$icon </span> <span class="application-label">$escapetool.xml($params.label)</a>
                </li>
              #end
            #end
          </ul>
        </div>
      </div>
    </div>
  {{/html}}
#end
##########################
## Display the information message
##########################
(% class="noitems" %)
{{translation key="platform.panels.applications.helper" /}}
##########################
## Display the 2 panels
##########################
(% class="row appLists" %)
(((
  #showAppPanel('displayedPanels', $services.localization.render('platform.panels.applications.displayedapps'), 'panel-primary', $displayedApps)
  #showAppPanel('blacklistedPanels', $services.localization.render('platform.panels.applications.blacklistedapps'), 'panel-info', $blacklistedApps)
)))
##########################
## Display the buttons
##########################
{{html}}
<button class="btn btn-primary" id="bt-save">$services.localization.render('platform.panels.applications.save')</button> <button class="btn btn-default" id="bt-revert">$services.localization.render('platform.panels.applications.revert')</button>
{{/html}}
{{/velocity}}

