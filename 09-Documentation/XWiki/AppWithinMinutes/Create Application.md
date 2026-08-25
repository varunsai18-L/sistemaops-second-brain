---
id: xwiki-AppWithinMinutes.CreateApplication
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906739000
sync_date: 2026-08-25 21:13:36
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Create Application

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906739000
- **Source:** [Create Application](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.CreateApplication)

---

{{include reference="AppWithinMinutes.VelocityMacros"/}}

{{velocity}}
#if ($request.wizard == 'true')
  {{include reference="AppWithinMinutes.WizardStep"/}}
#end
{{/velocity}}

{{template name="locationPicker_macros.vm" /}}

{{velocity output="false"}}
#macro (showStep)
  #appWizardHeader('name')
  <div class="wizard-help">
    <p>
      <strong>$services.localization.render('platform.appwithinminutes.wizardStepHelpTitle')</strong>
      $services.localization.render('platform.appwithinminutes.wizardStepHelpDescription')
    </p>
    <ul class="steps vertical">
      #foreach($step in $awmSteps)
        <li>
          <span class="btn btn-xs number">$mathtool.add($foreach.index, 1)</span>
          <span class="name">$services.localization.render("appWithinMinutes.wizardStep.${step}.name")</span>
          <span class="description">$services.localization.render("appWithinMinutes.wizardStep.${step}.description")</span>
        </li>
      #end
    </ul>
  </div>
  <form action="$doc.getURL()" method="post" class="xform wizard-body">
    <fieldset>
      #locationPicker({
        'id': 'app',
        'title': {
          'label': 'platform.appwithinminutes.appNameLabel',
          'hint': 'platform.appwithinminutes.appNameHint',
          'name': 'appName'
        },
        'preview': {
          'label': 'appWithinMinutes.createApp.location.label',
          'hint': 'appWithinMinutes.createApp.location.hint'
        },
        'parent': {
          'label': 'appWithinMinutes.createApp.parent.label',
          'hint': 'appWithinMinutes.createApp.parent.hint',
          'name': 'appParentReference',
          'reference': $doc.documentReference.wikiReference,
          'placeholder': 'appWithinMinutes.createApp.parent.placeholder'
        }
      })
      <div class="appName-preview"></div>
      #appWizardFooter(1)
    </fieldset>
  </form>
#end

#macro (processStep)
  ## Check if the application already exists.
  #getAppReference
  #getAppDescriptor($appReference)
  #if ($appDescriptor)
    ## Edit an existing application.
    #getAppClassReference($appDescriptor)
    #set ($appClassRef = $classReference)
  #else
    ## Create a new application. Use the default class name.
    #set ($appCodeRef = $services.model.createSpaceReference('Code', $appReference))
    #set ($appClassRef = $services.model.createDocumentReference("$!{appReference.name}Class", $appCodeRef))
  #end
  #set ($queryString = {'wizard': true})
  #if (!$xwiki.exists($appClassRef))
    #set ($appHomeRef = $services.model.resolveDocument('', 'default', $appReference))
    #set ($discard = $queryString.putAll({
      'form_token': $services.csrf.getToken(),
      'template': 'AppWithinMinutes.ClassTemplate',
      'parent': $services.model.serialize($appHomeRef),
      'title': "$appReference.name Class"
    }))
  #end
  $response.sendRedirect($xwiki.getURL($appClassRef, 'edit', $escapetool.url($queryString)))
#end

#macro (validateAppName)
  #getAppReference
  #if (!$appReference)
    <span class="xErrorMsg">$services.localization.render('platform.appwithinminutes.appNameEmptyError')</span>
  #else
    #getAppDescriptor($appReference)
    #if ($appDescriptor)
      ## Edit an existing application.
      #getAppClassReference($appDescriptor)
      #set ($appClassRef = $classReference)
    #else
      ## Create a new application.
      #set ($appCodeRef = $services.model.createSpaceReference('Code', $appReference))
      #set ($appClassRef = $services.model.createDocumentReference("$!{appReference.name}Class", $appCodeRef))
    #end
    <dl>
      <dt>$services.localization.render('platform.appwithinminutes.appNamePreviewHomePageUrlLabel')</dt>
      <dd><pre>$!escapetool.xml($xwiki.getDocument($appReference).externalURL)</pre></dd>
      <dt>$services.localization.render('platform.appwithinminutes.appNamePreviewCodeSpaceLabel')</dt>
      <dd>#hierarchy($appClassRef.parent)</dd>
    </dl>
    #set ($appHomeRef = $services.model.resolveDocument('', 'default', $appReference))
    #if ($appDescriptor || $xwiki.exists($appHomeRef) || $xwiki.exists($appClassRef))
      #warning($services.localization.render('platform.appwithinminutes.appNameIsUsedWarning'))
    #end
    #if (!$services.security.authorization.hasAccess('script', $xcontext.userReference, $appHomeRef))
      #error($escapetool.xml($services.localization.render('platform.appwithinminutes.appHomePageNoScriptRight')))
    #end
  #end
#end

#macro (getAppReference)
  #if ($request.resolve == 'true')
    #set ($appReference = $services.model.resolveSpace($request.appName))
  #elseif ("$!request.appName" != '')
    #set ($parentReference = $doc.documentReference.wikiReference)
    #if ("$!request.appParentReference" != '')
      #set ($parentReference = $services.model.resolveSpace($request.appParentReference))
    #end
    #set ($appReference = $services.model.createSpaceReference($request.appName, $parentReference))
  #else
    #set ($appReference = $NULL)
  #end
#end

#macro (getAppDescriptor $appReference)
  #set ($appDescriptorClassName = 'AppWithinMinutes.LiveTableClass')
  #set ($appDescriptorStatement = "from doc.object($appDescriptorClassName) as obj where doc.space = :space")
  #set ($localSpaceReference = $services.model.serialize($appReference, 'local'))
  #set ($appDescriptors = $services.query.xwql($appDescriptorStatement).bindValue('space', $localSpaceReference).execute())
  #if ($appDescriptors.size() > 0)
    #set ($appDescriptor = $xwiki.getDocument($appDescriptors.get(0)))
  #else
    #set ($appDescriptor = $NULL)
  #end
#end
{{/velocity}}

{{velocity}}
{{html clean="false"}}
#if ("$!request.appName" != '')
  #if ($xcontext.action == 'get')
    #validateAppName
  #else
    ## CSRF protection is not needed because this step only redirects to the next one passing data in the query string.
    #processStep
  #end
#elseif ($request.wizard == 'true')
  #showStep
  #set ($displayDocExtra = false)
#end
{{/html}}
{{/velocity}}
