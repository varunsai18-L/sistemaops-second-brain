---
id: xwiki-xwiki:AppWithinMinutes.RenameApplication
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906704000
sync_date: 2026-07-21 11:00:54
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# RenameApplication

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906704000
- **Source:** [RenameApplication](https://wiki.systemaops.in/bin/view/AppWithinMinutes/xwiki:AppWithinMinutes.RenameApplication)

---

{{velocity output="false"}}
#macro (renameApp $oldAppReference $newAppReference)
  #set ($oldApp = {
    'name': $oldAppReference.name,
    'reference': $oldAppReference
  })
  #set ($newApp = {
    'name': $newAppReference.name,
    'reference': $newAppReference
  })
  #getAppCodeReference($oldApp $newApp)
  #if (!$newApp.codeReference.equals($oldApp.codeReference))
    ## Some application code pages have to be renamed separately because they have the application name in their name.
    #renameAppCodePages($oldApp $newApp)
    #if (!$oldApp.codeReference.equals($oldApp.reference) && !$oldApp.codeReference.hasParent($oldApp.reference))
      ## The application code pages are not children of the application page. Rename the remaining code pages.
      #renameAppPage($oldApp.codeReference $newApp.codeReference true)
      #maybeFixAppPreferences($oldApp.codePreferencesReference $newApp.codePreferencesReference)
    #end
  #end
  #renameAppPage($oldAppReference $newAppReference true)
  #maybeFixAppPreferences($oldApp.preferencesReference $newApp.preferencesReference)
#end

#macro (getAppCodeReference $oldApp $newApp)
  #set ($oldApp.codeReference = $services.model.createSpaceReference('Code', $oldApp.reference))
  #set ($oldClassReference = $xwiki.getDocument($oldApp.reference).getValue('class'))
  #if ($oldClassReference)
    #set ($oldClassReference = $services.model.resolveDocument($oldClassReference, $oldApp.reference))
    #set ($oldApp.codeReference = $oldClassReference.parent)
  #end
  #if ($oldApp.codeReference.hasParent($oldApp.reference))
    ## The code space is nested inside the application space.
    #set ($newApp.codeReference = $oldApp.codeReference.replaceParent($oldApp.reference, $newApp.reference))
  #elseif ($oldApp.codeReference.equals($oldApp.reference))
    ## The code space is the same as the application space.
    #set ($newApp.codeReference = $newApp.reference)
  #elseif ($oldApp.codeReference.parent.equals($oldApp.reference.parent)
      && $oldApp.codeReference.name == "${oldApp.name}Code")
    ## The code space is a sibling of the application space.
    #set ($newApp.codeReference = $services.model.createSpaceReference("${newApp.name}Code",
      $newApp.reference.parent))
  #else
    #set ($newApp.codeReference = $oldApp.codeReference)
  #end
#end

#macro (getAppCodePages $app)
  #set ($app.homePageReference = $services.model.resolveDocument('', 'default', $app.reference))
  #set ($app.preferencesReference = $services.model.createDocumentReference('WebPreferences', $app.reference))
  #set ($app.codePreferencesReference = $services.model.createDocumentReference('WebPreferences', $app.codeReference))
  #set ($app.codePages = {})
  #foreach ($codePage in ['class', 'sheet', 'template', 'templateProvider', 'translations'])
    #set ($discard = $app.codePages.put("${codePage}Reference", $services.model.createDocumentReference(
      "${app.name}$stringtool.capitalize($codePage)", $app.codeReference)))
  #end
#end

#macro (renameAppCodePages $oldApp $newApp)
  #getAppCodePages($oldApp)
  #getAppCodePages($newApp)
  #foreach ($entry in $oldApp.codePages.entrySet())
    #renameAppPage($entry.value $newApp.codePages.get($entry.key) true)
  #end
  #updateAppClass($oldApp $newApp)
  #updateAppSheet($oldApp $newApp)
  #updateAppTemplateProvider($oldApp $newApp)
  #updateAppTranslations($oldApp $newApp)
#end

#macro (renameAppPage $oldReference $newReference $checkRights)
  #set ($renameRequest = $services.refactoring.requestFactory.createRenameRequest($oldReference, $newReference))
  #set ($discard = $renameRequest.setInteractive(false))
  #set ($discard = $renameRequest.setAutoRedirect(false))
  #set ($discard = $renameRequest.setCheckRights($checkRights))
  #set ($renameJob = $services.refactoring.rename($renameRequest))
  #set ($discard = $renameJob.join())
#end

#macro (updateAppClass $oldApp $newApp)
  #if ($xwiki.exists($newApp.codePages.classReference) &&
      $services.security.authorization.hasAccess('edit', $newApp.codePages.classReference))
    #set ($newClass = $xwiki.getDocument($newApp.codePages.classReference))
    ## Update the sheet.
    #set ($newSheet = $services.model.serialize($newApp.codePages.sheetReference, 'local'))
    #set ($discard = $newClass.getObject('XWiki.ClassSheetBinding').set('sheet', $newSheet))
    ## Update the data space used by old applications.
    #set ($metaData = $newClass.getObject('AppWithinMinutes.MetadataClass'))
    #if ($metaData.getValue('dataSpaceName') == $services.model.serialize($oldApp.reference, 'local'))
      ## Between 6.3M2 (XWIKI-11249) and 7.3RC1 (XWIKI-12741)
      #set ($discard = $metaData.set('dataSpaceName', $services.model.serialize($newApp.reference, 'local')))
    #end
    #set ($discard = $newClass.save('Update class after renaming app'))
  #end
#end

#macro (updateAppSheet $oldApp $newApp)
  #if ($xwiki.exists($newApp.codePages.sheetReference) &&
      $services.security.authorization.hasAccess('edit', $newApp.codePages.sheetReference))
    #set ($newSheet = $xwiki.getDocument($newApp.codePages.sheetReference))
    ## Update the class reference used within the sheet content.
    #set ($oldClassReference = $services.model.serialize($oldApp.codePages.classReference, 'local'))
    #set ($newClassReference = $services.model.serialize($newApp.codePages.classReference, 'local'))
    #set ($discard = $newSheet.setContent($newSheet.content.replace($oldClassReference, $newClassReference)))
    #set ($discard = $newSheet.save('Update sheet after renaming app'))
  #end
#end

#macro (updateAppTemplateProvider $oldApp $newApp)
  #if ($xwiki.exists($newApp.codePages.templateProviderReference) &&
      $services.security.authorization.hasAccess('edit', $newApp.codePages.templateProviderReference))
    #set ($newTemplateProvider = $xwiki.getDocument($newApp.codePages.templateProviderReference))
    #set ($newTemplateProviderObj = $newTemplateProvider.getObject('XWiki.TemplateProviderClass'))
    ## Update the name.
    #set ($name = $newTemplateProviderObj.getValue('name'))
    #if ($name.startsWith($oldApp.name.toLowerCase()))
      #set ($discard = $newTemplateProviderObj.set('name',
        "$newApp.name.toLowerCase()$name.substring($oldApp.name.length())"))
    #end
    ## Update the template.
    #set ($discard = $newTemplateProviderObj.set('template',
      $services.model.serialize($newApp.codePages.templateReference, 'local')))
    ## Update creation restrictions.
    #set ($creationRestrictions = [])
    #foreach ($creationRestriction in $newTemplateProviderObj.getValue('creationRestrictions'))
      #set ($creationRestrictionReference = $services.model.resolveSpace($creationRestriction, $oldApp.reference))
      #if ($creationRestrictionReference.equals($oldApp.reference))
        #set ($creationRestrictionReference = $newApp.reference)
      #else
        #set ($creationRestrictionReference = $creationRestrictionReference.replaceParent(
          $oldApp.reference, $newApp.reference))
      #end
      #set ($discard = $creationRestrictions.add($services.model.serialize($creationRestrictionReference, 'local')))
    #end
    #set ($discard = $newTemplateProviderObj.set('creationRestrictions', $creationRestrictions))
    #set ($discard = $newTemplateProvider.save('Update template provider after renaming app'))
  #end
#end

#macro (updateAppTranslations $oldApp $newApp)
  #if ($xwiki.exists($newApp.codePages.translationsReference) &&
      $services.security.authorization.hasAccess('edit', $newApp.codePages.translationsReference))
    #set ($newTranslations = $xwiki.getDocument($newApp.codePages.translationsReference))
    ## Update the default translation.
    #updateAppTranslation($newTranslations $oldApp $newApp)
    ## Update all the available translations.
    #foreach ($locale in $newTranslations.translationLocales)
      #set ($newTranslationsForLocale = $newTranslations.getTranslatedDocument($locale))
      #updateAppTranslation($newTranslationsForLocale $oldApp $newApp)
    #end
  #end
#end

## Special characters that need to be escaped in a translation key.
#set ($translationKeySpecialCharsPattern = $regextool.compile('([=: \\])'))

#macro (updateAppTranslation $translation $oldApp $newApp)
  ## Update the translation keys that are prefixed with the application name.
  #set ($oldAppKeyPrefix = $translationKeySpecialCharsPattern.matcher($oldApp.name.toLowerCase()).replaceAll('\\$1'))
  #set ($newAppKeyPrefix = $translationKeySpecialCharsPattern.matcher($newApp.name.toLowerCase()).replaceAll('\\$1'))
  #set ($content = $translation.content.replaceAll("(?m)(^$regextool.quote($oldAppKeyPrefix))",
    $regextool.quoteReplacement($newAppKeyPrefix)))
  ## Update the translation keys that are prefixed with the class reference.
  #set ($oldClassKeyPrefix = $services.model.serialize($oldApp.codePages.classReference, 'local'))
  #set ($oldClassKeyPrefix = $translationKeySpecialCharsPattern.matcher($oldClassKeyPrefix).replaceAll('\\$1'))
  #set ($newClassKeyPrefix = $services.model.serialize($newApp.codePages.classReference, 'local'))
  #set ($newClassKeyPrefix = $translationKeySpecialCharsPattern.matcher($newClassKeyPrefix).replaceAll('\\$1'))
  #set ($content = $content.replaceAll("(?m)(^$regextool.quote($oldClassKeyPrefix))",
    $regextool.quoteReplacement($newClassKeyPrefix)))
  #set ($discard = $translation.setContent($content))
  #set ($discard = $translation.save('Update translations after renaming app'))
#end

#**
 * Simple users don't have the right to administer the pages they create so the application wizard creates the
 * WebPreferences page for them (using programming rights). When renaming the applications they have created, simple
 * users don't have the right to move the WebPreferences page to the new location so we need to do this for them (again,
 * relying on programming rights).
 *#
#macro (maybeFixAppPreferences $oldPrefsReference $newPrefsReference)
  ## Fix the preferences page if:
  ## * the old preferences page exists (wasn't moved / renamed)
  ## * and the current user has administration right on it
  ## * the new preferences page doesn't exist
  ## * and the current user has the right to delete its home page.
  #set ($newPrefsHomeReference = $services.model.resolveDocument('', 'default', $newPrefsReference.parent))
  #if ($xwiki.exists($oldPrefsReference) && $services.security.authorization.hasAccess('admin', $oldPrefsReference)
      && !$xwiki.exists($newPrefsReference)
      && $services.security.authorization.hasAccess('delete', $newPrefsHomeReference))
    ## This requires programming rights!
    #renameAppPage($oldPrefsReference $newPrefsReference false)
  #end
#end
{{/velocity}}

{{velocity wiki="false"}}
#if ($request.oldAppReference && $request.newAppReference)
  #if ($services.csrf.isTokenValid($request.form_token))
    #set ($oldAppReference = $services.model.resolveSpace($request.oldAppReference))
    #set ($newAppReference = $services.model.resolveSpace($request.newAppReference))
    #if (!$services.security.authorization.hasAccess('delete', $oldAppReference)
        || !$services.security.authorization.hasAccess('edit', $newAppReference))
      #set ($discard = $response.sendError(403))
    #elseif (!$newAppReference.equals($oldAppReference))
      #renameApp($oldAppReference $newAppReference)
    #end
  #else
    #set ($discard = $response.sendError(401, 'Bad CSRF Token'))
  #end
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
