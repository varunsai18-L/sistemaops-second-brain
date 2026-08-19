---
id: xwiki-AppWithinMinutes.LiveTableViewSheet
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906745000
sync_date: 2026-08-19 20:23:04
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# LiveTable View Sheet

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906745000
- **Source:** [LiveTable View Sheet](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.LiveTableViewSheet)

---

{{template name="locationPicker_macros.vm" /}}

{{velocity output="false"}}
#macro (displayApp)
  #set ($discard = $xwiki.ssx.use('AppWithinMinutes.LiveTableViewSheet'))
  #set ($discard = $xwiki.jsx.use('AppWithinMinutes.LiveTableViewSheet', {'currentApp': $doc.getDocumentReference()}))
  #if (!$isReadOnly)
    #displayAppActions
  #end
  $doc.display('description')
  ## Display the live table only if it was generated.
  #if ($doc.content.length() > 0)
    = $services.localization.render('platform.appwithinminutes.appLiveTableHeading') =

    {{include reference="" author="target"/}}
  #end
#end

#macro (displayAppActions)
  ## Determine the user's rights
  #set ($className = $stringtool.removeEnd($classFullName, 'Class'))
  #set ($templateProviderReference = $services.model.resolveDocument("${className}TemplateProvider"))
  #set ($templateProvider = $xwiki.getDocument($templateProviderReference))
  #set ($creationRestrictions = $templateProvider.getValue('creationRestrictions'))
  #if ($creationRestrictions)
    #if ($creationRestrictions.size() > 0)
      #set ($dataSpaceRef = $services.model.resolveSpace($creationRestrictions.get(0)))
    #else
      ## There is no data space as the user can create application entries anywhere. Let's use the application space
      ## when the user clicks on the Add New Entry link from the home page.
      #set ($dataSpaceRef = $doc.documentReference.parent)
    #end
  #else
    ## The template provider is missing. Fall-back on the old 'dataSpace' property.
    #set ($dataSpaceRef = $services.model.resolveSpace($doc.getValue('dataSpace'), 'explicit',
      $doc.documentReference))
  #end
  #set ($hasCreateData = $services.security.authorization.hasAccess('edit', $dataSpaceRef))
  #set ($hasDeleteData = $services.security.authorization.hasAccess('admin', $dataSpaceRef))
  #set ($translationsRef = $services.model.resolveDocument("${className}Translations"))
  #set ($hasEditTranslations = $xwiki.isMultiLingual() && $xwiki.exists($translationsRef)
    && $services.security.authorization.hasAccess('edit', $translationsRef))
  #set ($classRef = $services.model.resolveDocument($classFullName))
  #set ($hasEditApplication = $services.security.authorization.hasAccess('edit', $classRef))
  #set ($hasDeleteApplication = $hasDeleteData
    && $services.security.authorization.hasAccess('admin', $doc.documentReference.parent)
    && $services.security.authorization.hasAccess('admin', $classRef.parent))
  ## Display the application actions based on the user's rights
  #if ($hasCreateData || $hasDeleteData || $hasEditApplication || $hasEditTranslations || $hasDeleteApplication)
    (% id="actionBox" class="floatinginfobox" %)
    (((
      = $services.localization.render('platform.appwithinminutes.appHomePageActionsHeading') =
      #if ($hasCreateData)
        * [[{{displayIcon name="add"/}} $services.localization.render('platform.appwithinminutes.appHomePageAddEntryHint')>>||anchor="AddNewEntry" class="action add"]]##
          #if ("$!templateProvider.getValue('terminal')" == '1')
            #set ($entryReference = $services.model.createDocumentReference('__entryName__', $dataSpaceRef))
          #else
            #set ($entryReference = $services.model.resolveDocument('', 'default',
              $services.model.createSpaceReference('__entryName__', $dataSpaceRef)))
          #end
          ## We need to set the title if we want to be able to sort or filter the doc.title live table column.
          #set ($params = {
            'form_token': $services.csrf.token,
            'template': "${className}Template",
            'title': '__entryName__',
            'parent': $services.model.serialize($doc.documentReference, 'local')
          })
          #if ($xwiki.getDocument($classRef).xWikiClass.properties.size() > 0)
            ## The entry has properties so go in edit mode to edit them.
            #set ($action = 'edit')
            #set ($params.editor = 'inline')
          #else
            ## There are no properties to edit so create the new entry and get back to the home page.
            #set ($action = 'save')
            #set ($discard = $params.putAll({
              'xredirect': $doc.getURL(),
              'form_token': $services.csrf.token
            }))
          #end
          {{html}}<input type="hidden" value="$xwiki.getURL($entryReference, $action, $escapetool.url($params))" />{{/html}}
      #end
      #if ($hasEditApplication)
        #set ($queryString = $escapetool.url({
          'appName': $doc.space,
          'resolve': true
        }))
        * [[{{displayIcon name="edit"/}} $services.localization.render('platform.appwithinminutes.appHomePageEditAppLabel')>>AppWithinMinutes.CreateApplication||queryString="$queryString" class="action edit"]]
      #end
      #if ($hasEditTranslations)
        * [[{{displayIcon name="translate"/}} $services.localization.render('platform.appwithinminutes.appHomePageTranslateAppLabel')>>path:${xwiki.getURL($translationsRef, 'edit', 'editor=wiki')}||class="action translate"]]
      #end
      #if ($hasDeleteData)
        #set ($deleteDataURL = $xwiki.getURL('AppWithinMinutes.DeleteApplication', 'view', $escapetool.url({
          'appName': $doc.space,
          'resolve': true,
          'scope': 'entries',
          'xredirect': $doc.getURL()
        })))
        * [[{{displayIcon name="cross"/}} $services.localization.render('platform.appwithinminutes.appHomePageDeleteEntriesLabel')>>path:${deleteDataURL}||class="action deleteData"]]
      #end
      #if ($hasDeleteApplication)
        #set ($deleteAppURL = $xwiki.getURL('AppWithinMinutes.DeleteApplication', 'view', $escapetool.url({
          'appName': $doc.space,
          'resolve': true,
          'xredirect': $doc.getURL()
        })))
        * [[{{displayIcon name="trash"/}} $services.localization.render('platform.appwithinminutes.appHomePageDeleteAppLabel')>>path:${deleteAppURL}||class="action delete"]]
      #end
    )))
  #end
#end

#macro (renameAppModal)
  <div class="modal" id="renameAppModal" tabindex="-1" role="dialog" aria-labelledby="renameAppModal-label"
      data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog" role="document">
      <form class="modal-content xform">
        ## The fieldset allows us to disable and enable the entire form quickly and easy.
        <fieldset>
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
                title="$escapetool.xml($services.localization.render('appWithinMinutes.renameApp.close'))"
                aria-label="$escapetool.xml($services.localization.render('appWithinMinutes.renameApp.close'))">
              <span aria-hidden="true">&times;</span>
            </button>
            <span class="modal-title" id="renameAppModal-label">
              $escapetool.xml($services.localization.render('appWithinMinutes.renameApp.label'))
            </span>
          </div>
          <div class="modal-body">
            #renameAppModalBody
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">
              $escapetool.xml($services.localization.render('cancel'))
            </button>
            <button type="submit" class="btn btn-primary" disabled="disabled">
              $escapetool.xml($services.localization.render('core.rename.submit'))
            </button>
          </div>
        </fieldset>
      </form>
    </div>
  </div>
#end

#macro (renameAppModalBody)
  #info($services.localization.render('appWithinMinutes.renameApp.changeAppTitleInfo'))
  #warning($services.localization.render('appWithinMinutes.renameApp.regenerateAppCodeWarning'))
  <div class="hidden">
    <input type="hidden" name="form_token" value="$!escapetool.xml($services.csrf.token)" />
    <input type="hidden" name="oldAppReference" value="$escapetool.xml(
      $services.model.serialize($doc.documentReference.parent, 'local'))"/>
    <span class="appNameEmptyError xErrorMsg">
      $services.localization.render("platform.appwithinminutes.appNameEmptyError")
    </span>
    <span class="pageExistsError xErrorMsg">
      $services.localization.render("appWithinMinutes.renameApp.pageExistsError")
    </span>
    <span class="locationForbiddenError xErrorMsg">
      $services.localization.render("appWithinMinutes.renameApp.locationForbiddenError")
    </span>
  </div>
  #set ($appName = $doc.pageReference.name)
  #set ($isNestedPage = $doc.documentReference.name == $services.model.getEntityReference('DOCUMENT', 'default').name)
  #set ($parentReference = $doc.documentReference.parent)
  #if ($isNestedPage)
    #set ($parentReference = $parentReference.parent)
  #end
  #locationPicker({
    'id': 'renameApp',
    'title': {
      'label': 'appWithinMinutes.renameApp.newName.label',
      'hint': 'platform.appwithinminutes.appNameHint',
      'name': 'newAppName',
      'value': $appName,
      'placeholder': 'appWithinMinutes.renameApp.newName.label'
    },
    'preview': {
      'label': 'appWithinMinutes.renameApp.location.label',
      'hint': 'appWithinMinutes.renameApp.location.hint'
    },
    'parent': {
      'label': 'appWithinMinutes.renameApp.parent.label',
      'hint': 'appWithinMinutes.renameApp.parent.hint',
      'name': 'newAppParentReference',
      'reference': $parentReference,
      'placeholder': 'appWithinMinutes.createApp.parent.placeholder'
    }
  })
#end
{{/velocity}}

{{velocity}}
#set ($liveTableObj = $doc.getObject('AppWithinMinutes.LiveTableClass'))
#if ($liveTableObj)
  #set ($discard = $doc.use($liveTableObj))
  #set ($classFullName = $doc.getValue('class'))
  #if ("$!classFullName" == '' || !$xwiki.exists($classFullName))
    {{warning}}
      {{translation key="platform.appwithinminutes.appHomePageMovedWarning"/}}
    {{/warning}}

  #end
  #displayApp()

  {{html clean="false"}}
  #renameAppModal()
  {{/html}}
#end
{{/velocity}}
