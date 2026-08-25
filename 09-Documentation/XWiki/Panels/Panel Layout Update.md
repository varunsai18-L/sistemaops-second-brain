---
id: xwiki-Panels.PanelLayoutUpdate
type: XWiki Page
space: "Panels"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906840000
sync_date: 2026-08-25 21:13:58
tags:
  - xwiki/documentation
  - space/panels
---
# Panel Layout Update

- **Space:** Panels
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906840000
- **Source:** [Panel Layout Update](https://wiki.systemaops.in/bin/view/Panels/Panels.PanelLayoutUpdate)

---

{{velocity}}
#set ($place = $request.place)
##
## Get the preferences document where the new layout must be saved (XWiki.XWikiPreferences or Space.WebPreferences)
##
#if ("$!{request.prefsdoc}" != '')
  #set ($prefsdocument = $request.prefsdoc)
#else
  #set ($prefsdocument = 'XWiki.XWikiPreferences')
#end
##
## Check to see if the current user has admin rights on the current preferences document.
##
#if (!$xwiki.hasAccessLevel('admin', $xcontext.user, $prefsdocument))
  {{html clean="false"}}
  #xwikimessageboxstart($services.localization.render('panelwizard.placemanager') $services.localization.render('panelwizard.notadmininplace', [$escapetool.html($place)]))
  #xwikimessageboxend()
  {{/html}}
#elseif ("$!request.xpage" == 'plain')
  ## Set the current panel layout.
  #if ("$!place" == '')
    #set ($prefsdoc = $xwiki.getDocument($prefsdocument))
  #else
    #set ($prefsdoc = $xwiki.getDocument("${place}:${prefsdocument}"))
  #end
  #set ($discard = $prefsdoc.use('XWiki.XWikiPreferences'))
  #set ($leftPanels = $request.leftPanels)
  #set ($rightPanels = $request.rightPanels)
  #set ($showLeftPanels = $request.showLeftPanels)
  #set ($showRightPanels = $request.showRightPanels)
  #set ($leftPanelsWidth = $request.leftPanelsWidth)
  #set ($rightPanelsWidth = $request.rightPanelsWidth)
  #if ($leftPanels)
    #set ($discard = $prefsdoc.set('leftPanels', $leftPanels))
  #end
  #if ($showLeftPanels)
    #set ($discard = $prefsdoc.set('showLeftPanels', $showLeftPanels))
  #end
  #if ($leftPanelsWidth)
    #set ($discard = $prefsdoc.set('leftPanelsWidth', $leftPanelsWidth))
  #end
  #if ($rightPanels)
    #set ($discard = $prefsdoc.set('rightPanels', $rightPanels))
  #end
  #if ($showRightPanels)
    #set ($discard = $prefsdoc.set('showRightPanels', $showRightPanels))
  #end
  #if ($rightPanelsWidth)
    #set ($discard = $prefsdoc.set('rightPanelsWidth', $rightPanelsWidth))
  #end
  #if (${services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
    #set ($ok = $prefsdoc.save($services.localization.render('panelwizard.save.versionComment', true)))
  #else
    ## CSRF protection
    $response.sendRedirect("$!{services.csrf.getResubmissionURL()}")
  #end
  SUCCESS
#else

= $services.localization.render('panelwizard.panellayoutupdate') =

{{warning}}$services.localization.render('panelwizard.nodirectaccess', ['[[Panel Wizard>>Panels.PanelWizard]]']){{/warning}}
#end
{{/velocity}}
