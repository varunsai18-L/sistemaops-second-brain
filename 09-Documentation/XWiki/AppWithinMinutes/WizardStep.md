---
id: xwiki-AppWithinMinutes.WizardStep
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906777000
sync_date: 2026-08-25 21:13:49
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# WizardStep

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906777000
- **Source:** [WizardStep](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.WizardStep)

---

{{velocity output="false"}}
#set ($awmSteps = ['name', 'structure', 'entries', 'presentation'])

#macro (appWizardHeader $stepId)
  <div class="wizard-header">
    #set ($stepNumber = $awmSteps.indexOf($stepId) + 1)
    #set ($stepTitle = $services.localization.render("appWithinMinutes.wizardStep.${stepId}.title"))
    <h2>$services.localization.render('platform.appwithinminutes.wizardStepHeading', [$stepNumber, $stepTitle])</h2>
    <ul class="steps">
      #foreach ($step in $awmSteps)
        #set ($index = $foreach.index + 1)
        #set ($extraClassName = "#if ($stepNumber == $index) step-active#elseif ($stepNumber > $index) step-done#end")
        <li>
          <span class="btn btn-xs number$extraClassName">
            #if ($stepNumber > $index)
              $services.icon.renderHTML('check')
            #else
              $index
            #end
          </span>
          <span class="name$extraClassName">
            $services.localization.render("appWithinMinutes.wizardStep.${step}.name")
          </span>
        </li>
      #end
    </ul>
    <div class="clearfloats"></div>
  </div>
#end

#macro (appWizardFooter $stepId)
  <div class="wizard-footer buttons">
    #set ($nextLabel = $services.localization.render('platform.appwithinminutes.wizardStepNextButtonLabel'))
    #set ($nextTip = $services.localization.render('platform.appwithinminutes.wizardStepNextButtonTip'))
    #if ($stepId == 'presentation')
      #set ($nextLabel = $services.localization.render('platform.appwithinminutes.wizardStepFinishButtonLabel'))
      #set ($nextTip = $services.localization.render('platform.appwithinminutes.wizardStepFinishButtonTip'))
      #set ($templateProviderReference = "$stringtool.removeEnd($classReference, 'Class')TemplateProvider")
      #set ($previousURL = $xwiki.getURL($templateProviderReference, 'edit',
        'wizard=true&sheet=AppWithinMinutes.TemplateProviderEditSheet'))
    #elseif ($stepId == 'entries')
      #set ($classReference = "$stringtool.removeEnd($doc.fullName, 'TemplateProvider')Class")
      #set ($previousURL = $xwiki.getURL($classReference, 'edit', 'wizard=true'))
    #elseif ($stepId == 'structure' && $doc.isNew())
      #set ($previousURL = $xwiki.getURL('AppWithinMinutes.CreateApplication', 'view', 'wizard=true'))
    #end
    #if ($previousURL)
      <span class="buttonwrapper left">
        <a href="$previousURL" class="button secondary" title="$escapetool.xml($services.localization.render(
          'platform.appwithinminutes.wizardStepPreviousButtonTip'))">$escapetool.xml($services.localization.render(
          'platform.appwithinminutes.wizardStepPreviousButtonLabel'))</a>
      </span>
    #end
    <span class="buttonwrapper">
      <input type="submit" id="wizard-next" name="xaction_save" value="$escapetool.xml($nextLabel)"
        title="$escapetool.xml($nextTip)" class="button"/>
    </span>
  </div>
#end
{{/velocity}}

{{velocity}}
#if ($doc.fullName == 'AppWithinMinutes.WizardStep')
  Code shared by all AppWithinMinutes wizard steps.
#else
  ## Use the style sheet and the JavaScript code required by the velocity macros previously defined.
  #set ($discard = $xwiki.ssfx.use('uicomponents/wizard/wizard.css', true))
  #set ($discard = $xwiki.jsx.use('AppWithinMinutes.WizardStep'))
#end
{{/velocity}}
