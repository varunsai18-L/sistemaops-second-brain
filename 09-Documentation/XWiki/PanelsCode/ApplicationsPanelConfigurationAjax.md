---
id: xwiki-PanelsCode.ApplicationsPanelConfigurationAjax
type: XWiki Page
space: "PanelsCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907274000
sync_date: 2026-08-25 21:14:14
tags:
  - xwiki/documentation
  - space/panelscode
---
# ApplicationsPanelConfigurationAjax

- **Space:** PanelsCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907274000
- **Source:** [ApplicationsPanelConfigurationAjax](https://wiki.systemaops.in/bin/view/PanelsCode/PanelsCode.ApplicationsPanelConfigurationAjax)

---

{{velocity}}
#if($xcontext.action=='get' && $request.outputSyntax == 'plain')
  #if(!$services.csrf.isTokenValid($request.form_token))
  BAD CSRF
  #elseif(!$xwiki.hasAccessLevel('edit', $xcontext.user, 'PanelsCode.ApplicationsPanelConfiguration'))
  NO RIGHT
  #else
    ## Get the blacklist configuration
    #set($configDoc = $xwiki.getDocument($services.model.createDocumentReference('', 'PanelsCode', 'ApplicationsPanelConfiguration')))
    ## Get the desired blacklist
    #set($list = $jsontool.fromString($request.blacklist))
    #foreach($app in $list)
      #set($blackListObj = $configDoc.getObject('PanelsCode.ApplicationsPanelBlackListClass', 'applicationId', $app))
      #if(!$blackListObj)
        #set($blackListObj = $configDoc.newObject('PanelsCode.ApplicationsPanelBlackListClass'))
        #set($discard = $blackListObj.set('applicationId', $app))
      #end
    #end
    #foreach($obj in $configDoc.getObjects('PanelsCode.ApplicationsPanelBlackListClass').clone())
      #set($app = $obj.getValue('applicationId'))
      #if(!$list.contains($app))
        #set($discard = $configDoc.removeObject($obj))
      #end
    #end
    ## Get the orderlist configuration
    #set ($list = $jsontool.fromString($request.orderlist))
    #foreach ($app in $list)
      #set ($orderObj = $configDoc.getObject('PanelsCode.ApplicationsPanelOrderClass', 'applicationId', $app))
      #if (!$orderObj)
        #set ($orderObj = $configDoc.newObject('PanelsCode.ApplicationsPanelOrderClass'))
        #set ($discard = $orderObj.set('applicationId', $app))
      #end
      #set ($discard = $orderObj.set('order', $foreach.count))
    #end
    ## Remove the order objects that are not set
    #foreach($obj in $configDoc.getObjects('PanelsCode.ApplicationsPanelOrderClass').clone())
      #set($app = $obj.getValue('applicationId'))
      #if(!$list.contains($app))
        #set($discard = $configDoc.removeObject($obj))
      #end
    #end
    #set($discard = $configDoc.setHidden(true))
    #set($discard = $configDoc.save("Save the new configuration"))
    SUCCESS
  #end
#end
{{/velocity}}

