---
id: xwiki-xwiki:XWiki.XWikiClasses
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906694000
sync_date: 2026-07-21 11:02:15
tags:
  - xwiki/documentation
  - space/xwiki
---
# Data types

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906694000
- **Source:** [Data types](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.XWikiClasses)

---

{{template name="locationPicker_macros.vm" /}}

{{velocity output="false"}}
#if ($request.space && $request.name)
  #set ($className = "#toXMLName($stringtool.removeEnd($request.name, 'Class'))")
  #set ($classTitle = $stringtool.removeEnd($request.title, 'Class'))
  #if ("$!classTitle" == '')
    #set ($classTitle = $className)
  #end
  #set ($classTitle = "$classTitle Class")
  #set ($classSpaceReference = $services.model.resolveSpace($request.space))
  #set ($classReference = $services.model.createEntityReference("${className}Class", 'DOCUMENT', $classSpaceReference))
  #if ($services.security.authorization.hasAccess('edit', $classReference))
    $response.sendRedirect($xwiki.getURL($classReference, 'edit', $escapetool.url({
      'editor': 'wiki',
      'template': $request.template,
      'parent': $request.parent,
      'title': $classTitle,
      'form_token': $services.csrf.token
    })))
    ## Stop processing, since we already sent a redirect.
    #stop
  #end
#end
{{/velocity}}

{{velocity}}
$services.localization.render('platform.xclass.classes.description', [
  '[[',
  '>>http://www.xwiki.org/xwiki/bin/view/Documentation/DevGuide/]]'
])

(% id="HClassTemplates" %)
= {{translation key="platform.xclass.classes.templates.heading"/}} =

{{translation key="platform.xclass.classes.templates.description"/}}

* [[$services.localization.render('platform.xclass.classes.templates.classSheet')>>ClassSheet]]
* [[$services.localization.render('platform.xclass.classes.templates.classTemplate')>>ClassTemplate]]
* [[$services.localization.render('platform.xclass.classes.templates.objectSheet')>>ObjectSheet]]

(% id="HCreateClass" %)
= {{translation key="platform.xclass.classes.createClass.heading"/}} =

$services.localization.render('platform.xclass.classes.createClass.description', ['//', '//'])

#if ("$!classReference" != '')
  {{warning}}{{translation key="platform.xclass.classes.createClass.denied"/}}{{/warning}}

#end
{{html}}
<form action="$doc.URL" method="post" class="xform half">
  <fieldset>
  <div class="hidden">
    <input type="hidden" name="parent" value="XWiki.XWikiClasses"/>
    <input type="hidden" name="template" value="XWiki.ClassTemplate"/>
  </div>
  #locationPicker({
    'id': 'target',
    'title': {
      'label': 'core.create.title',
      'hint': 'platform.xclass.classes.createClass.title.hint',
      'name': 'title',
      'placeholder': 'platform.xclass.classes.createClass.title.placeholder'
    },
    'preview': {
      'label': 'core.create.locationPreview.label',
      'hint': 'platform.xclass.classes.createClass.location.hint'
    },
    'parent': {
      'label': 'core.create.spaceReference.label',
      'hint': 'platform.xclass.classes.createClass.parent.hint',
      'name': 'space',
      'reference': $doc.documentReference.parent,
      'placeholder': 'platform.xclass.classes.createClass.parent.placeholder'
    },
    'name': {
      'label': 'core.create.name.label',
      'hint': 'platform.xclass.classes.createClass.name.hint',
      'name': 'name',
      'placeholder': 'platform.xclass.classes.createClass.title.placeholder'
    }
  })
  <p>
    <span class="buttonwrapper">
      <input type="submit" class="button" value="$escapetool.xml(
        $services.localization.render('platform.xclass.classes.createClass.label'))"/>
    </span>
  </p>
  </fieldset>
</form>
{{/html}}
{{/velocity}}

(% id="HClassesLiveTable" %)
= {{translation key="platform.xclass.classes.livetable.heading"/}} =

{{liveData
  id="classes"
  properties="doc.title,doc.location,doc.date,doc.author,pageCount,_actions"
  source="liveTable"
  sourceParameters="resultPage=XWiki.XWikiClassesLiveTableResults&translationPrefix=platform.xclass.classes.livetable.&queryFilters="
  }}
{
  "meta": {
    "propertyDescriptors": [
      {
        "id": "doc.title",
        "editable": false
      },
      {
        "id": "pageCount",
        "editable": false,
        "filterable": false,
        "sortable": false,
        "displayer": "number"
      }
    ]
  }
}
{{/liveData}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
