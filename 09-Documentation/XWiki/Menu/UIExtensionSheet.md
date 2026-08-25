---
id: xwiki-Menu.UIExtensionSheet
type: XWiki Page
space: "Menu"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907320000
sync_date: 2026-08-25 21:14:16
tags:
  - xwiki/documentation
  - space/menu
---
# UIExtensionSheet

- **Space:** Menu
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907320000
- **Source:** [UIExtensionSheet](https://wiki.systemaops.in/bin/view/Menu/Menu.UIExtensionSheet)

---

{{velocity}}
#macro (displayExtensionPointTitle $id)
  #set ($shortId = $stringtool.removeStart($id, 'org.xwiki.platform.'))
  #set ($shortId = $stringtool.removeStart($shortId, 'platform.'))
  #if ("$!shortId" != '')
    $escapetool.xml($services.localization.render("menu.uix.extensionPoint.value.$shortId"))
  #else
    $escapetool.xml($services.localization.render('menu.uix.extensionPoint.value.nowhere'))
  #end
#end
##
##
#set ($discard = $doc.use('XWiki.UIExtensionClass'))
#set ($uixObject = $doc.getObject('XWiki.UIExtensionClass'))
#set ($selectedExtensionPointId = $uixObject.getProperty('extensionPointId').value)
#if ($xcontext.action == 'edit')
  #set ($discard = $xwiki.jsx.use('Menu.UIExtensionSheet'))
  ## Prepare the extension point map.
  #set ($menuPanel = "{{velocity}}
    ${escapetool.h}panelheader(""$doc.plainTitle"")
    {{menu type=""vertical collapsible open""
      label=""$escapetool.velocity($services.rendering.escape($doc.plainTitle, 'xwiki/2.1'))""}}{{include
      reference=""${escapetool.d}uix.doc.documentReference"" /}}
    {{/menu}}
    ${escapetool.h}panelfooter()
    {{/velocity}}")
  #set ($menuBar = "{{velocity}}
    ${escapetool.h}if (${escapetool.d}xwiki.hasAccessLevel('view', ${escapetool.d}xcontext.user, ${escapetool.d}uix.doc.documentReference))
      {{menu type=""horizontal fixedWidth""
       id=""menu-horizontal-$doc.fullName.replaceAll('[\s|,|.|:|\[|\]|\[\/\]|\[\\\]|=|@|#]', '-')""
       label=""$escapetool.velocity($services.rendering.escape($doc.plainTitle, 'xwiki/2.1'))""}}{{include reference=""${escapetool.d}uix.doc.documentReference"" /}}{{/menu}}
    ${escapetool.h}end
    {{/velocity}}")
  #set ($extensionPoints = {
    'org.xwiki.platform.template.header.after': $menuBar,
    'platform.panels.rightPanels': $menuPanel,
    'platform.panels.leftPanels': $menuPanel
  })
  #set ($selectedContent = $uixObject.getProperty('content').value)
  #if (("$!selectedExtensionPointId" != '' && !$extensionPoints.containsKey($selectedExtensionPointId))
    || ("$!selectedContent" != '' && !$extensionPoints.containsValue($selectedContent)))
    ## Either custom extension point or custom content for a known extension point.
    #set ($discard = $extensionPoints.put($selectedExtensionPointId, $selectedContent))
  #end
#end
(% class="xform" %)
(((
  ; {{html wiki="true"}}<label#if ($xcontext.action == 'edit') for="XWiki.UIExtensionClass_0_extensionPointId"#end>{{translation key="menu.uix.extensionPoint.label"/}}</label>{{/html}}##
    (% class="xHint" %){{translation key="menu.uix.extensionPoint.hint"/}}
  #if ($xcontext.action == 'edit')
    : {{html}}<select id="XWiki.UIExtensionClass_0_extensionPointId" name="XWiki.UIExtensionClass_0_extensionPointId">
        <option value="">$services.localization.render('menu.uix.extensionPoint.value.nowhere')</option>
        #foreach ($extensionPointId in $extensionPoints.keySet())
          #set ($selected = $extensionPointId == $selectedExtensionPointId)
          <option value="$escapetool.xml($extensionPointId)"#if ($selected) selected="selected"#end>
            #displayExtensionPointTitle($extensionPointId)
          </option>
        #end
      </select>{{/html}}
  #else
    : #displayExtensionPointTitle($selectedExtensionPointId)
  #end
  ##
  ##
  #if ($xcontext.action == 'edit')
    ; {{html wiki="true"}}<label for="XWiki.UIExtensionClass_0_content">{{translation key="menu.uix.content.label"/}}</label>{{/html}}##
      (% class="xHint" %){{translation key="menu.uix.content.hint"/}}
    : {{html}}<select id="XWiki.UIExtensionClass_0_content" name="XWiki.UIExtensionClass_0_content">
        <option value="">$services.localization.render('menu.uix.extensionPoint.value.nowhere')</option>
        #foreach ($entry in $extensionPoints.entrySet())
          #set ($value = $escapetool.xml($entry.value).replaceAll("\r", '&#13;').replaceAll("\n", '&#10;'))
          #set ($selected = $entry.value == $selectedContent)
          <option value="$value"#if ($selected) selected="selected"#end>
            #displayExtensionPointTitle($entry.key)
          </option>
        #end
      </select>{{/html}}
  #end
  ##
  ##
  ; {{html wiki="true"}}<label#if ($xcontext.action == 'edit') for="XWiki.UIExtensionClass_0_scope"#end>{{translation key="menu.uix.scope.label"/}}</label>{{/html}}##
    (% class="xHint" %){{translation key="menu.uix.scope.hint"/}}
  : $doc.display('scope')
)))

#set ($discard = $doc.set('name', $doc.fullName))
#if ($xcontext.action == 'edit')
  (% class="hidden" %)(((
    $doc.display('name', 'hidden')
  )))
#end
{{/velocity}}
