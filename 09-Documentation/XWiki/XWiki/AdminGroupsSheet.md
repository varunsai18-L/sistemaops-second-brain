---
id: xwiki-XWiki.AdminGroupsSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905806000
sync_date: 2026-08-25 21:13:11
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminGroupsSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905806000
- **Source:** [AdminGroupsSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminGroupsSheet)

---

{{velocity output="false"}}
#macro (createGroupModal)
  <div class="modal" id="createGroupModal" tabindex="-1" role="dialog"
      aria-labelledby="createGroupModal-label" data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog" role="document">
      <form class="modal-content xform">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="createGroupModal-label">
            $escapetool.xml($services.localization.render('rightsmanager.creategroup'))
          </div>
        </div>
        <div class="modal-body">
          <div class="hidden">
            <input type="hidden" name="form_token" value="$!services.csrf.token" />
            <input type="hidden" name="template" value="XWiki.XWikiGroupTemplate" />
          </div>
          <dl>
            <dt>
              <label for="createGroupModal-groupName" class="sr-only">
                $escapetool.xml($services.localization.render('xe.admin.groups.name'))
              </label>
            </dt>
            <dd class="form-group has-feedback">
              <input type="text" class="form-control" id="createGroupModal-groupName" name="name" autocomplete="off"
                placeholder="$escapetool.xml($services.localization.render('xe.admin.groups.name'))" />
              <span class="form-control-feedback loading hidden" aria-hidden="true"></span>
              <span class="form-control-feedback success hidden" aria-hidden="true">$services.icon.renderHTML('check')</span>
              <span class="form-control-feedback error hidden" aria-hidden="true">$services.icon.renderHTML('cross')</span>
              <span class="help-block hidden"></span>
            </dd>
          </dl>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $escapetool.xml($services.localization.render('cancel'))
          </button>
          <button type="submit" class="btn btn-primary">
            $escapetool.xml($services.localization.render('create'))
          </button>
        </div>
      </form>
    </div>
  </div>
#end

#macro (editGroupModal)
  <div class="modal" id="editGroupModal" tabindex="-1" role="dialog" aria-labelledby="editGroupModal-label"
      data-backdrop="static" data-keyboard="false" data-live-data="#groupstable" data-live-data-action="edit">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="editGroupModal-label">
            $escapetool.xml($services.localization.render('xe.admin.groups.editGroup'))
          </div>
        </div>
        <div class="modal-body"></div>
      </div>
    </div>
  </div>
#end

#macro (deleteGroupModal)
  <div class="modal" id="deleteGroupModal" tabindex="-1" role="dialog" aria-labelledby="deleteGroupModal-label"
       data-live-data="#groupstable" data-live-data-action="delete">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="deleteGroupModal-label">
            $escapetool.xml($services.localization.render('xe.admin.groups.deleteGroup'))
          </div>
        </div>
        <div class="modal-body">
          #set ($message = $escapetool.xml($services.localization.render('rightsmanager.confirmdeletegroup')))
          <p>$message.replace('__name__', '<span class="groupName"></span>')</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $escapetool.xml($services.localization.render('cancel'))
          </button>
          <button type="submit" class="btn btn-danger" data-dismiss="modal">
            $escapetool.xml($services.localization.render('delete'))
          </button>
        </div>
      </div>
    </div>
  </div>
#end
{{/velocity}}

{{velocity}}
{{html clean="false"}}
#set ($discard = $xwiki.ssx.use('XWiki.AdminGroupsSheet'))
#set ($discard = $xwiki.jsx.use('XWiki.AdminGroupsSheet'))
## The following are needed when editing a group (e.g., for adding new members).
#userPicker_import()
#set ($discard = $xwiki.ssx.use('XWiki.XWikiGroupSheet'))
#set ($discard = $xwiki.jsx.use('XWiki.XWikiGroupSheet'))
#set ($properties = ['name', 'members', '_actions'])
#if (!$xcontext.isMainWiki())
  #set ($discard = $properties.add(2, 'scope'))
#end
<div class="medium-avatars">
  #set ($sourceParameters = {
      'template': 'getgroups.vm',
      'translationPrefix': 'xe.admin.groups.'
  })
  $services.liveData.render({
    'id': 'groupstable',
    'source': 'liveTable',
    'properties': $stringtool.join($properties, ','),
    'sourceParameters': $escapetool.url($sourceParameters)
  }, {
    'query': {
        'filters': [
          {
            'property': 'scope',
            'constraints': [{
              'operator': 'contains',
              'value': 'local'
            }]
          }
        ]
      },
    'meta': {
      'propertyDescriptors': [
        {
          'id': 'name',
          'displayer': 'html',
          'sortable': false,
          'editable': false
        },
        {
          'id': 'members',
          'sortable': false,
          'filterable': false,
          'editable': false
        },
        {
          'id': 'scope',
          'sortable': false,
          'editable': false,
          'filter': {
            'id': 'list',
            'options': [
              {'value': 'local', 'label': $services.localization.render('xe.admin.groups.local')},
              {'value': 'global', 'label': $services.localization.render('xe.admin.groups.global')},
              {'value': 'both', 'label': $services.localization.render('xe.admin.groups.both')}
            ]
          }
        },
        {
          'id': '_actions',
          'displayer': {
            'id': 'actions',
            'actions': ['edit', 'delete']
          }
        }
      ],
      'actions': [
        {
          'id': 'delete',
          'name': $services.localization.render('platform.livetable._actions.delete')
        }
      ]
    }
  })
</div>
<p>
  <button type="button" class="btn btn-primary" data-toggle="modal" data-target="${escapetool.h}createGroupModal">
    $escapetool.xml($services.localization.render('rightsmanager.creategroup'))
  </button>
</p>
#createGroupModal()
#editGroupModal()
#deleteGroupModal()
{{/html}}
{{/velocity}}
