---
id: xwiki-xwiki:XWiki.ClassSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906690000
sync_date: 2026-07-21 11:02:11
tags:
  - xwiki/documentation
  - space/xwiki
---
# Default Class Sheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906690000
- **Source:** [Default Class Sheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.ClassSheet)

---

{{template name="locationPicker_macros.vm" /}}

{{velocity}}
## This document can be copied in order to be customized so we cannot rely on its name to determine if the currently
## displayed document is a class or the class sheet itself. We look for the sheet descriptor instead.
#set ($isSheet = $doc.getObject('XWiki.SheetDescriptorClass'))
#if ($isSheet)
  ## Viewing the sheet document itself.
  {{translation key="platform.xclass.defaultClassSheet.description"/}}
#elseif ("$!request.bindSheet" != '' && $hasEdit)
  #if ($services.csrf.isTokenValid($request.getParameter('form_token')))
    ## Bind the sheet to the class.
    #set ($classSheetReference = $services.model.resolveDocument($request.bindSheet))
    #if ($services.sheet.bindClassSheet($doc, $classSheetReference))
      $doc.save($services.localization.render('platform.xclass.defaultClassSheet.sheets.bind'))
    #end
    $response.sendRedirect($request.xredirect)
  #else
    $response.sendRedirect($services.csrf.getResubmissionURL())
  #end
  ## Stop processing, since we already sent a redirect.
  #stop
#elseif("$!request.docName" != '')
  ## Request for creating a new instance.
  ## We don't actually create a new instance here, we just redirect to the edit mode.
  #set ($targetSpaceRef = $services.model.resolveSpace($request.spaceName))
  #set ($targetDocRef = $services.model.createDocumentReference($request.docName, $targetSpaceRef))
  #if (!$xwiki.exists($targetDocRef) && $services.security.authorization.hasAccess('edit', $targetDocRef))
    ## Compute the default edit mode to ensure backward compatibility with documents that are still using the deprecated
    ## inline action.
    #set ($editAction = $xwiki.getDocument($request.template).getDefaultEditMode())
    $response.sendRedirect($xwiki.getURL($targetDocRef, $editAction, $escapetool.url({
      'form_token': $request.form_token,
      'template': $request.template,
      'parent': $request.parent,
      'title': $request.docName
    })))
    ## Stop processing, since we already sent a redirect.
    #stop
  #end
#end
{{/velocity}}

{{velocity}}
## If this sheet is explicitly bound to the displayed class then print the class document content before the
## sheet output. Class authors can put the description of the class in the class document content.
#set($classSheetReference = $services.model.createDocumentReference($doc.wiki, 'XWiki', 'ClassSheet'))
#if($services.sheet.getDocumentSheets($doc).contains($classSheetReference))
  {{include reference="" author="target"/}}
#end
{{/velocity}}

{{velocity}}
#if (!$isSheet)
  #set ($className = $doc.pageReference.name)
  #set ($className = $stringtool.removeEnd($className, 'Class'))
  ## Determine the class sheets.
  #set ($classSheetReferences = $services.sheet.getClassSheets($doc))
  #if ($classSheetReferences.isEmpty())
    ## There is no class sheet explicitly bound to this class. Fall-back on naming convention.
    ## Before XWiki 2.0, the default class sheet was suffixed with "ClassSheet". Since 2.0, the suffix is just "Sheet".
    #set ($defaultClassSheetReference = $services.model.createDocumentReference("${className}ClassSheet",
      $doc.documentReference.parent))
    #if (!$xwiki.exists($defaultClassSheetReference))
      #set ($defaultClassSheetReference = $services.model.createDocumentReference("${className}Sheet",
        $doc.documentReference.parent))
    #end
  #end
  ## Determine the template using naming convention.
  ## Before XWiki 2.0, the default class template was suffixed with "ClassTemplate".
  ## Since 2.0, the suffix is just "Template".
  #set ($classTemplateReference = $services.model.createDocumentReference("${className}ClassTemplate",
    $doc.documentReference.parent))
  #if (!$xwiki.exists($classTemplateReference))
    #set ($classTemplateReference = $services.model.createDocumentReference("${className}Template",
      $doc.documentReference.parent))
  #end
  ## Determine the template provider using naming convention.
  #set ($classTemplateProviderReference = $services.model.createDocumentReference("${className}TemplateProvider",
    $doc.documentReference.parent))
  #set ($classTemplateProviderDoc = $xwiki.getDocument($classTemplateProviderReference))
  #set ($hasClassTemplateProvider = !$classTemplateProviderDoc.isNew())
  #set($classTemplateDoc = $xwiki.getDocument($classTemplateReference))
  #set($hasClassSheets = !$classSheetReferences.isEmpty() || $xwiki.exists($defaultClassSheetReference))
  #set($hasClassTemplate = !$classTemplateDoc.isNew())
  #if(!$defaultSpace)
    #set($defaultSpace = $doc.space)
  #end
  #if(!$defaultParent)
    #set($defaultParent = ${doc.fullName})
  #end

  #set ($classEditorURL = $doc.getURL('edit', 'editor=class'))
  #if($doc.getxWikiClass().properties.size() == 0)
    #set ($openLink = "<a href='$escapetool.xml($classEditorURL)'>")
    #set ($closeLink = '</a>')
    {{warning}}
      {{html}}
      ## First escape the content of the translation, then replace the placeholders with content that would otherwise be
      ## escaped during the first escaping.
      #set ($warningMessage = $services.localization.render('platform.xclass.defaultClassSheet.properties.empty', 
        ['__OPEN_LINK__', '__CLOSE_LINK__']))
      $escapetool.xml($warningMessage).replace('__OPEN_LINK__', $openLink).replace('__CLOSE_LINK__', $closeLink)
      {{/html}}
    {{/warning}}
  #else
    (% id="HClassProperties" %)
    = {{translation key="platform.xclass.defaultClassSheet.properties.heading"/}} =
    #foreach($property in $doc.getxWikiClass().properties)
      * $services.rendering.escape("$property.prettyName ($property.name: $xwiki.metaclass.get($property.classType).prettyName)", $xwiki.currentContentSyntaxId)
    #end
    #set ($openLink = "<a href='$escapetool.xml($classEditorURL)'>")
    #set ($closeLink = '</a>')
    #set ($warningMessage = $escapetool.xml($services.localization.render('platform.xclass.defaultClassSheet.properties.edit', ['__OPEN_LINK__', '__CLOSE_LINK__'])))
    ## First escape the content of the translation, then replace the placeholders with content that would otherwise be
    ## escaped during the first escaping.
    * //{{html}}$warningMessage.replace('__OPEN_LINK__', $openLink).replace('__CLOSE_LINK__', $closeLink){{/html}}//

  #end
  #if ($hasClassSheets && $hasClassTemplate)
    (% id="HCreatePage" %)
    = {{translation key="platform.xclass.defaultClassSheet.createPage.heading"/}} =
    #if("$!targetDocRef" != '' && $xwiki.exists($targetDocRef))
      {{warning}}
        {{html}}
          #set ($targetDocLink = $xwiki.getURL($targetDocRef))
          #set ($openLink = "<a href='$escapetool.xml($targetDocLink)'>")
          #set ($message = $escapetool.xml($services.localization.render('platform.xclass.defaultClassSheet.createPage.pageAlreadyExists', ['__OPEN_LINK__', '__CLOSE_LINK__'])))
          ## First escape the content of the translation, then replace the placeholders with content that would
          ## otherwise be escaped during the first escaping.
          $message.replace('__OPEN_LINK__', $openLink).replace('__CLOSE_LINK__', '</a>')
        {{/html}}
      {{/warning}}
    #elseif("$!targetDocRef" != '')

      {{warning}}{{translation key="platform.xclass.defaultClassSheet.createPage.denied"/}}{{/warning}}
    #end

    {{html}}
    <form action="$doc.getURL()" id="newdoc" method="post" class="xform half">
      <fieldset>
      <div class="hidden">
        <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
        <input type="hidden" name="parent" value="$escapetool.xml(${defaultParent})"/>
        <input type="hidden" name="template" value="$escapetool.xml(${classTemplateDoc})"/>
        <input type="hidden" name="sheet" value="1"/>
      </div>
      #locationPicker({
        'id': 'target',
        'title': {
          'label': 'core.create.title',
          'hint': 'core.create.title.hint',
          'name': 'docTitle',
          'placeholder': 'core.create.name.placeholder'
        },
        'preview': {
          'label': 'core.create.locationPreview.label',
          'hint': 'core.create.locationPreview.hint'
        },
        'parent': {
          'label': 'core.create.spaceReference.label',
          'hint': 'core.create.spaceReference.hint',
          'name': 'spaceName',
          'reference': $services.model.resolveSpace($defaultSpace),
          'placeholder': 'core.create.spaceReference.placeholder'
        },
        'name': {
          'label': 'core.create.name.label',
          'hint': 'core.create.name.hint',
          'name': 'docName',
          'placeholder': 'core.create.name.placeholder'
        }
      })
      <p>
        <span class="buttonwrapper">
          <input type="submit" class="button" value="$escapetool.xml($services.localization.render(
            'platform.xclass.defaultClassSheet.createPage.label'))"/>
        </span>
      </p>
      </fieldset>
    </form>
    {{/html}}

  #end## has class sheet and class template
  (% id="HExistingPages" %)
  = {{translation key="platform.xclass.defaultClassSheet.pages.heading"/}} =

  {{translation key="platform.xclass.defaultClassSheet.pages.description"/}}

  #set ($options = {
    'className': $doc.fullName,
    'translationPrefix' : 'platform.index.',
    'queryFilters': ['unique']
  })
  {{liveData
    id="classEntries"
    properties="doc.title,doc.location,doc.date,doc.author,doc.objectCount,_actions"
    source="liveTable"
    className="$services.rendering.escape(${doc.fullName}, 'xwiki/2.1')"
    sourceParameters="$services.rendering.escape($escapetool.url($options), 'xwiki/2.1')"
  }}
  {
    "meta": {
      "propertyDescriptors": [
        {
          "id": "doc.title",
          "editable": false
        },
        {
          "id": "doc.objectCount",
          "editable": false,
          "filterable": false,
          "sortable": false
        }
      ]
    }
  }
  {{/liveData}}

  (% id="HClassSheets" %)
  = {{translation key="platform.xclass.defaultClassSheet.sheets.heading"/}} =
  #if (!$hasClassSheets || !$hasClassTemplate)

    {{translation key="platform.xclass.defaultClassSheet.sheets.missing"/}}
  #end

  {{info}}
    #set ($message = $services.localization.render('platform.xclass.defaultClassSheet.sheets.description', ['__START_EM__', '__END_EM__']))
    #set ($message = $escapetool.xml($message))
    ## First escape the content of the translation, then replace the placeholders with content that would
    ## otherwise be escaped during the first escaping.
    {{html}}$message.replace('__START_EM__', '<em>').replace('__END_EM__', '</em>'){{/html}}
  {{/info}}

  #if(!$hasClassSheets)
    {{html}}
      <form action="$xwiki.getURL($defaultClassSheetReference, 'save', 'editor=wiki')" method="post">
        <div>
          <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
          <input type="hidden" name="parent" value="$escapetool.xml(${doc.fullName})"/>
          <input type="hidden" name="xredirect" value="$escapetool.xml(${doc.URL})"/>
          #set ($sheetContent = $xwiki.getDocument('XWiki.ObjectSheet').getContent().replace('XWiki.MyClass',
            $doc.fullName))
          ## We have to encode the new line characters in order to preserve them, otherwise they are replace with a
          ## space when the HTML is cleaned.
          ## FIXME: Use a dedicated escape tool method when XCOMMONS-405 is implemented.
          #set ($sheetContent = $escapetool.xml($sheetContent).replaceAll("\n", '&#10;'))
          <input type="hidden" name="content" value="$sheetContent"/>
          <input type="hidden" name="title" value="${escapetool.h}if(${escapetool.d}doc.documentReference.name == '$escapetool.xml($defaultClassSheetReference.name)')$escapetool.xml($className) Sheet${escapetool.h}{else}${escapetool.d}services.display.title(${escapetool.d}doc, {'displayerHint': 'default', 'outputSyntaxId': 'plain/1.0'})${escapetool.h}end"/>
          <span class="buttonwrapper"><input type="submit" class="button" value="$escapetool.xml(
            $services.localization.render('platform.xclass.defaultClassSheet.sheets.create'))"/></span>
        </div>
      </form>
    {{/html}}
  #else
    #set($defaultClassSheetDoc = $xwiki.getDocument($defaultClassSheetReference))
    #if($classSheetReferences.isEmpty() && !$defaultClassSheetDoc.getObject('XWiki.SheetClass'))
      ## The sheet is not bound to the class.
      #set($xredirect = $xwiki.relativeRequestURL)
      #set($defaultClassSheetStringReference = $services.model.serialize($defaultClassSheetReference, "default"))
      #set($bindURL = $doc.getURL('view', "bindSheet=${escapetool.url($defaultClassSheetStringReference)}&xredirect=${escapetool.url($xredirect)}&form_token=$!{services.csrf.getToken()}"))
      {{warning}}
        {{translation key="platform.xclass.defaultClassSheet.sheets.notBound"/}} ##
        #if ($hasEdit)
          {{html}}
          <a href="$escapetool.xml($bindURL)">##
            $escapetool.xml($services.localization.render('platform.xclass.defaultClassSheet.sheets.bind')) »##
          </a>.
          {{/html}}
        #end
      {{/warning}}

    #end
    #if ($classSheetReferences.size() < 2)
      #set($classSheetDoc = $defaultClassSheetDoc)
      #if(!$classSheetReferences.isEmpty())
        #set($classSheetDoc = $xwiki.getDocument($classSheetReferences.get(0)))
      #end
      #set ($sheetPath = "#hierarchy($classSheetDoc.documentReference, {'plain': true, 'local': true, 'limit': 4})")
      #set ($classSheetLink = "$services.localization.render('platform.xclass.defaultClassSheet.sheets.view', [$sheetPath.trim()]) »")
      #set ($classSheetLink = $services.rendering.escape($classSheetLink, 'xwiki/2.1'))
      #set ($classSheetLink = $services.rendering.escape($classSheetLink, 'xwiki/2.1'))
      #set ($classSheetText = ${classSheetDoc.fullName})
      #set ($classSheetText = $services.rendering.escape($classSheetText, 'xwiki/2.1'))
      [[$classSheetLink>>$classSheetText]]
    #else
      {{translation key="platform.xclass.defaultClassSheet.sheets.list"/}}

      #foreach($classSheetReference in $classSheetReferences)
        * [[$services.model.serialize($classSheetReference, "default")]]
      #end
    #end
  #end

  (% id="HClassTemplate" %)
  = {{translation key="platform.xclass.defaultClassSheet.template.heading"/}} =

    {{info}}
      #set ($message = $services.localization.render('platform.xclass.defaultClassSheet.template.description', ['__START_EM__', '__END_EM__']))
      #set ($message = $escapetool.xml($message))
      ## First escape the content of the translation, then replace the placeholders with content that would
      ## otherwise be escaped during the first escaping.
      {{html}}$message.replace('__START_EM__', '<em>').replace('__END_EM__', '</em>'){{/html}}
    {{/info}}

  #if (!$hasClassTemplate)
    {{html}}
      <form action="$escapetool.xml($classTemplateDoc.getURL('save', 'editor=wiki'))" method="post">
        <div>
          <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
          <input type="hidden" name="parent" value="$escapetool.xml(${doc.fullName})"/>
          <input type="hidden" name="xredirect" value="$escapetool.xml(${doc.URL})"/>
          <input type="hidden" name="title" value="$escapetool.xml($className) Template"/>
          <span class="buttonwrapper"><input type="submit" class="button" value="$escapetool.xml(
            $services.localization.render('platform.xclass.defaultClassSheet.template.create'))"/></span>
        </div>
      </form>
    {{/html}}
  #else
    #if(!$classTemplateDoc.getObject(${doc.fullName}))
      #set($xredirect = $xwiki.relativeRequestURL)
      #set($createUrl = $classTemplateDoc.getURL('objectadd', "classname=${escapetool.url($doc.fullName)}&xredirect=${escapetool.url($xredirect)}&form_token=$!{services.csrf.getToken()}"))
      {{warning}}
        #set ($message = $services.localization.render('platform.xclass.defaultClassSheet.template.missingObject', ['__CLASS_NAME__']))
        #set ($message = $escapetool.xml($message))
        {{html}}
          ## First escape the content of the translation, then replace the placeholders with content that would
          ## otherwise be escaped during the first escaping.
          $message.replace('__CLASS_NAME__', "<em>$escapetool.xml($className)</em>")
          <a href="$escapetool.xml($createUrl)">##
            $escapetool.xml($services.localization.render('platform.xclass.defaultClassSheet.template.addObject', [$className])) »##
          </a>.
        {{/html}}
      {{/warning}}

    #end
    #set ($templatePath = "#hierarchy($classTemplateDoc.documentReference, {'plain': true, 'local': true, 'limit': 4})")
    #set ($templateDocLink = "$services.localization.render('platform.xclass.defaultClassSheet.template.view', [$templatePath.trim()]) »")
    #set ($templateDocLink = $services.rendering.escape($templateDocLink, 'xwiki/2.1'))
    #set ($templateDocLink = $services.rendering.escape($templateDocLink, 'xwiki/2.1'))
    #set ($templateDocText = "${classTemplateDoc.fullName}")
    ## First escape the xwiki/2.1 syntax of the translation, then replace the placeholders with content that would
    ## otherwise be escaped during the first escaping.
    #set ($templateDocText = $services.rendering.escape($templateDocText, 'xwiki/2.1'))
    [[$templateDocLink>>$templateDocText]]
  #end
  ## Create a template provider only if a template for the current class exists.
  #if ($classTemplateDoc.getObject(${doc.fullName}))
    (% id="HClassTemplateProvider" %)
    = {{translation key="platform.xclass.defaultClassSheet.templateProvider.heading"/}} =

      {{info}}
        #set ($message = $services.localization.render('platform.xclass.defaultClassSheet.templateProvider.description', ['__EM__']))
        #set ($message = $services.rendering.escape($message, 'xwiki/2.1'))
        ## First escape the xwiki/2.1 syntax of the translation, then replace the placeholders with content that would
        ## otherwise be escaped during the first escaping.
        ## The replacement key is itself escaped, and it's escaped form needs to be used for the replacement.
        $message.replace('~_~_~E~M~_~_', '//')
      {{/info}}

    #if (!$hasClassTemplateProvider)
      #set ($templateProviderClassName = 'XWiki.TemplateProviderClass')
      ## Do the page creation and object addition in one step, providing some default values.
      ## In order to get the root space of the class and use it as restrictionSpace, we need to be sure that we have
      ## the expected result for multiple level hierarchies, like MyApplication.Code.MyApplicationClass. In this case,
      ## the template provider in enabled in MyApplication space.
      #set ($restrictionSpace = $doc.documentReference.spaceReferences.get(0).name)
      #set ($createUrlQueryString = $escapetool.url({
        'classname': $templateProviderClassName,
        'xredirect': $xwiki.relativeRequestURL,
        'form_token': $services.csrf.token,
        "${templateProviderClassName}_name": $className,
        "${templateProviderClassName}_description":
          $services.localization.render('platform.xclass.templateProvider.defaultDescription', [$className]),
        "${templateProviderClassName}_template": $classTemplateDoc,
        "${templateProviderClassName}_visibilityRestrictions": $restrictionSpace}))
      #set ($createUrl = $classTemplateProviderDoc.getURL('objectadd', $createUrlQueryString))
      {{html}}
        <form action="$escapetool.xml($classTemplateProviderDoc.getURL('save', 'editor=wiki'))" method="post">
          <div>
            <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
            <input type="hidden" name="parent" value="$escapetool.xml(${doc.fullName})"/>
            <input type="hidden" name="xredirect" value="$escapetool.xml($createUrl)"/>
            <input type="hidden" name="title" value="$escapetool.xml($className) Template Provider"/>
            <span class="buttonwrapper"><input type="submit" class="button" value="$escapetool.xml(
              $services.localization.render('platform.xclass.defaultClassSheet.templateProvider.create'))"/></span>
          </div>
        </form>
      {{/html}}
    #else
      #set ($templateProviderPath = "#hierarchy($classTemplateProviderDoc.documentReference, {'plain': true, 'local': true, 'limit': 4})")
      #set ($linkTarget = "$services.localization.render('platform.xclass.defaultClassSheet.templateProvider.view', [$templateProviderPath.trim()]) »")
      #set ($linkTarget = $services.rendering.escape($linkTarget, 'xwiki/2.1'))
      #set ($linkTarget = $services.rendering.escape($linkTarget, 'xwiki/2.1'))
      #set ($linkLabel = $services.rendering.escape(${classTemplateProviderDoc.fullName}, 'xwiki/2.1'))
      [[$linkTarget>>$linkLabel]]
    #end
  #end

#end## !$isSheet
{{/velocity}}
