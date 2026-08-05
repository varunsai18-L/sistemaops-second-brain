---
id: xwiki-xwiki:XWiki.TemplateProviderSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905863000
sync_date: 2026-07-21 11:01:10
tags:
  - xwiki/documentation
  - space/xwiki
---
# TemplateProviderSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905863000
- **Source:** [TemplateProviderSheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.TemplateProviderSheet)

---

{{include reference="XWiki.TemplateProviderMacros" /}}

{{velocity output="false"}}
#macro (initializeTemplateProvider)
  #if ($doc.documentReference.name.endsWith('Provider'))
    #set ($discard = $doc.set('template', $stringtool.removeEnd($doc.fullName, 'Provider').trim()))
    #set ($templateName = $stringtool.removeEnd($doc.documentReference.name, 'Provider').trim())
    #set ($templateName = $stringtool.join($stringtool.splitByCharacterTypeCamelCase($templateName), ' '))
    #set ($templateName = $templateName.replaceAll('\s+', ' '))
    #set ($discard = $doc.set('name', $templateName))
  #end
#end
{{/velocity}}

{{velocity}}
{{html clean="false"}}
#set ($discard = $xwiki.ssx.use('XWiki.TemplateProviderMacros'))
#set ($discard = $xwiki.jsx.use('XWiki.TemplateProviderMacros'))
#set ($discard = $doc.use('XWiki.TemplateProviderClass'))
#if ($doc.isNew())
  #initializeTemplateProvider
#end
<div class="xform row templateProviderSheet">
  ##
  ## Left side
  ##
  <div class="col-xs-12 col-md-6">
    <dl>
      ##
      ## Template Provider Title
      ##
      #if ($isEditing)
        <dt>
          <label for="title">
            $escapetool.xml($services.localization.render('xe.templateprovider.name'))
          </label>
        </dt>
        <dd>
          <input type="text" value="$!escapetool.xml($doc.title)" name="title" id="title" />
        </dd>
      #end
      ##
      ## Template Name
      ##
      <dt>
        <label#if ($isEditing) for="XWiki.TemplateProviderClass_0_name"#end>
          $escapetool.xml($services.localization.render('xe.templateprovider.templatename'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $escapetool.xml($services.localization.render('xe.templateprovider.templatename.info'))
          </span>
        #end
      </dt>
      <dd>
        #if ($isEditing)
          #displayPropertyValue('name')
        #else
          $!escapetool.xml($services.localization.render($doc.getValue('name')))
        #end
      </dd>
      ##
      ## Template Description
      ##
      <dt>
        <label#if ($isEditing) for="XWiki.TemplateProviderClass_0_description"#end>
          $escapetool.xml($services.localization.render('administration.templateProvider.description'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $services.localization.render('administration.templateProvider.description.hint')
          </span>
        #end
      </dt>
      <dd>
        #if ($isEditing)
          #displayPropertyValue('description')
        #else
          $!escapetool.xml($services.localization.render($doc.getValue('description')))
        #end
      </dd>
      ##
      ## Template Icon
      ##
      <dt>
        <label#if($isEditing) for="XWiki.TemplateProviderClass_0_icon"#end>
          $escapetool.xml($services.localization.render('administration.templateProvider.icon'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $services.localization.render('administration.templateProvider.icon.hint', ['', ''])
          </span>
        #end
      </dt>
      <dd>
        #if ($isEditing)
          #displayPropertyValue('icon')
        #else
          $!services.icon.renderHTML($doc.getValue('icon'))
        #end
      </dd>
      ##
      ## Visibility Restrictions
      ##
      <dt>
        <label>$escapetool.xml($services.localization.render('xe.templateprovider.spaces'))</label>
        #if ($isEditing)
          <span class="xHint">
            $escapetool.xml($services.localization.render('xe.templateprovider.spaces.info'))
          </span>
        #end
      </dt>
      <dd>
        #set ($visibilityRestrictions = $doc.getValue('visibilityRestrictions'))
        #if ($isEditing || ($visibilityRestrictions && $visibilityRestrictions.size() > 0))
          #displayPathsPropertyValue('visibilityRestrictions')
        #else
          $escapetool.xml($services.localization.render('xe.templateprovider.spaces.all'))
        #end
      </dd>
    </dl>
  </div>
  ##
  ## Right side
  ##
  <div class="col-xs-12 col-md-6">
    <dl>
      ##
      ## Template Reference
      ##
      <dt>
        <label#if ($isEditing) for="XWiki.TemplateProviderClass_0_template"#end>
          $escapetool.xml($services.localization.render('xe.templateprovider.template'))
        </label>
      </dt>
      <dd>
        #set ($template = $doc.getValue('template'))
        #if ($isEditing)
          #set ($pagePickerParams = {
            'id': "XWiki.TemplateProviderClass_0_template",
            'name': "XWiki.TemplateProviderClass_0_template",
            'value': "$!escapetool.xml($template)"
          })
          #pagePicker($pagePickerParams)
        #elseif ("$!template" != '')
          #set ($templateReference = $services.model.resolveDocument($template))
          #hierarchy($templateReference {
            'local': true,
            'selfIsActive': false
          })
        #end
      </dd>
      ##
      ## Creation Restrictions
      ##
      <dt>
        <label>
          $escapetool.xml($services.localization.render('administration.templateProvider.creationRestrictions'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $services.localization.render('administration.templateProvider.creationRestrictions.hint')
          </span>
        #end
      </dt>
      <dd>
        #set ($creationRestrictions = $doc.getValue('creationRestrictions'))
        #if ($isEditing || ($creationRestrictions && $creationRestrictions.size() > 0))
          #displayPathsPropertyValue('creationRestrictions')
        #else
          $escapetool.xml($services.localization.render('administration.templateProvider.creationRestrictions.none'))
        #end
      </dd>
      ##
      ## Creation Restrictions As Suggestions
      ##
      <dt>
        <label>
          #if ($isEditing)
            #displayPropertyValue('creationRestrictionsAreSuggestions')
          #end
          $escapetool.xml($services.localization.render('administration.templateProvider.creationRestrictionsAreSuggestions'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $services.localization.render('administration.templateProvider.creationRestrictionsAreSuggestions.hint')
          </span>
        #end
      </dt>
      <dd>
        #if (!$isEditing)
          #displayPropertyValue('creationRestrictionsAreSuggestions')
        #end
      </dd>
      ##
      ## Terminal page creation - Advanced user (both view and edit mode)
      ##
      #if ($isAdvancedUser || $isSuperAdmin)
        <dt>
          <label#if ($isEditing) for="XWiki.TemplateProviderClass_0_terminal"#end>
            $escapetool.xml($services.localization.render('xe.templateprovider.terminal'))
          </label>
          #if ($isEditing)
            <span class="xHint">
              $escapetool.xml($services.localization.render('xe.templateprovider.terminal.hint'))
            </span>
          #end
        </dt>
        <dd>#displayPropertyValue('terminal')</dd>
      #else
        <dd>#displayPropertyValue('terminal' 'hidden')</dd>
      #end
      ##
      ## Action
      ##
      <dt>
        <label#if ($isEditing) for="XWiki.TemplateProviderClass_0_action"#end>
          $escapetool.xml($services.localization.render('xe.templateprovider.action'))
        </label>
        #if ($isEditing)
          <span class="xHint">
            $escapetool.xml($services.localization.render('xe.templateprovider.action.info'))
          </span>
        #end
      </dt>
      <dd>#displayPropertyValue('action')</dd>
    </dl>
  </div>
  #locationPickerModal
</div>
{{/html}}

{{iconPicker id="XWiki.TemplateProviderClass_0_icon" prefix="" /}}

##
## Go back to the administration
##
#if (!$isEditing)
  (% class="buttonwrapper" %)
  [[{{translation key="xe.templateprovider.backtoadmin"/}}>>path:$xwiki.getURL($services.model.createDocumentReference('', 'XWiki', 'XWikiPreferences'), 'admin', 'section=Templates')]]
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
