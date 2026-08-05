---
id: xwiki-xwiki:AppWithinMinutes.ClassEditSheet
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906807000
sync_date: 2026-07-21 11:02:36
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# ClassEditSheet

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906807000
- **Source:** [ClassEditSheet](https://wiki.systemaops.in/bin/view/AppWithinMinutes/xwiki:AppWithinMinutes.ClassEditSheet)

---

{{include reference="AppWithinMinutes.VelocityMacros" /}}

{{groovy}}
import com.xpn.xwiki.XWikiContext;
import com.xpn.xwiki.api.Context;
import com.xpn.xwiki.api.Object;
import com.xpn.xwiki.api.PropertyClass;
import com.xpn.xwiki.doc.XWikiDocument;
import com.xpn.xwiki.objects.BaseObject;

/**
 * Used to preview class fields that have a custom display associated, before they are actually added/saved to the
 * class. For instance, when the user drags a Date field from the palette to the field canvas the class editor needs to
 * display that Date field as if the user would be editing an object with this Date field in "Inline form" edit mode.
 * This means that if the Date field has a custom display, the custom display should be used (e.g. using a Date picker).
 */
class PropertyCustomDisplayer
{
    private XWikiContext context;

    public PropertyCustomDisplayer(Context context)
    {
        this.context = context.getContext();
    }

    public String display(PropertyClass property, String prefix, com.xpn.xwiki.api.Object object)
    {
        HashMap<String, Object> backup = new HashMap<String, Object>();
        try {
            XWikiDocument.backupContext(backup, this.context);
            return this.displayInternal(property.getPropertyClass(), prefix, object.getXWikiObject());
        } finally {
            XWikiDocument.restoreContext(backup, this.context);
        }
    }

    private String displayInternal(com.xpn.xwiki.objects.classes.PropertyClass property, String prefix, BaseObject object)
    {
        StringBuffer result = new StringBuffer();
        property.displayCustom(result, property.getName(), prefix, "edit", object, this.context);
        return result.toString();
    }
}
xcontext.put('propertyCustomDisplayer', new PropertyCustomDisplayer(xcontext))
{{/groovy}}

{{velocity output="false"}}
#**
 * Constants
 *#
## Magic date used to mark in AWM that the date field is not set for the current entry. See https://jira.xwiki.org/browse/XWIKI-10296
#set($MAGIC_DATE = $datetool.toDate('yyyy-MM-dd', '9999-12-31'))

#**
 * Displays the field palette.
 *#
#macro (displayFieldPalette)
  <div id="palette">
    <p><strong>$services.localization.render('platform.appwithinminutes.classEditorPaletteTitle')</strong></p>
    <p class="xHint">$services.localization.render('platform.appwithinminutes.classEditorPaletteHint')</p>
    ## List all form field types, grouped by category.
    #set ($formFieldDocs = [])
    #set ($formFieldClassName = 'AppWithinMinutes.FormFieldClass')
    #set ($categoryListStatement = 'from doc.object(AppWithinMinutes.FormFieldCategoryClass) as category order by category.priority')
    <ul>
    #foreach ($category in $services.query.xwql($categoryListStatement).execute())
      #set ($categoryDoc = $xwiki.getDocument($category))
      <li>
        <div class="category">$escapetool.xml($categoryDoc.plainTitle)</div>
        #set ($formFieldsForCategoryStatement = "from doc.object($formFieldClassName) as field where field.category = :category order by field.priority")
        #set ($formFieldsForCategoryQuery = $services.query.xwql($formFieldsForCategoryStatement).bindValue('category', $category))
        <ul>
        #foreach ($formField in $formFieldsForCategoryQuery.execute())
          #set ($formFieldDoc = $xwiki.getDocument($formField))
          #set ($discard = $formFieldDocs.add($formFieldDoc))
          #set ($formFieldIcon = $formFieldDoc.getObject($formFieldClassName).getProperty('icon').value)
          #set ($formFieldIconRendered = $services.icon.renderHTML($formFieldIcon))
          #if ("$!formFieldIconRendered" == "")
            #if ($formFieldIcon.contains('/'))
              #set ($formFieldIconURL = $xwiki.getSkinFile($formFieldIcon))
            #else
              #set ($formFieldIconURL = $formFieldDoc.getAttachmentURL($formFieldIcon))
            #end
            #set ($formFieldIconRendered = "<img src='$escapetool.xml($formFieldIconURL)' alt='$escapetool.xml($formFieldDoc.plainTitle)' class='icon' />")
          #end
          <li class="field">
            $formFieldIconRendered
            $escapetool.xml($formFieldDoc.plainTitle)
            ## FIXME: We should use the 'get' action instead to prevent the stats module from recording this AJAX request.
            ## The 'edit' action is a temporary solution until the sheet module is modified to allow a sheet to be enforced through
            ## the query string even if it doesn't match the action (e.g. the 'get' action).
            ## The sheet parameter is required when editing a new class because the request will be made to a document that doesn't exist.
            ## FIXME2: In the future don't force the text editor type and instead use the default editor. This means
            ## that if the WYSIWYG editor is used, we'll need to convert the HTML into the target syntax so that the
            ## Template in #updateAndSaveTemplate is saved with target syntax and not HTML.
            ## See https://jira.xwiki.org/browse/XWIKI-13789
            #set ($fieldURL = $doc.getURL('edit', $escapetool.url({
              'xpage': 'plain',
              'sheet': 'AppWithinMinutes.ClassEditSheet',
              'form_token': $services.csrf.getToken(),
              'template': 'AppWithinMinutes.ClassTemplate',
              'field': $formFieldDoc.fullName,
              'xeditmode': 'text'
            })))
            <input type="hidden" value="$escapetool.xml($fieldURL)" class="data"/>
          </li>
        #end
        </ul>
      </li>
    #end
    </ul>
  </div>
#end

#**
 * Displays the field canvas.
 *#
#macro (displayFieldCanvas)
  #set ($propertyType2FormField = {})
  #foreach ($formFieldDoc in $formFieldDocs)
    ## Use the type of the field template.
    #set ($type = $formFieldDoc.getxWikiClass().properties.get(0).classType)
    #set ($discard = $propertyType2FormField.put($type, $formFieldDoc))
  #end
  <div id="canvas">
    <p class="hint">
      $services.localization.render('platform.appwithinminutes.classEditorCanvasHint')
    </p>
    <ul>
      #set ($unknownFields = [])
      #foreach ($field in $doc.getxWikiClass().properties)
        #set ($formFieldDoc = $propertyType2FormField.get($field.classType))
        #if ($formFieldDoc)
          <li>#displayField($field $formFieldDoc)</li>
        #else
          #set($discard = $unknownFields.add($field))
        #end
      #end
    </ul>
    <div class="hidden">
      ## Output the field meta data even if the field is not supported to preserve it when the class is saved.
      #foreach ($field in $unknownFields)
        #displayFieldMetaData($field)
      #end
    </div>
  </div>
#end

#**
 * Display the options to create/update the class template, the class sheet and the class translation bundle.
 *#
#macro (displayClassOptions)
  #set ($className = $stringtool.removeEnd($doc.fullName, 'Class'))
  #set ($templateReference = $services.model.resolveDocument("${className}Template"))
  #set ($translationsReference = $services.model.resolveDocument("${className}Translations"))
  #set ($classSheets = $services.sheet.getClassSheets($doc))
  #set ($sheetReference = $null)
  #if ($classSheets.isEmpty())
    #set ($sheetReference = $services.model.resolveDocument("${className}Sheet"))
  #elseif ($classSheets.size() == 1)
    #set ($sheetReference = $classSheets.get(0))
  #end
  ## Hide the options if neither the sheet nor the template nor the translation bundle exists. They don't have to be
  ## updated, they have to be created.
  <dl id="options" #if (!$xwiki.exists($sheetReference) && !$xwiki.exists($templateReference)
      && !$xwiki.exists($translationsReference))class="hidden"#end>
    <dt>
      <label for="updateClassTemplate">
        <input type="checkbox" id="updateClassTemplate" name="updateClassTemplate" checked="checked" />
        $services.localization.render('platform.appwithinminutes.classEditorUpdateTemplateLabel')
      </label>
    </dt>
    <dd>
      <span class="xHint">
        $services.localization.render('platform.appwithinminutes.classEditorUpdateTemplateHint',
          ["#pageLink($templateReference)"])
      </span>
    </dd>
    <dt>
      <label for="updateClassSheet">
        <input type="checkbox" id="updateClassSheet" name="updateClassSheet"
          #if ($sheetReference)checked="checked" #{else}disabled="disabled" #end/>
        $services.localization.render('platform.appwithinminutes.classEditorUpdateSheetLabel')
      </label>
    </dt>
    <dd>
    #if ($sheetReference)
      <span class="xHint">
        $services.localization.render('platform.appwithinminutes.classEditorUpdateSheetHint',
          ["#pageLink($sheetReference)"])
      </span>
    #else
        #inlineWarning($services.localization.render('platform.appwithinminutes.classEditorMultipleSheetsWarning'))
    #end
    </dd>
    <dt>
      <label for="updateClassTranslations">
        <input type="checkbox" id="updateClassTranslations" name="updateClassTranslations" checked="checked" />
        $services.localization.render('platform.appwithinminutes.classEditorUpdateTranslationsLabel')
      </label>
    </dt>
    <dd>
      <span class="xHint">
        $services.localization.render('platform.appwithinminutes.classEditorUpdateTranslationsHint',
          ["#pageLink($translationsReference)"])
      </span>
    </dd>
  </dl>
#end

#macro (pageLink $reference)
  #set ($class = 'wikilink')
  #set ($action = 'view')
  #set ($params = {})
  #if (!$xwiki.exists($reference))
    #set ($class = 'wikicreatelink')
    #set ($action = 'create')
    #set ($discard = $params.put('parent', $doc.fullName))
  #end
  <span class="$class"><a href="$escapetool.xml($xwiki.getURL($reference, $action, $escapetool.url($params)))"
    >$escapetool.xml($reference.name)</a></span>##
#end

#**
 * Display a form field.
 *#
#macro (displayField $field $formFieldDoc)
  #if ($formFieldDoc.getObject('XWiki.StyleSheetExtension'))
    #set ($discard = $xwiki.ssx.use($formFieldDoc.fullName))
  #end
  #if ($formFieldDoc.getObject('XWiki.JavaScriptExtension'))
    #set ($discard = $xwiki.jsx.use($formFieldDoc.fullName))
  #end
  <div class="hidden">
    #displayFieldMetaData($field)
    ## We need this information to avoid querying and loading all FormField documents twice.
    ## NOTE: We use a different ID format to avoid collisions with the field meta properties.
    <input type="hidden" id="template-$field.name" name="template-$field.name"
      value="$escapetool.xml($formFieldDoc.fullName)"
      data-propertyName="$escapetool.xml($formFieldDoc.getxWikiClass().propertyNames[0])" />
  </div>
  #set ($className = $stringtool.removeEnd($doc.fullName, 'Class'))
  #set ($templateRef = $services.model.resolveDocument("${className}Template"))
  #set ($templateDoc = $xwiki.getDocument($templateRef))
  ## Simulate the editing of the class instance from the template document.
  ## Note that we can't simply call display on the template document because $field could be a new field that hasn't
  ## been added to the class yet (so the object from the template doesn't have this field yet).
  <dl class="field-viewer">
    #displayFieldProperty($field "${doc.fullName}_0_" $templateDoc.getObject($doc.fullName, true))
  </dl>
  #set ($propertyNames = ['name', 'prettyName', 'number', 'required', 'hint'])
  #set ($formFieldObj = $formFieldDoc.getObject('AppWithinMinutes.FormFieldClass'))
  #set ($customPropertyNames = $formFieldObj.getProperty('properties').value.split('\s+'))
  #set ($discard = $customPropertyNames.removeAll($propertyNames))
  #set ($discard = $propertyNames.addAll($customPropertyNames.subList(0, $customPropertyNames.size())))
  <dl class="field-config">
    #foreach ($propertyName in $propertyNames)
      #set ($propertyDefinition = $field.xWikiClass.get($propertyName))
      #if ($propertyDefinition)
        #displayFieldProperty($propertyDefinition "field-${field.name}_" $field)
      #end
    #end
  </dl>
#end

#**
 * Display the field meta data. This is needed to preserve the field when its type is not supported by the editor.
 *#
#macro (displayFieldMetaData $field)
  <input type="hidden" id="type-$field.name" name="type-$field.name" value="$field.classType" />
#end

#**
 * Displays a configuration property of a class field. This macro can also be used to display a property of an object.
 *#
#macro (displayFieldProperty $property $prefix $field)
  #set ($displayFormType = $property.getProperty('displayFormType'))
  #if ($property.classType == 'Boolean' && (!$displayFormType || $displayFormType.value == 'checkbox'))
    <dt>
      <label for="$!{prefix}$property.name">
        #displayPropertyEditInput($property, $prefix, $field)$escapetool.xml($property.prettyName)
      </label>
    </dt>
    <dd></dd>
  #else
    <dt><label for="${prefix}$property.name">$escapetool.xml($property.prettyName)</label></dt>
    <dd>#displayPropertyEditInput($property, $prefix, $field)</dd>
  #end
#end

#**
 * Displays the input used to edit the specified property of the given object. The given object can be either an
 * instance of an XWiki class or a class field. In the first case the property represents an object field and in the
 * second case the property represents a field meta property. We currently don't use custom display for metaproperty,
 * so in that case we fallback on displayEdit.
 *#
#macro (displayPropertyEditInput $property $prefix $object)
  #set ($wrappedProperty = $property.propertyClass)
  #if ($wrappedProperty.isCustomDisplayed($xcontext.context))
    #set ($customDisplayer = $!xcontext.get('propertyCustomDisplayer').display($property, $prefix, $object))
    #if ((! $customDisplayer) && ("$!customDisplayer" == ""))
      $doc.displayEdit($property, $prefix, $object)
    #else
      $customDisplayer
    #end
  #else
    $doc.displayEdit($property, $prefix, $object)
  #end
#end

#**
 * Called when a new form field is added via AJAX.
 *#
#macro (displayNewField)
  ## Output the SkinExtension hooks to allow field displayers to pull JavaScript/CSS resources.
  ## Output also the LinkExtension hook because $xwiki.linkx.use() is used to load CSS files from WebJars.
  ## The class editor moves this resource includes in the HTML page head.
  <!-- com.xpn.xwiki.plugin.skinx.LinkExtensionPlugin -->
  #skinExtensionHooks
  #set ($formFieldDoc = $xwiki.getDocument($request.field))
  #set ($formFieldDocClassFields = $formFieldDoc.getxWikiClass().getXWikiClass().properties)
  #if ($formFieldDocClassFields.size() > 0)
    ## Clone the field template.
    #set ($field = $formFieldDocClassFields.get(0).clone())
    #if ("$!field.prettyName" == '')
      #set ($discard = $field.setPrettyName($formFieldDoc.title))
    #end
    #set ($xclass = $doc.getxWikiClass().getXWikiClass())
    #set ($discard = $xclass.addField($field.name, $field))
    #set ($discard = $field.setObject($xclass))
    #displayField($doc.getxWikiClass().get($field.name) $formFieldDoc)
  #else
    Unsupported form field.
  #end
#end

#**
 * Preview a class field (requires Programming Right).
 *#
#macro (previewField)
  ## Find the request parameter that specifies the field template.
  #foreach ($paramName in $request.getParameterMap().keySet())
    #if ($paramName.startsWith('template-'))
      #set ($fieldName = $paramName.substring(9))
      #set ($fieldTemplateDoc = $xwiki.getDocument($request.getParameter($paramName)))
      #break
    #end
  #end
  ##
  ## Clone the field template.
  #set ($field = $fieldTemplateDoc.getxWikiClass().getXWikiClass().properties.get(0).clone())
  ##
  ## Update the field meta properties based on the submitted data.
  #set ($valuesFromRequest = $xcontext.context.getForm().getObject("field-$fieldName"))
  #set ($discard = $field.getxWikiClass().fromMap($valuesFromRequest, $field))
  ##
  ## Don't rename the field (ignore the submitted name).
  #set ($discard = $field.setName($fieldName))
  ##
  ## We have to add the field to the class before setting its value.
  ## (otherwise the field value from the request is ignored).
  #set ($xclass = $doc.getxWikiClass().getXWikiClass())
  #set ($discard = $xclass.addField($fieldName, $field))
  #set ($discard = $field.setObject($xclass))
  ##
  ## Create an object that has this field and set its value from request.
  #set ($object = $fieldTemplateDoc.getObject($doc.fullName, true))
  ##
  ## Filter empty values from the request, otherwise the update method could try to select an invalid value.
  #set ($values = [])
  #foreach ($value in $request.getParameterValues("${doc.fullName}_0_$fieldName"))
    #if ($value != '')
      #set ($discard = $values.add($value))
    #end
  #end
  #if ($values.size() > 0)
    #set ($stringArray = $request.getParameterValues("template-$fieldName"))
    #set ($discard = $xclass.fromMap({$fieldName: $values.toArray($stringArray)}, $object.getXWikiObject()))
  #end
  ##
  ## Display the field.
  #set ($field = $doc.getxWikiClass().get($fieldName))
  #displayPropertyEditInput($field, "${doc.fullName}_0_", $object)
#end

#**
 * Display the edit class form.
 *#
#macro (displayEditForm)
  #set ($discard = $xwiki.jsx.use('AppWithinMinutes.ClassEditSheet'))
  #set ($discard = $xwiki.ssx.use('AppWithinMinutes.ClassEditSheet'))
  #set ($discard = $xwiki.ssx.use('AppWithinMinutes.ClassSheetGenerator'))
  #if ("$!request.wizard" == 'true')
    #appWizardHeader('structure')
  #end
  #displayFieldPalette()
  #displayFieldCanvas()
  #displayClassOptions()
  #if("$!request.wizard" == 'true')
    #appWizardFooter('structure')
  #end
  <div class="clearfloats"></div>
#end

#**
 * Displays either the edit class form or a new form field. The later is used when adding a new form field via AJAX.
 *#
#macro (doEdit)
  #if ("$!request.field" != '')
    #displayNewField()
  #elseif ("$!request.preview" == 'true')
    #previewField()
  #else
    ## Make sure that only the sheet content is rendered when the class is saved using AJAX.
    <div class="hidden">
      <input type="hidden" name="xpage" value="plain" />
      #if ($request.wizard == 'true')
        ## Preserve the wizard mode.
        <input type="hidden" name="wizard" value="true" />
      #end
      ## Compute the application title to be used as the wizard step title.
      #getAppTitle
    </div>
    #displayEditForm()
  #end
#end

#**
 * Create the home page of the application code space, if it doesn't exist already.
 *#
#macro (maybeCreateCodeSpace)
  #set ($codeHomePageReference = $services.model.resolveDocument('', 'default', $doc.documentReference.parent))
  #if (!$xwiki.exists($codeHomePageReference))
    #set ($codeSpaceTemplate = $services.model.resolveDocument('AppWithinMinutes.CodeSpaceTemplate'))
    #set ($copyAsJob = $services.refactoring.copyAs($codeSpaceTemplate, $codeHomePageReference))
    #try()
      #set ($discard = $copyAsJob.join())
      #set ($copyAsJobStatus = $services.job.getJobStatus($copyAsJob.request.id))
      #set ($errorMessage = $copyAsJobStatus.logTail.getFirstLogEvent('ERROR').toString())
    #end
  #end
#end

#**
 * Updates and saves the class definition based on the submitted data.
 *#
#macro(updateAndSaveClass)
  #set($class = $doc.xWikiClass)
  #set($xclass = $class.getXWikiClass().clone())
  #set($xdoc = $doc.document)
  ##
  ## Handle new fields and field type changes.
  ##
  #set($fieldNames = [])
  #foreach($paramName in $request.getParameterMap().keySet())
    #if($paramName.startsWith('type-'))
      #set($fieldName = $paramName.substring(5))
      #set($fieldType = $request.getParameter($paramName))
      #set($field = $class.get($fieldName))
      #if(!$field || $field.classType != $fieldType)
        #if($field)
          ## The field type has changed. Remove the field and add a new one with the proper type.
          #set($discard = $xclass.removeField($fieldName))
        #end
        ## Add a new class field with the specified type.
        #set($fieldTemplateRef = $request.getParameter("template-$fieldName"))
        #if("$!fieldTemplateRef" != '')
          #set($fieldTemplateDoc = $xwiki.getDocument($fieldTemplateRef))
          #set($field = $fieldTemplateDoc.getxWikiClass().getXWikiClass().properties.get(0).clone())
          #set($discard = $field.setObject($xclass))
          #set($discard = $xclass.addField($fieldName, $field))
          #set($discard = $fieldNames.add($fieldName))
          #set($discard = $xdoc.setMetaDataDirty(true))
        #end
      #else
        #set($discard = $fieldNames.add($fieldName))
      #end
    #end
  #end
  ##
  ## Handle deleted fields.
  ##
  #foreach($field in $class.properties)
    #if(!$fieldNames.contains($field.name))
      #set($discard = $xclass.removeField($field.name))
    #end
  #end
  ##
  ## Handle field updates.
  ##
  #set($fieldsToRename = {})
  #foreach($fieldName in $xclass.propertyNames)
    #set($field = $xclass.get($fieldName))
    #set($valuesFromRequest = $xcontext.context.getForm().getObject("field-$fieldName"))
    #set($discard = $field.getxWikiClass().fromMap($valuesFromRequest, $field))
    #if($field.name.matches('^[a-zA-Z_][\w:\-\.]*$'))
      #if($fieldName != $field.name)
        ## The field name has changed.
        #if($xclass.get($field.name))
          ## There is already a field with the same name.
          #set($errorMessage = $services.localization.render('platform.appwithinminutes.classEditorDuplicateFieldNameError', [$field.name]))
          #break
        #else
          #set($discard = $xclass.removeField($fieldName))
          #set($discard = $xclass.addField($field.name, $field))
          #set($originalField = $class.get($fieldName))
          #if($originalField)
            ## This is not a new field.
            #set($discard = $fieldsToRename.put($fieldName, $field.name))
            #set($discard = $xclass.addPropertyForRemoval($originalField.propertyClass))
          #end
        #end
      #end
    #else
      #set($errorMessage = $services.localization.render('propertynamenotcorrect'))
      #break
    #end
  #end
  ##
  ## Save
  ##
  #if(!$errorMessage)
    #set($discard = $xdoc.setXClass($xclass))
    #set($discard = $xdoc.renameProperties($doc.documentReference, $fieldsToRename))
    #set($discard = $xdoc.setHidden(true))
    #set($discard = $xdoc.setMetaDataDirty(true))
    #set($discard = $doc.save($services.localization.render('core.comment.updateClassProperty'), $minorEdit))
  #end
  ##
  ## Handle field renames.
  ##
  #if(!$errorMessage && !$fieldsToRename.isEmpty())
    ## We need to load all documents (except the class and template, which we handle below) that have objects of this class and rename their properties.
    ## If we don`t skip the template, we can not control the behaviour of emptyIsToday for date fields, which we want to handle in #updateAndSaveTemplate only once.
    ##
    ## FIXME: even if it is not a good practice to have an object in the class document, it is still possible. We should handle field renames for the class document
    ## as well. Note that there is a possibility that objects in the class' document are automatically updated. Needs checking.
    ##
    ## We use HQL because XWQL doesn't allow us to escape the special characters from the class name.
    #set($instancesStatement = ', BaseObject as obj where doc.fullName = obj.name and obj.className = :className'
      + ' and doc.fullName not in (:className, :templateName)')
    #set($className = $stringtool.removeEnd($doc.fullName, 'Class'))
    #set($instancesQuery = $services.query.hql($instancesStatement).bindValue('className', $doc.fullName).bindValue(
      'templateName', "${className}Template"))
    #foreach($instanceDocName in $instancesQuery.execute())
      #set($instanceDoc = $xwiki.getDocument($instanceDocName))
      #set($discard = $instanceDoc.document.renameProperties($doc.documentReference, $fieldsToRename))
      #set($discard = $instanceDoc.save($services.localization.render('core.comment.updateClassPropertyName'), true))
    #end
  #end
#end

#**
 * Handle Date fields that have the "Empty is today" option checked in the class edit form.
 * See https://jira.xwiki.org/browse/XWIKI-10296
 **#
#macro(handleEmptyIsTodayDateFields $templateDoc)
  #foreach($property in $doc.xWikiClass.properties)
    ## We check directly on the request if the user provided an empty date. We can not check from the template
    ## document's object that we've just parsed from the request using the updateObjectFromRequest method because it
    ## already applies the emtpyIsToday mechanism and that would not be good for us.
    #set($newValueRequestParameterName = "${doc.fullName}_0_${property.name}")
    #set($newDateStringValue = "$!{request.getParameter($newValueRequestParameterName)}")
    #if($property.classType == 'Date' && $property.getValue('emptyIsToday') == 1 && $newDateStringValue == '')
      #set($discard = $templateDoc.set($property.name, $MAGIC_DATE))
    #end
  #end
#end

#**
 * Updates and saves the class template based on the submitted data.
 *#
#macro(updateAndSaveTemplate)
  #if(!$errorMessage && $request.updateClassTemplate)
    #set($className = $stringtool.removeEnd($doc.fullName, 'Class'))
    #set($templateRef = $services.model.resolveDocument("${className}Template"))
    #set($templateDoc = $xwiki.getDocument($templateRef))
    #set($discard = $templateDoc.setParent($doc.documentReference.name))
    #if ($request.templateTitle)
      #set($discard = $templateDoc.setTitle($request.templateTitle))
    #end
    #if ($request.templateContent)
      #set($discard = $templateDoc.setContent($request.templateContent))
    #end
    ## Rename the properties of the template's object, if applicable.
    #set($discard = $templateDoc.document.renameProperties($doc.documentReference, $fieldsToRename))
    ## Fill the template's object with the default values from the class editor's form.
    #set($discard = $templateDoc.updateObjectFromRequest($doc.fullName))
    ## 
    #handleEmptyIsTodayDateFields($templateDoc)
    #set($discard = $templateDoc.setHidden(true))
    #set($discard = $templateDoc.save(
      $services.localization.render('platform.appwithinminutes.classEditorTemplateSaveComment'),
      $minorEdit))
  #end
#end

#**
 * Updates and saves the class sheet based on the submitted data.
 *#
#macro(updateAndSaveSheet)
  #if(!$errorMessage && $request.updateClassSheet)
    #set($classSheets = $services.sheet.getClassSheets($doc))
    #if($classSheets.isEmpty())
      #set($className = $stringtool.removeEnd($doc.fullName, 'Class'))
      #set($sheetReference = $services.model.resolveDocument("${className}Sheet"))
      #set($discard = $services.sheet.bindClassSheet($doc, $sheetReference))
      #set($discard = $doc.save($services.localization.render('platform.appwithinminutes.classEditorBindSheetSaveComment'),
        $minorEdit))
    #elseif($classSheets.size() == 1)
      #set($sheetReference = $classSheets.get(0))
    #end
    #if($sheetReference)
      #set($sheetDoc = $xwiki.getDocument($sheetReference))
      #set($sheetGeneratorDoc = $xwiki.getDocument('AppWithinMinutes.ClassSheetGenerator'))
      #set($discard = $sheetDoc.setParent($doc.documentReference.name))
      #set($discard = $sheetDoc.setContent($doc.getRenderedContent($sheetGeneratorDoc.content,
        $sheetGeneratorDoc.syntax.toIdString(), 'plain/1.0')))
      ## We assume for now that the output produced by the sheet generator uses the same syntax as the code of the sheet
      ## generator. We have to set the syntax because the default wiki syntax (used when creating new wiki pages) could
      ## be different than the one used by the sheet generator.
      #set($discard = $sheetDoc.setSyntax($sheetGeneratorDoc.syntax))
      #set($discard = $sheetDoc.setHidden(true))
      #set($discard = $sheetDoc.save($services.localization.render('platform.appwithinminutes.classEditorSheetSaveComment'),
        $minorEdit))
    #end
  #end
#end

#**
 * Updates and saves the class translation bundle based on the submitted data.
 *#
#macro(updateAndSaveTranslations)
  #if(!$errorMessage && $request.updateClassTranslations)
    #set($className = $stringtool.removeEnd($doc.fullName, 'Class'))
    #set($translationsRef = $services.model.resolveDocument("${className}Translations"))
    #set($translationsDoc = $xwiki.getDocument($translationsRef))
    #set($translationsObj = $translationsDoc.getObject('XWiki.TranslationDocumentClass', true))
    #set ($scope = 'USER')
    #if ($services.security.authorization.hasAccess('admin', $doc.documentReference.wikiReference))
      #set ($scope = 'WIKI')
    #end
    #set($discard = $translationsObj.set('scope', $scope))
    #set($discard = $translationsDoc.setParent($doc.documentReference.name))
    #set($translationsGeneratorDoc = $xwiki.getDocument('AppWithinMinutes.ClassTranslationsGenerator'))
    #set($discard = $translationsDoc.setContent($doc.getRenderedContent($translationsGeneratorDoc.content,
      $translationsGeneratorDoc.syntax.toIdString(), 'plain/1.0')))
    #set($discard = $translationsDoc.setSyntaxId('plain/1.0'))
    #set($discard = $translationsDoc.setHidden(true))
    #set($discard = $translationsDoc.save(
      $services.localization.render('platform.appwithinminutes.classEditorTranslationsSaveComment'),
      $minorEdit))
  #end
#end

#**
 * Updates and saves the class definition, the class sheet and the class template.
 *#
#macro (doSave)
  #set ($minorEdit = "$!request.minorEdit" != '')
  #maybeCreateCodeSpace
  #updateAndSaveClass
  #updateAndSaveTemplate
  #updateAndSaveSheet
  #updateAndSaveTranslations
  #if ($action == 'save')
    #if ($errorMessage)
      #error($errorMessage)
    #elseif ("$!request.wizard" == 'true')
      ## Redirect to next wizard step.
      #set ($className = $stringtool.removeEnd($doc.fullName, 'Class'))
      #set ($templateProviderReference = $services.model.resolveDocument("${className}TemplateProvider"))
      #set ($queryString = {
        'wizard': true,
        'sheet': 'AppWithinMinutes.TemplateProviderEditSheet'
      })
      #if (!$xwiki.exists($templateProviderReference))
        #set ($discard = $queryString.putAll({
          'form_token': $services.csrf.getToken(),
          'template': 'XWiki.TemplateProviderTemplate',
          'parent': $doc.fullName
        }))
      #end
      $response.sendRedirect($xwiki.getURL($templateProviderReference, 'edit', $escapetool.url($queryString)))
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
#if("$!request.wizard" == 'true')
  {{include reference="AppWithinMinutes.WizardStep" /}}
#end
{{/velocity}}

{{velocity}}
{{html clean="false"}}
## Determine the action button that triggered the request
#set ($action = 'edit')
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
{{/html}}
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
