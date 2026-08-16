---
id: xwiki-AppWithinMinutes.LiveTableEditSheet
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906725000
sync_date: 2026-08-16 20:01:50
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# LiveTableEditSheet

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906725000
- **Source:** [LiveTableEditSheet](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.LiveTableEditSheet)

---

{{include reference="XWiki.TemplateProviderMacros" /}}

{{include reference="AppWithinMinutes.VelocityMacros" /}}

{{velocity output="false"}}
#macro (listAvailableColumns $classReference)
  <select id="availableColumns" aria-describedby='availableColumnsHint'>
    #set ($classFields = $xwiki.getDocument($classReference).getxWikiClass().properties)
    #if ($classFields.size() > 0)
      <optgroup label="$escapetool.xml($services.localization.render(
          'platform.appwithinminutes.liveTableEditorClassFieldColumnGroupLabel'))" id="classFields">
        #foreach ($field in $classFields)
          <option value="$field.name">$escapetool.xml($field.translatedPrettyName)</option>
        #end
      </optgroup>
    #end
    <optgroup label="$escapetool.xml($services.localization.render(
        'platform.appwithinminutes.liveTableEditorGenericColumnGroupLabel'))">
      #foreach ($entry in $genericColumns.entrySet())
        <option value="$entry.key" title="$escapetool.xml($entry.value.get(1))">
          $escapetool.xml($entry.value.get(0))
        </option>
      #end
    </optgroup>
  </select>
  <a href="#addColumn" class="addColumn" title="$services.localization.render(
    'platform.appwithinminutes.liveTableEditorAddColumnHint')">$services.icon.renderHTML('add')</a>
#end

#macro (displayHelpPanel)
  #set ($genericColumns = {
    'doc.title': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocTitleColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocTitleColumnDescription')
    ],
    'doc.name': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocNameColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocNameColumnDescription')
    ],
    'doc.location': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocLocationColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocLocationColumnDescription')
    ],
    'doc.author': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocAuthorColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocAuthorColumnDescription')
    ],
    'doc.creator': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocCreatorColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocCreatorColumnDescription')
    ],
    'doc.date': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocDateColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocDateColumnDescription')
    ],
    'doc.creationDate': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocCreationDateColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorDocCreationDateColumnDescription')
    ],
    '_actions': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorActionsColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorActionsColumnDescription')
    ],
    '_attachments': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorAttachmentsColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorAttachmentsColumnDescription')
    ],
    '_images': [
      $services.localization.render('platform.appwithinminutes.liveTableEditorImagesColumnName'),
      $services.localization.render('platform.appwithinminutes.liveTableEditorImagesColumnDescription')
    ]
  })
  <div class="wizard-help">
    <p>
      <strong>$services.localization.render('platform.appwithinminutes.liveTableEditorHelpTitle')</strong>
      $services.localization.render('platform.appwithinminutes.liveTableEditorHelpDescription')
    </p>
    <dl>
      #foreach ($columnId in ['doc.title', 'doc.location', 'doc.date', 'doc.author', '_actions'])
        <dt>$genericColumns.get($columnId).get(0)</dt>
        <dd>$genericColumns.get($columnId).get(1)</dd>
      #end
    </dl>
  </div>
#end

#macro (displayFormFields)
  <div class="hidden">
    ## Make sure that only the sheet content is rendered when the class is saved using AJAX.
    <input type="hidden" name="xpage" value="plain" />
    ## We prevent the class name and the data space from being edited directly. They can be specified in the URL.
    #getAppClassReference($doc)
    <input type="hidden" name="AppWithinMinutes.LiveTableClass_0_class"
      value="$escapetool.xml($services.model.serialize($classReference, 'local'))" />
    #displayPropertyValue('dataSpace', 'hidden')
    ## We have to pass the list of available columns to the JavaScript code.
    #listAvailableColumns($classReference)
  </div>
  <dl>
    <dt>
      <label for="xwikidoctitleinput">$services.localization.render('core.editors.content.titleField.label')</label>
      <span class="xHint">$services.localization.render('platform.appwithinminutes.liveTableEditorTitleHint')</span>
    </dt>
    <dd><input id="xwikidoctitleinput" type="text" name="title" value="$escapetool.xml($doc.title)"/></dd>
    <dt>
      <label for="AppWithinMinutes.LiveTableClass_0_description">
        $doc.displayPrettyName('description', false, false)
      </label>
      <span class="xHint">
        $services.localization.render('platform.appwithinminutes.liveTableEditorDescriptionHint')
      </span>
    </dt>
    <dd>#displayPropertyValue('description')</dd>
    <dt>
      <label id='availableColumnsLabel' for="AppWithinMinutes.LiveTableClass_0_columns">$doc.displayPrettyName('columns', false, false)</label>
      <span id='availableColumnsHint' class="xHint">$services.localization.render('platform.appwithinminutes.liveTableEditorColumnsHint')</span>
    </dt>
    <dd>#displayPropertyValue('columns')</dd>
  </dl>
#end

#macro (getApplicationIcon $classReference)
  #set ($applicationIcon = '')
  ## Look for the corresponding UI extension.
  #set ($uixPointId = 'org.xwiki.platform.panels.Applications')
  #set ($uixObject = $doc.getObject('XWiki.UIExtensionClass', 'extensionPointId', $uixPointId))
  #set ($uixId = $uixObject.getValue('name'))
  #foreach ($uix in $services.uix.getExtensions($uixPointId))
    #if ($uix.id == $uixId)
      #set ($applicationIcon = $uix.parameters.icon)
    #end
  #end
  #if ("$!applicationIcon" == '')
    ## Fallback on the entry icon.
    #set ($templateProviderReference = $services.model.createDocumentReference(
      "$stringtool.removeEnd($classReference.name, 'Class')TemplateProvider",
      $classReference.parent
    ))
    #set ($entryIcon = $xwiki.getDocument($templateProviderReference).getValue('icon'))
    #if ("$!entryIcon" != '')
      #set ($applicationIcon = "icon:$entryIcon")
    #else
      #set ($applicationIcon = 'icon:application')
    #end
  #end
#end

#macro (displayIcon)
  #if ($services.uix)
    #getApplicationIcon($classReference)
    <dl>
      <dt>
        <label for="applicationIcon">
          $services.localization.render('platform.appwithinminutes.liveTableEditorIcon')
        </label>
        <span class="xHint">
          $services.localization.render('platform.appwithinminutes.liveTableEditorIconHintWithPicker',
            [$xwiki.getSkinFile('icons/silk/index_abc.png')])
        </span>
      </dt>
      <dd>
        <input id="applicationIcon" name="applicationIcon" type="text" size="10"
          value="$!escapetool.xml($applicationIcon)" />
      </dd>
    </dl>
  #end
#end

#macro (doEdit)
  {{html clean="false"}}
  #set ($liveTableObj = $doc.getObject('AppWithinMinutes.LiveTableClass', true))
  #set ($discard = $doc.use($liveTableObj))
  #set ($discard = $xwiki.ssx.use('AppWithinMinutes.LiveTableEditSheet'))
  #set ($discard = $xwiki.jsx.use('AppWithinMinutes.LiveTableEditSheet'))
  #if ("$!request.wizard" == 'true')
    #appWizardHeader('presentation')
  #end
  #displayHelpPanel()
  <div class="form-body">
    #displayFormFields()
    #displayIcon()
    #if ("$!request.wizard" == 'true')
      #appWizardFooter('presentation')
    #end
  </div>
  <div class="clearfloats"></div>
  {{/html}}

  {{iconPicker id="applicationIcon" prefix="icon:" /}}
#end

#macro (maybeGrantSpaceAdminRight $spaceRef)
  ## Grant space administration rights only if the space is new. Don't overwrite existing space preferences.
  #set ($spaceHomeRef = $services.model.resolveDocument('', 'default', $spaceRef))
  #set ($spacePrefsRef = $services.model.resolveDocument('WebPreferences', 'explicit', $spaceRef))
  ## Verify that the current user has script right on the current space home.
  #set ($hasScript = $services.security.authorization.hasAccess('script',  $xcontext.userReference, $spaceHomeRef))
  #if ($hasScript && !$xwiki.exists($spaceHomeRef) && !$xwiki.exists($spacePrefsRef))
    #set ($spacePrefsDoc = $xwiki.getDocument($spacePrefsRef))
    #set ($discard = $spacePrefsDoc.use($spacePrefsDoc.getObject('XWiki.XWikiGlobalRights', true)))
    #set ($discard = $spacePrefsDoc.set('allow', 1))
    #set ($discard = $spacePrefsDoc.set('levels', 'admin'))
    #set ($discard = $spacePrefsDoc.set('users', $services.model.serialize($xcontext.userReference, 'default')))
    #set ($discard = $spacePrefsDoc.setTitle('$services.localization.render(''admin.preferences.title'')'))
    #set ($discard = $spacePrefsDoc.setParent($services.model.serialize($spaceHomeRef, 'default')))
    #set ($discard = $spacePrefsDoc.setHidden(true))
    #set ($discard = $spacePrefsDoc.saveWithProgrammingRights($services.localization.render(
      'platform.appwithinminutes.grantSpaceAdminRightsSaveComment')))
  #end
#end

#macro (maybeGrantSpaceAdminRights)
  ## Application space
  #set ($appReference = $doc.documentReference.parent)
  #maybeGrantSpaceAdminRight($appReference)
  ## Code space (if it's not nested inside the application space)
  #set ($className = $request.get('AppWithinMinutes.LiveTableClass_0_class'))
  #set ($classReference = $services.model.resolveDocument($className))
  #if (!$classReference.hasParent($appReference))
    #maybeGrantSpaceAdminRight($classReference.parent)
  #end
#end

#macro (updateAndSaveLiveTable)
  #set ($discard = $doc.updateObjectFromRequest('AppWithinMinutes.LiveTableClass'))
  #set ($liveTableGeneratorDoc = $xwiki.getDocument('AppWithinMinutes.LiveTableGenerator'))

  ## Generate the LiveTable by displaying the LiveTableGenerator document in the context of the current document.
  #set ($displayParameters = $services.display.createDocumentDisplayerParameters())
  #set ($discard = $displayParameters.setExecutionContextIsolated(false))
  #set ($discard = $displayParameters.setContentTranslated(true))
  #set ($generatedLiveTableContent = $services.display.content($liveTableGeneratorDoc, {
    'outputSyntaxId': 'plain/1.0',
    'displayerParameters': $displayParameters
  }))

  ## Use the generated LiveTable content for the data home page.
  #set ($dataSpaceReference = $services.model.resolveSpace($doc.getValue('dataSpace')))
  #set ($dataSpaceHomeReference = $services.model.resolveDocument('', 'default', $dataSpaceReference))
  #if ($dataSpaceHomeReference.equals($doc.documentReference) || !$xwiki.exists($dataSpaceHomeReference))
    ## Either the application space and the data space are one and the same or this is a new application and we don't
    ## want to promote the data space anymore.
    #set ($dataHomePage = $doc)
  #else
    ## The application data is stored in a different space.
    #set ($dataHomePage = $xwiki.getDocument($dataSpaceHomeReference))
    #set ($discard = $dataHomePage.setHidden(true))
    #set ($escapedAppName = $doc.documentReference.parent.name.toLowerCase().replace("'", "''"))
    #set ($discard = $dataHomePage.setTitle("${escapetool.d}services.localization.render('${escapedAppName}.dataSpace.title')"))

    ## Update the home page content.
    #set ($homePageContent = '')
    #if ("$!generatedLiveTableContent" != '')
      ## Include the entries live table in the application home page.
      #set ($escapedReference = $services.model.serialize($dataSpaceHomeReference).replaceAll('([~"])', '~$1'))
      #set ($homePageContent = "{{include reference=""$escapedReference"" /}}")
    #end
    #set ($discard = $doc.setContent($homePageContent))
  #end
  #set ($discard = $dataHomePage.setContent($generatedLiveTableContent))
  ## We assume for now that the output produced by the live table generator uses the same syntax as the code of the live
  ## table generator. We have to set the syntax because the default wiki syntax (used when creating new wiki pages)
  ## could be different than the one used by the live table generator.
  #set ($discard = $dataHomePage.setSyntax($liveTableGeneratorDoc.syntax))

  #set ($minorEdit = "$!request.minorEdit" != '')
  #set ($comment = $request.comment)
  #if ("$!comment" == '')
    #set ($comment = $services.localization.render('platform.appwithinminutes.liveTableEditorSaveComment'))
  #end

  #if ($dataHomePage != $doc)
    ## Save the data home page.
    #set ($discard = $dataHomePage.save($comment, $minorEdit))
  #end

  ## Save the application home page.
  #set ($discard = $doc.save($comment, $minorEdit))
#end

#macro (updateAndSaveIcon)
  #set ($uix = $doc.getObject('XWiki.UIExtensionClass', true))
  #set ($discard = $uix.set('name', "platform.panels.${doc.space}Application"))
  #set ($discard = $uix.set('extensionPointId', 'org.xwiki.platform.panels.Applications'))
  #set ($uixParams = [
    "label=$doc.plainTitle",
    "target=$doc.fullName",
    "icon=$request.applicationIcon"
  ])
  #set ($discard = $uix.set('parameters', $stringtool.join($uixParams, $util.newline)))
  #set ($hasWikiAdminRights = $services.security.authorization.hasAccess('admin', $doc.documentReference.wikiReference))
  #set ($discard = $uix.set('scope', "#if ($hasWikiAdminRights)wiki#{else}user#end"))
  #set ($discard = $doc.save('Updated application icon', true))
#end

#macro (doSave)
  #maybeGrantSpaceAdminRights()
  #updateAndSaveLiveTable()
  #updateAndSaveIcon()
  #if ($action == 'save')
    #if ($errorMessage)
      {{error}}$services.rendering.escape($errorMessage, 'xwiki/2.1'){{/error}}
    #else
      ## Redirect to view mode.
      $response.sendRedirect($doc.getURL())
    #end
  #else
    #if ($errorMessage)
      $response.sendError(400, $errorMessage)
    #else
      $response.setStatus(204)
    #end
  #end
#end
{{/velocity}}

{{velocity}}
#if (!$services.security.authorization.hasAccess('script', $xcontext.userReference, $doc.documentReference))
  {{error}}{{translation key="platform.appwithinminutes.appHomePageNoScriptRight" /}}{{/error}}

#end
#if ("$!request.wizard" == 'true')
  {{include reference="AppWithinMinutes.WizardStep" /}}
#end
{{/velocity}}

{{velocity}}
## Determine the action button that triggered the request
#set ($action = $xcontext.action)
#foreach ($paramName in $request.getParameterMap().keySet())
  #if ($paramName.startsWith('xaction_'))
    #set ($action = $paramName.substring(8))
    #break
  #end
#end
#if ($action == 'edit')
  #doEdit()
#elseif ($action == 'save' || $action == 'saveandcontinue')
  #if ($services.csrf.isTokenValid($request.form_token))
    #doSave()
  #else
    $response.sendRedirect($services.csrf.getResubmissionURL())
  #end
#end
{{/velocity}}
