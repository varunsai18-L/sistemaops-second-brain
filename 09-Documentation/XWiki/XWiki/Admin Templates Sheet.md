---
id: xwiki-xwiki:XWiki.AdminTemplatesSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905800000
sync_date: 2026-07-21 11:01:05
tags:
  - xwiki/documentation
  - space/xwiki
---
# Admin Templates Sheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905800000
- **Source:** [Admin Templates Sheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.AdminTemplatesSheet)

---

{{velocity}}
## Create form, left column.
(% class="col-xs-12 col-md-6" %)(((
(% id="HAdminTemplatesCreateProvider" %)
== {{translation key="admin.templates.createprovider"/}} ==

{{html}}
  <form class="xform" action="$doc.getURL('create')" method="post">
    <fieldset>
    #template('locationPicker_macros.vm')
    #locationPicker({
      'id': 'target',
      'title': {
        'label': 'core.create.title',
        'hint': 'core.create.title.hint',
        'name': 'title',
        'placeholder': 'admin.templates.createprovider.defaultdocname'
      },
      'preview': {
        'label': 'core.create.locationPreview.label',
        'hint': 'core.create.locationPreview.hint'
      },
      'parent': {
        'label': 'core.create.spaceReference.label',
        'hint': 'core.create.spaceReference.hint',
        'name': 'spaceReference',
        'reference': $doc.documentReference.lastSpaceReference,
        'placeholder': 'core.create.spaceReference.placeholder'
      },
      'name': {
        'label': 'core.create.name.label',
        'hint': 'core.create.name.hint',
        'name': 'name',
        'value': '',
        'placeholder': 'admin.templates.createprovider.defaultdocname'
      }
    })
    #if ($isAdvancedUser || $isSuperAdmin)
      <dl>
        <dt>
          <label for="terminal">
            <input type="checkbox" id="terminal" name="tocreate" value="terminal" checked="checked" />
            $services.localization.render('core.create.terminal.label')
          </label>
        </dt>
        <dd>
          <span class="xHint">$services.localization.render('core.create.terminal.hint')</span>
        </dd>
      </dl>
    #else
      <input type="hidden" id="terminal" name="tocreate" value="terminal" />
    #end
    <div class="buttons">
      <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
      <input type="hidden" name="parent" value="XWiki.TemplateProviderClass"/>
      <input type="hidden" name="template" value="XWiki.TemplateProviderTemplate"/>
      <span class="buttonwrapper"><input id="createTemplateProvider" type="submit" value="$services.localization.render('admin.templates.createprovider.create')" class="button"/></span>
    </div>
    </fieldset>
  </form>
{{/html}}
)))

## Available providers list, right column.
#set($availableProviders = $services.query.hql("
  , BaseObject obj
  WHERE
    doc.fullName=obj.name and obj.className='XWiki.TemplateProviderClass' and doc.fullName!='XWiki.TemplateProviderTemplate'
  ORDER BY
    doc.fullName").execute())
#if($availableProviders.size() > 0)
  (% class="col-xs-12 col-md-6" %)(((
  (% id="HAdminTemplatesProvidersList" %)
  == {{translation key="admin.templates.providerslist"/}} ==

    #foreach($providerFullname in $availableProviders)
      * [[$services.rendering.escape($services.rendering.escape($xwiki.getDocument($providerFullname).plainTitle, $xwiki.currentContentSyntaxId), $xwiki.currentContentSyntaxId)>>$services.rendering.escape($providerFullname, $xwiki.currentContentSyntaxId)]]
    #end
  )))
#end

{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
