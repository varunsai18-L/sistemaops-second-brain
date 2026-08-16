---
id: xwiki-AppWithinMinutes.Content
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906757000
sync_date: 2026-08-16 19:45:26
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Content

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906757000
- **Source:** [Content](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.Content)

---

{{velocity}}
#if ($type == 'edit')
  #set ($className = $object.getxWikiClass().name)
  #if ($doc.fullName == $className)
    ## We are editing the class so the content must be read from / written to the template document.
    #set ($name = 'templateContent')
    #set ($editedDocument = $xwiki.getDocument("$stringtool.removeEnd($className, 'Class')Template"))
  #else
    ## We are editing an application entry so the content must be read from / written to the current document.
    #set ($name = 'content')
    #set ($editedDocument = $tdoc)
  #end
  ## Use the preferred content editor.
  #set ($useWysiwygEditor = $xwiki.getUserPreference('editor') == 'Wysiwyg')
  {{html clean="false"}}
  ## The "content" id is expected by some JavaScript and CSS code.
  #set ($id = 'content')
  #if (!$useWysiwygEditor)
    <div id="xwikieditcontentinner">
      ## The tool bar may have an entry to insert an HTML macro. Make sure it doesn't break the HTML macro we are currently in.
      #set ($toolBar = "#template('simpleedittoolbar.vm')")
      $!toolBar.replace('{{', '&#123;&#123;')
      ## Display a simple textarea.
      <textarea id="$escapetool.xml($id)" cols="80" rows="25" name="$name"
      data-syntax="$escapetool.xml($doc.syntax.toIdString())">$escapetool.xml($editedDocument.content)</textarea>
  #end
  #if ($useWysiwygEditor)
    $!services.edit.syntaxContent.wysiwyg($editedDocument.content, $editedDocument.syntax, {
      'id': "$id",
      'name': "$name",
      'rows': 25,
      'cols': 80,
      'full': true,
      'restricted': $editedDocument.isRestricted()
    })
  #else
    </div>
  #end
  {{/html}}
#elseif ("$!type" != '')
  ## Display the content of the current document without using any sheet. We can't use the include macro here (with the
  ## author parameter) because the content may have unsaved changes (e.g. on preview action). We make sure that the HTML
  ## macro is not closed unintentionally, even though the XHTML printer protects us against this, just to be extra safe.
  {{html}}$services.display.content($tdoc, {
    'displayerHint': 'default'
  }).replace('{{/html}}', '&amp;#123;&amp;#123;/html&amp;#125;&amp;#125;'){{/html}}
#else
  The display mode is not specified!
#end
{{/velocity}}
