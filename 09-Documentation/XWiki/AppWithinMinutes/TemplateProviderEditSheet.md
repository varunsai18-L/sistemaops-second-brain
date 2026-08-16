---
id: xwiki-AppWithinMinutes.TemplateProviderEditSheet
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906702000
sync_date: 2026-08-16 19:45:21
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# TemplateProviderEditSheet

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906702000
- **Source:** [TemplateProviderEditSheet](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.TemplateProviderEditSheet)

---

{{include reference="XWiki.TemplateProviderMacros" /}}

{{include reference="AppWithinMinutes.VelocityMacros" /}}

{{velocity}}
#if ("$!request.wizard" == 'true')
  {{include reference="AppWithinMinutes.WizardStep" /}}
#end
{{/velocity}}

{{velocity output="false"}}
#set ($appDescriptorClassName = 'AppWithinMinutes.LiveTableClass')

#macro (updateHiddenTemplateProviderProperties)
  #set ($prefix = $stringtool.removeEnd($doc.documentReference.name, 'TemplateProvider'))
  #set ($discard = $doc.setTitle("$prefix Template Provider"))
  #set ($templateProviderObj = $doc.getObject('XWiki.TemplateProviderClass'))
  #set ($discard = $templateProviderObj.set('name', "${prefix.toLowerCase()}.entry.name"))
  #set ($discard = $templateProviderObj.set('template', $stringtool.removeEnd($doc.fullName, 'Provider')))
#end

#macro (initVisibleTemplateProviderProperties $templateProviderObj)
  #getAppReference
  #set ($localStringAppRef = $services.model.serialize($appReference, 'local'))
  #set ($icon = 'application')
  #foreach ($uix in $services.uix.getExtensions('org.xwiki.platform.panels.Applications'))
    #if ($uix.id == "platform.panels.${localStringAppRef}Application" && $uix.parameters.icon.startsWith('icon:'))
      ## Use the application icon by default if set.
      #set ($icon = $stringtool.removeStart($uix.parameters.icon, 'icon:'))
    #end
  #end
  #set ($discard = $templateProviderObj.set('icon', $icon))
  #set ($homePageRef = $services.model.resolveDocument('', 'default', $appReference))
  ## We recommend the users to create the entries in the application space by default because:
  ## * for most applications it's better to keep the entries in the same place
  ## * if the application is not yet created the application space doesn't exist so the user cannot select it from the
  ##   tree unless we select it by default
  #set ($creationRestrictions = [$services.model.serialize($appReference, 'local')])
  #set ($creationRestrictionsAreSuggestions = 1)
  #if ($xwiki.exists($homePageRef))
    ## We are (most probably) editing an existing application. Initialize the entry location based on the information
    ## stored on the application home page.
    #set ($dataSpace = $xwiki.getDocument($homePageRef).getValue('dataSpace'))
    #set ($dataSpaceReference = $services.model.resolveSpace($dataSpace, 'explicit', $appReference))
    #set ($creationRestrictions = [$services.model.serialize($dataSpaceReference, 'local')])
    #set ($creationRestrictionsAreSuggestions = 0)
    ## Preserve the old behavior.
    #set ($discard = $templateProviderObj.set('terminal', 1))
  #end
  #set ($discard = $templateProviderObj.set('creationRestrictions', $creationRestrictions))
  #set ($discard = $templateProviderObj.set('creationRestrictionsAreSuggestions', $creationRestrictionsAreSuggestions))
#end

#macro (maybeAddXRedirectToNextWizardStep)
  #if ("$!request.wizard" == 'true')
    ## Add redirect to next wizard step.
    #getAppReference
    #set ($homePageRef = $services.model.resolveDocument('', 'default', $appReference))
    #set ($queryString = {"wizard" : true})
    #if (!$xwiki.exists($homePageRef))
      #set ($classReference = "${stringtool.removeEnd($doc.fullName, 'TemplateProvider')}Class")
      #set ($wikiHomePageRef = $services.model.resolveDocument('', 'default'))
      #set ($wikiHomePage = $services.model.serialize($wikiHomePageRef, 'local'))
      #set ($discard = $queryString.putAll({
        'form_token': $services.csrf.getToken(),
        'template': 'AppWithinMinutes.LiveTableTemplate',
        "${appDescriptorClassName}_0_class": $classReference,
        'title': $appReference.name,
        'parent': $wikiHomePage
      }))
    #end
    #set ($queryString = $escapetool.url($queryString))
    <input type="hidden" name="xredirect" value="$escapetool.xml($xwiki.getURL($homePageRef, 'edit', $queryString))" />
  #end
#end

#macro (displayEditForm)
  #set ($discard = $xwiki.ssx.use('XWiki.TemplateProviderMacros'))
  #set ($discard = $xwiki.jsx.use('XWiki.TemplateProviderMacros'))
  #updateHiddenTemplateProviderProperties
  #if ($doc.isNew())
    #initVisibleTemplateProviderProperties($templateProviderObj)
  #end
  <div class="hidden">
    <input type="hidden" name="title" value="$escapetool.xml($doc.title)" />
    <input type="hidden" name="xhidden" value="1" />
    #foreach ($property in ['name', 'template', 'action'])
      #displayPropertyValue($property 'hidden')
    #end
    #maybeAddXRedirectToNextWizardStep
  </div>
  <div class="xform row templateProviderSheet">
    <div class="xHint col-xs-12">
      $services.icon.renderHTML('info')
      $services.localization.render('appWithinMinutes.templateProviderEditor.hint')
    </div>
    ##
    ## Left side
    ##
    <div class="col-xs-12 col-md-6">
      <dl>
        ##
        ## Icon
        ##
        <dt>
          <label for="XWiki.TemplateProviderClass_0_icon">
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.icon.name'))
          </label>
          <span class="xHint">
            $services.localization.render('appWithinMinutes.templateProviderEditor.icon.hint')
          </span>
        </dt>
        <dd>#displayPropertyValue('icon')</dd>
        ##
        ## Description
        ##
        <dt>
          <label for="XWiki.TemplateProviderClass_0_description">
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.description.name'))
          </label>
          <span class="xHint">
            $services.localization.render('appWithinMinutes.templateProviderEditor.description.hint')
          </span>
        </dt>
        <dd>#displayPropertyValue('description')</dd>
        ##
        ## Visibility Restrictions
        ##
        <dt>
          <label>
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.visibilityRestrictions.name'))
          </label>
          <span class="xHint">
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.visibilityRestrictions.hint'))
          </span>
        </dt>
        <dd>#displayPathsPropertyValue('visibilityRestrictions')</dd>
      </dl>
    </div>
    ##
    ## Right side
    ##
    <div class="col-xs-12 col-md-6">
      <dl>
        ##
        ## Creation Restrictions
        ##
        <dt>
          <label for="XWiki.TemplateProviderClass_0_creationRestrictions">
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.creationRestrictions.name'))
          </label>
          <span class="xHint">
            $services.localization.render('appWithinMinutes.templateProviderEditor.creationRestrictions.hint')
          </span>
        </dt>
        <dd>#displayPathsPropertyValue('creationRestrictions')</dd>
        ##
        ## Creation Restrictions As Suggestions
        ##
        <dt>
          <label for="XWiki.TemplateProviderClass_0_creationRestrictionsAreSuggestions">
            #displayPropertyValue('creationRestrictionsAreSuggestions')
            $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.creationRestrictionsAreSuggestions.name'))
          </label>
          <span class="xHint">
            $services.localization.render('appWithinMinutes.templateProviderEditor.creationRestrictionsAreSuggestions.hint')
          </span>
        </dt>
        <dd></dd>
        ##
        ## Terminal page creation - Advanced user
        ##
        #if ($isAdvancedUser || $isSuperAdmin)
          <dt>
            <label for="XWiki.TemplateProviderClass_0_terminal">
              $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.terminal.name'))
            </label>
            <span class="xHint">
              $escapetool.xml($services.localization.render('appWithinMinutes.templateProviderEditor.terminal.hint'))
            </span>
          </dt>
          <dd>#displayPropertyValue('terminal')</dd>
        #else
          <dd>#displayPropertyValue('terminal' 'hidden')</dd>
        #end
      </dl>
    </div>
    #locationPickerModal
  </div>
#end

#macro (doEdit)
  #if ("$!request.wizard" == 'true')
    #appWizardHeader('entries')
    ## Compute the application title to be used as the wizard step title.
    #getAppTitle
  #end
  #displayEditForm
  #if ("$!request.wizard" == 'true')
    #appWizardFooter('entries')
  #end
#end
{{/velocity}}

{{velocity}}
#if ($doc.getObject('XWiki.TemplateProviderClass'))
  {{html clean="false"}}
  #doEdit
  {{/html}}

  {{iconPicker id="XWiki.TemplateProviderClass_0_icon" prefix="" /}}
#end
{{/velocity}}
