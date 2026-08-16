---
id: xwiki-AppWithinMinutes.ClassSheetGenerator
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906794000
sync_date: 2026-08-16 20:01:57
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# ClassSheetGenerator

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906794000
- **Source:** [ClassSheetGenerator](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.ClassSheetGenerator)

---

{{velocity output="false"}}
#macro(escapeSingleQuotes $string)
$string.replace("'", "''")##
#end

#**
 * Generic property display.
 *#
#macro(displayProperty $property $indentation)
${indentation}<dt ${escapetool.h}if (!${escapetool.d}editing && ${escapetool.d}hasEdit)
${indentation}    class="editableProperty"
${indentation}    data-property="${escapetool.d}escapetool.xml(${escapetool.d}services.model.serialize(${escapetool.d}object.getPropertyReference('#escapeSingleQuotes($property.name)')))"
${indentation}    data-property-type="object"${escapetool.h}end>
${indentation}  <label${escapetool.h}if (${escapetool.d}editing) for="$escapetool.xml("${doc.fullName}_0_$property.name")"${escapetool.h}end>
${indentation}    ${escapetool.d}escapetool.xml(${escapetool.d}doc.displayPrettyName('#escapeSingleQuotes($property.name)', false, false))
${indentation}  </label>
#if ("$!property.hint" != '')
${indentation}  <span class="xHint">
${indentation}    ${escapetool.d}escapetool.xml(${escapetool.d}services.localization.render('#escapeSingleQuotes($property.hint)'))
${indentation}  </span>
#end
${indentation}</dt>
${indentation}<dd>${escapetool.d}doc.display('#escapeSingleQuotes($property.name)')</dd>
#end

#**
 * Unfortunately the custom display mechanism for properties doesn't offer a clean way to overwrite the display only when
 * some conditions are met (e.g. a specific action) so we're putting the custom display code in the sheet.
 *#
#macro(displayBooleanProperty $property $indentation)
${indentation}${escapetool.h}if (${escapetool.d}editing)
${indentation}  <dt>
${indentation}    <label for="$escapetool.xml("${doc.fullName}_0_$property.name")">
${indentation}      ${escapetool.d}doc.display('#escapeSingleQuotes($property.name)')
${indentation}      ${escapetool.d}escapetool.xml(${escapetool.d}doc.displayPrettyName('#escapeSingleQuotes($property.name)', false, false))
${indentation}    </label>
${indentation}  </dt>
#if ("$!property.hint" != '')
${indentation}  <dd>
${indentation}    <span class="xHint">
${indentation}      ${escapetool.d}escapetool.xml(${escapetool.d}services.localization.render('#escapeSingleQuotes($property.hint)'))
${indentation}    </span>
${indentation}  </dd>
#end
${indentation}${escapetool.h}else
#displayProperty($property "$indentation  ")
${indentation}${escapetool.h}end
#end
{{/velocity}}

{{velocity filter="none"}}
{{{##
{{velocity}}
${escapetool.h}set (${escapetool.d}object = ${escapetool.d}doc.getObject('#escapeSingleQuotes($doc.fullName)'))
#set ($appName = $stringtool.removeEnd($doc.documentReference.name, 'Class'))
#set ($translationKeyPrefix = "#escapeSingleQuotes($appName.toLowerCase()).sheet.")
${escapetool.h}if (!${escapetool.d}object)
  ${escapetool.h}set (${escapetool.d}messageKey = '${translationKeyPrefix}description')
  ${escapetool.h}set (${escapetool.d}messageType = 'info')
  ${escapetool.h}if (${escapetool.d}doc.documentReference.name != '#escapeSingleQuotes("${appName}Sheet")')
    ${escapetool.h}set (${escapetool.d}messageKey = '${translationKeyPrefix}noObject')
    ${escapetool.h}set (${escapetool.d}messageType = 'warning')
  ${escapetool.h}end
  {{${escapetool.d}messageType}}
  ${escapetool.d}services.localization.render(${escapetool.d}messageKey)
  {{/${escapetool.d}messageType}}
  ${escapetool.h}stop
${escapetool.h}end
#set ($properties = $doc.getxWikiClass().properties)
#if ($properties && $properties.size() > 0)
## This is needed for in-place editing.
${escapetool.h}set (${escapetool.d}discard = ${escapetool.d}xwiki.jsfx.use('uicomponents/edit/editableProperty.js', {
  'forceSkinAction': true,
  'language': ${escapetool.d}xcontext.locale
}))
${escapetool.h}set (${escapetool.d}discard = ${escapetool.d}doc.use(${escapetool.d}object))
${escapetool.h}set (${escapetool.d}editing = ${escapetool.d}xcontext.action == 'edit')
{{html wiki="true" clean="false"}}
## We don't have access to the form element to set the CSS class for the vertical form layout standard.
<div class="xform">
  <dl>
#foreach ($property in $properties)
#set ($displayFormType = $property.getProperty('displayFormType'))
#if ($property.type.indexOf('Boolean') != -1 && "$!displayFormType.value" == 'checkbox')
#displayBooleanProperty($property '    ')
#else
#displayProperty($property '    ')
#end
#end
  </dl>
</div>
{{/html}}
#else## No properties to display.
{{info}}
${escapetool.d}services.localization.render('${translationKeyPrefix}noFields')
{{/info}}
#end
{{/velocity}}##
}}}
{{/velocity}}
