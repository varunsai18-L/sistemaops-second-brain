---
id: xwiki-AppWithinMinutes.ClassTranslationsGenerator
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906768000
sync_date: 2026-08-19 20:23:03
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# ClassTranslationsGenerator

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906768000
- **Source:** [ClassTranslationsGenerator](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.ClassTranslationsGenerator)

---

{{include reference="AppWithinMinutes.VelocityMacros" /}}

{{velocity output="false"}}
## Special characters that need to be escaped in the key.
#set ($keySpecialCharsPattern = $regextool.compile('([=: \\])'))

#macro (map $key $value)
$keySpecialCharsPattern.matcher($key).replaceAll('\\$1')=$value
#end

#getAppTitle
{{/velocity}}

{{velocity wiki="false"}}
$escapetool.h Class fields
#set ($prefix = "${doc.fullName}_")
#foreach ($property in $doc.getxWikiClass().properties)
#map("$prefix$property.name" $property.prettyName)
#if ($property.type == 'StaticListClass')
## Generate translations for the list values.
#foreach ($entry in $property.mapValues.entrySet())
#map("$prefix${property.name}_$entry.key" $entry.value.value)
#end
#end
#end

$escapetool.h Sheet keys
#set ($appName = $doc.documentReference.name.replaceAll('Class', '').toLowerCase())
#map("${appName}.sheet.description" "This page controls how $appTitle pages are displayed in both view and edit modes.")
#map("${appName}.sheet.noObject" "The current page doesn't have the expected $appTitle object.")
#map("${appName}.sheet.noFields" "The $appTitle application doesn't have any fields to display.")

$escapetool.h Live table generic keys
#set ($prefix = "${appName}.livetable.")
#set ($liveTableGenericKeys = {
  'doc.title': 'liveTableEditorDocTitleColumnName',
  'doc.name': 'liveTableEditorDocNameColumnName',
  'doc.space': 'liveTableEditorDocSpaceColumnName',
  'doc.fullname': 'liveTableEditorDocFullNameColumnName',
  'doc.location': 'liveTableEditorDocLocationColumnName',
  'doc.author': 'liveTableEditorDocAuthorColumnName',
  'doc.creator': 'liveTableEditorDocCreatorColumnName',
  'doc.date': 'liveTableEditorDocDateColumnName',
  'doc.creationDate': 'liveTableEditorDocCreationDateColumnName',
  '_avatar': 'liveTableEditorAvatarColumnName',
  '_images': 'liveTableEditorImagesColumnName',
  '_attachments': 'liveTableEditorAttachmentsColumnName',
  '_actions': 'liveTableEditorActionsColumnName',
  '_actions.edit': 'appLiveTableEditEntryActionName',
  '_actions.delete': 'appLiveTableDeleteEntryActionName'
})
#foreach ($entry in $liveTableGenericKeys.entrySet())
#map("$prefix$entry.key" $services.localization.render("platform.appwithinminutes.$entry.value"))
#end
#map("${prefix}emptyvalue" '-')

$escapetool.h Live table specific keys
#foreach ($property in $doc.getxWikiClass().properties)
#map("$prefix$property.name" $property.prettyName)
#end

$escapetool.h Other keys
#map("${appName}.entry.name" $appTitle)

$escapetool.h Deprecated keys
#map("${appName}.dataSpace.title" 'Data')
{{/velocity}}
