---
id: xwiki-XWiki.TemplateProviderMacros
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905816000
sync_date: 2026-08-25 21:13:12
tags:
  - xwiki/documentation
  - space/xwiki
---
# TemplateProviderMacros

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905816000
- **Source:** [TemplateProviderMacros](https://wiki.systemaops.in/bin/view/XWiki/XWiki.TemplateProviderMacros)

---

{{template name="hierarchy_macros.vm" /}}

{{velocity output="false"}}
#set ($isEditing = $xcontext.action == 'edit')

#macro (displayPropertyValue $property $action)
  #if ($action)
    #set ($output = $doc.display($property, $action))
  #else
    #set ($output = $doc.display($property))
  #end
  #unwrapXPropertyDisplay($output)
#end

#macro (displayPathsPropertyValue $property)
  <ul class="paths">
    #set ($hierarchyOptions = {
      'local': true,
      'selfIsActive': false
    })
    #set ($paths = $doc.getValue($property))
    #foreach ($path in $paths)
      <li class="path">
        #if ($isEditing)
          <a href="#path-delete" class="path-delete">$services.icon.renderHTML('delete')</a>
          <input type="hidden" name="XWiki.TemplateProviderClass_0_$property"
            value="$escapetool.xml($path)" />
        #end
        #set ($spaceReference = $services.model.resolveSpace($path))
        #hierarchy($spaceReference $hierarchyOptions)
      </li>
    #end
    #if ($isEditing)
      ## This is used as a template on the client side when a new path is added.
      <li class="path hidden">
        <a href="#path-delete" class="path-delete">$services.icon.renderHTML('delete')</a>
        <input type="hidden" name="XWiki.TemplateProviderClass_0_$property" disabled="disabled" />
        <ol class="breadcrumb">
          <li class="loading"></li>
        </ol>
      </li>
      <li class="path-add">
        <input type="hidden" name="XWiki.TemplateProviderClass_0_$property" value="" />
        <a href="#path-add">$services.icon.renderHTML('add')</a>
      </li>
    #end
  </ul>
#end

#macro (locationPickerModal)
  <div class="location-picker modal fade" tabindex="-1" role="dialog" data-backdrop="static">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title">$services.localization.render('core.documentPicker.title')</div>
        </div>
        <div class="modal-body">
          #documentTree({
            'class': 'location-tree',
            'finder': true,
            'showAttachments': false,
            'showTerminalDocuments': false,
            'showTranslations': false
          })
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $services.localization.render('core.documentPicker.cancel')
          </button>
          <button type="button" class="btn btn-primary" disabled="disabled">
            $services.localization.render('core.documentPicker.select')
          </button>
        </div>
      </div>
    </div>
  </div>
#end
{{/velocity}}
