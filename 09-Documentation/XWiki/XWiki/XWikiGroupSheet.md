---
id: xwiki-XWiki.XWikiGroupSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905791000
sync_date: 2026-08-16 19:44:49
tags:
  - xwiki/documentation
  - space/xwiki
---
# XWikiGroupSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905791000
- **Source:** [XWikiGroupSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.XWikiGroupSheet)

---

{{velocity}}
{{html clean="false"}}
#set ($discard = $xwiki.ssx.use('XWiki.XWikiGroupSheet'))
## Keep testing the inline action for backward compatibility with existing groups.
#if ($xcontext.action == 'edit' || $xcontext.action == 'inline')
  #if ($request.xpage == 'plain')
    ## AJAX request.
    #set ($wrapperTag = 'form')
    <form class="xform" action="$doc.getURL('preview')">
      <input type="hidden" name="form_token" value="$!services.csrf.token" />
  #else
    #set ($discard = $xwiki.jsx.use('XWiki.XWikiGroupSheet'))
    ## The form is generated in the edit template.
    #set ($wrapperTag = 'div')
    <div class="xform">
  #end
    <dl>
      <dt><label for="userInput">$services.localization.render('xe.admin.groups.addUser')</label></dt>
      <dd>
        #set ($parameters = {'id': 'userInput', 'name': 'name'})
        #userPicker(true $parameters)
      </dd>
      <dt><label for="groupInput">$services.localization.render('xe.admin.groups.addGroup')</label></dt>
      <dd>
        #set ($parameters = {'id': 'groupInput', 'name': 'name'})
        #groupPicker(true $parameters)
      </dd>
    </dl>
    <div class="buttons">
      <span class="buttonwrapper">
        <button type="submit" id="addMembers" name="xpage" value="adduorg">
          $services.localization.render('xe.admin.groups.addUser.submit')
        </button>
      </span>
    </div>
  </$wrapperTag>
#end
#set ($properties = ['member', 'type'])
#if (!$xcontext.isMainWiki() && $services.wiki.user.userScope != 'LOCAL_ONLY')
  #set ($discard = $properties.add('scope'))
#end
## Keep testing the inline action for backward compatibility with existing groups.
#if ($xcontext.action == 'edit' || $xcontext.action == 'inline')
  #set ($discard = $properties.add('_actions'))
#end
<div class="medium-avatars">
  #set ($sourceParameters = {
    'template': 'getgroupmembers.vm',
    'translationPrefix': 'xe.admin.groups.',
    '$doc': $doc.documentReference
  })
  $services.liveData.render({
    'id': 'groupusers',
    'source': 'liveTable',
    'properties': $stringtool.join($properties, ','),
    'sourceParameters': $escapetool.url($sourceParameters)
  }, {
    'meta': {
      'propertyDescriptors': [
        {
          'id': 'member',
          'displayer': 'html',
          'editable': false
        }
      ],
      'actions': [
        {
          'id': 'edit',
          'allowProperty': '-'
        }, {
          'id': 'delete',
          'async': {
            'httpMethod': 'POST',
            'loadingMessage': $services.localization.render('administration.section.groups.deleteUserFromGroup.loading'),
            'successMessage': $services.localization.render('administration.section.groups.deleteUserFromGroup.success'),
            'failureMessage': $services.localization.render('administration.section.groups.deleteUserFromGroup.failure')
          }
        }
      ]
    }
  })
</div>
{{/html}}
{{/velocity}}
