---
id: xwiki-xwiki:XWiki.ExportDocumentTree
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905788000
sync_date: 2026-07-21 11:01:03
tags:
  - xwiki/documentation
  - space/xwiki
---
# ExportDocumentTree

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905788000
- **Source:** [ExportDocumentTree](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.ExportDocumentTree)

---

{{velocity}}
#if ($xcontext.action != 'get')
  {{html clean="false"}}
  #template('export_macros.vm')
  #exportTreeSelector({
    'filter': 'pristineInstalledExtensionDocument',
    'root': "wiki:$xcontext.database"
  })
  {{/html}}
#end
{{/velocity}}

{{velocity}}
#if ($xcontext.action == 'get')
  {{include reference="XWiki.DocumentTreeMacros" /}}
#end
{{/velocity}}

{{velocity output="false"}}
#macro (postProcessDocumentTreeData $data)
  #if ($request.data == 'children')
    ## Change the icons in order to be able to differentiate content pages from extension pages and from customized
    ## extension pages.
    #foreach ($node in $data)
      #if ($node.data.type == 'document')
        #set ($documentReference = $services.model.resolveDocument($node.data.id))
        #set ($iconName = 'file-text')
        #set ($iconStyle = 'text-success')
        #if ($services.extension.xar.isExtensionDocument($documentReference))
          #if ($services.extension.xar.isCustomizedExtensionDocument($documentReference))
            #set ($iconName = 'file-code')
            #set ($iconStyle = 'text-warning')
            #if ($services.extension.xar.isEditAllowed($documentReference))
              ## Distinguish safe modifications (e.g. configuration) from unsafe modifications (code).
              #set ($iconStyle = 'text-success')
            #end
            #if ($request.filters == 'installedExtensionDocument')
              ## This node is visible probably because it has some child content pages, but the user should not be able
              ## to select it with the current filter.
              #set ($node.state = {'disabled': true, 'undetermined': true})
            #end
          #else
            #set ($iconName = 'file-white')
            #set ($iconStyle = 'text-danger')
            #if ($request.filters == 'pristineInstalledExtensionDocument'
                || $request.filters == 'installedExtensionDocument')
              ## This node is visible probably because it has some child content pages or child customized extension
              ## pages, but the user should not be able to select it with the current filter.
              #set ($node.state = {'disabled': true, 'undetermined': true})
            #end
          #end
          ## Show the extension name and id as a tool tip for the tree node.
          #set ($installedExtensions = $services.extension.xar.getInstalledExtensions($documentReference))
          #set ($tooltip = [])
          #foreach ($installedExtension in $installedExtensions)
            #set ($discard = $tooltip.add("$installedExtension.name ($installedExtension.id)"))
          #end
          #if ($tooltip.size() > 0)
            #set ($node.a_attr.title = $stringtool.join($tooltip, ', '))
          #end
        #end
        #set ($iconMetaData = $services.icon.getMetaData($iconName))
        #if ($iconMetaData.iconSetType == 'IMAGE')
          #set ($node.icon = $iconMetaData.url)
        #elseif ($iconMetaData.iconSetType == 'FONT')
          #set ($node.icon = "$iconMetaData.cssClass $iconStyle")
        #end
      #elseif ($node.data.type == 'empty')
        #set ($node.state = {'disabled': true, 'selected': false})
        #set ($node.a_attr = {'class': 'jstree-no-checkboxes'})
      #end
    #end
  #end
#end
{{/velocity}}

{{velocity}}
#if ($xcontext.action == 'get')
  #updateDocTreeConfigFromRequest
  #handleDocumentTreeRequest
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
