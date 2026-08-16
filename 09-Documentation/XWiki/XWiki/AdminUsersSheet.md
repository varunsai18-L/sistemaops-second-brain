---
id: xwiki-XWiki.AdminUsersSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905829000
sync_date: 2026-08-16 19:44:37
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminUsersSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905829000
- **Source:** [AdminUsersSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminUsersSheet)

---

{{velocity output="false"}}
#macro (displayUsersLiveData)
  #set ($properties = ['name', 'first_name', 'last_name', '_actions'])
  #set ($sourceParameters = {
    'template': 'getusers.vm',
    'translationPrefix': 'xe.admin.users.'
  })
  #if (!$xcontext.isMainWiki())
    #set ($discard = $properties.add(3, 'scope'))
  #end
  <div class="medium-avatars">
    $services.liveData.render({
      'id': 'userstable',
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
            'id': 'first_name',
            'sortable': false,
            'editable': false
          },
          {
            'id': 'last_name',
            'sortable': false,
            'editable': false
          },
          {
            'id': 'scope',
            'sortable': false,
            'editable': false,
            'filter': {
              'id': 'list',
              'options': [
                {'value': 'local', 'label': $services.localization.render('rightsmanager.local')},
                {'value': 'global', 'label': $services.localization.render('rightsmanager.global')},
                {'value': 'both', 'label': $services.localization.render('rightsmanager.both')}
              ]
            }
          },
          {
            'id': '_actions',
            'displayer': {
              'id': 'actions',
              'actions': ['edit', 'disable', 'enable', 'delete']
            }
          }
        ],
        'actions': [
          {
            'id': 'disable',
            'icon': 'lock',
            'allowProperty': 'doc.hasdisable',
            'urlProperty': 'doc.disable_url',
            'extraIconClasses': 'text-warning'
          },
          {
            'id': 'enable',
            'icon': 'unlock',
            'allowProperty': 'doc.hasenable',
            'urlProperty': 'doc.enable_url',
            'extraIconClasses': 'text-success'
          }
        ]
      }
    })
  </div>
  <p>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="${escapetool.h}createUserModal"
        ## Disable the button until the JavaScript code that handles the user creation is ready.
        disabled="disabled">
      $escapetool.xml($services.localization.render('rightsmanager.addnewuser'))
    </button>
  </p>
#end

#macro (createUserModal)
  <div class="modal" id="createUserModal" tabindex="-1" role="dialog" aria-labelledby="createUserModal-label"
      data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="createUserModal-label">
            $escapetool.xml($services.localization.render('rightsmanager.addnewuser'))
          </div>
        </div>
        <div class="modal-body"></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $escapetool.xml($services.localization.render('cancel'))
          </button>
          <button type="button" class="btn btn-primary" disabled="disabled">
            $escapetool.xml($services.localization.render('create'))
          </button>
        </div>
      </div>
    </div>
  </div>
#end

#macro (editUserModal)
  <div class="modal" id="editUserModal" tabindex="-1" role="dialog" aria-labelledby="editUserModal-label"
      data-backdrop="static" data-keyboard="false" data-live-data="#userstable" data-live-data-action="edit">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="editUserModal-label">
            $escapetool.xml($services.localization.render('xe.admin.users.editUser'))
          </div>
        </div>
        <div class="modal-body"></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $escapetool.xml($services.localization.render('cancel'))
          </button>
          <button type="button" class="btn btn-primary" disabled="disabled">
            $escapetool.xml($services.localization.render('save'))
          </button>
        </div>
      </div>
    </div>
  </div>
#end

#macro (deleteUserModal)
  ## Load the resources needed by the user picker in order to be able to select the new author when deleting users that
  ## have script or programming rights.
  #userPicker_import
  <div class="modal" id="deleteUserModal" tabindex="-1" role="dialog" aria-labelledby="deleteUserModal-label"
      data-live-data="#userstable" data-live-data-action="delete">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="modal-title" id="deleteUserModal-label">
            $escapetool.xml($services.localization.render('xe.admin.users.deleteUser'))
          </div>
        </div>
        <div class="modal-body loading"></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            $escapetool.xml($services.localization.render('cancel'))
          </button>
          <button type="button" class="btn btn-danger" data-dismiss="modal">
            $escapetool.xml($services.localization.render('delete'))
          </button>
        </div>
      </div>
    </div>
  </div>
#end

#macro (deleteUserModalContent $userReference)
  {{html clean="false"}}
  #set ($userReference = $services.model.resolveDocument($userReference, 'user', $doc.documentReference))
  <p>$services.localization.render('administration.section.users.deleteUser.confirmationMessage', [
    "#displayUser($userReference {'useInlineHTML': true})",
    "<a href='$xwiki.getURL($userReference, 'view', 'category=groups')'>",
    '</a>'
  ])</p>
  ## Check if the user we're about to delete has programming or script rights because in this case deleting the user may
  ## break the pages where this user was the last (content) author.
  ##
  ## Note that we check programming and script rights at the wiki level only, in the wiki where the user is defined.
  ## This doesn't cover all the cases because script right can be set at page level so it's possible that the user has
  ## script right only on some pages (and not at the wiki level). Counting the pages that were last modified by this
  ## user and for which they have script right is costly (we need to check script right separately for each page that
  ## was last modified by the user, we can't do it in the database query).
  #set ($wikiPrefsRef = $services.model.createDocumentReference($userReference.wikiReference.name, 'XWiki',
    'XWikiPreferences'))
  #if ($services.security.authorization.hasAccess('programming', $userReference, $wikiPrefsRef))
    #maybeShowDeleteUserWarning($userReference 'programming')
  #elseif ($services.security.authorization.hasAccess('script', $userReference, $wikiPrefsRef))
    #maybeShowDeleteUserWarning($userReference 'script')
  #end
  {{/html}}
#end

#macro (maybeShowDeleteUserWarning $userReference $right)
  #countPagesLastModifiedBy($userReference)
  #if ($pageCount > 0)
    {{/html}}
    
    {{error cssClass="xform"}}
      {{html}}
      #set ($pageIndexReference = $services.model.createDocumentReference(
        $userReference.wikiReference.name, 'Main', 'AllDocs'))
      #set ($pageIndexURL = $xwiki.getURL($pageIndexReference, 'view', "doc.author=${escapetool.url($services.model.serialize($userReference, 'local'))}"))
      #set ($translationKey = "administration.section.users.deleteUser.${right}RightsWarning")
      $services.localization.render($translationKey, ["<a href='$pageIndexURL'>", $pageCount, '</a>'])
      <dl>
        <dt>
          <label for="newAuthor">$escapetool.xml($services.localization.render(
            'administration.section.users.deleteUser.newAuthor'))</label>
          #set ($translationKey = 'administration.section.users.deleteUser.newAuthor.hint')
          #set ($rightTranslation = $services.localization.render(
            "administration.section.users.deleteUser.newAuthor.$right"))
          <span class="xHint">$escapetool.xml($services.localization.render($translationKey,
            [$rightTranslation]))</span>
        </dt>
        <dd>
          #set ($userPickerParams = {
            'id': 'newAuthor',
            'name': 'newAuthor',
            'data-required-right': $right
          })
          #userPicker(false $userPickerParams)
          #set ($translationKey = 'administration.section.users.deleteUser.newAuthor.error')
          <span class="xErrorMsg hidden">$escapetool.xml($services.localization.render($translationKey,
            [$rightTranslation]))</span>
        </dd>
      </dl>
      {{/html}}
    {{/error}}
    
    {{html clean="false"}}
  #end
#end

#macro (countPagesLastModifiedBy $userReference)
  #if ($userReference.wikiReference.name == $xcontext.mainWikiName)
    ## Global user: search everywhere.
    #set ($wikis = $services.wiki.allIds)
  #else
    ## Local user: search only in the wiki where the user is defined.
    #set ($wikis = [$userReference.wikiReference.name])
  #end
  #set ($pageCount = 0)
  #set ($statement = 'where doc.author = :user or doc.contentAuthor = :user')
  #foreach ($wiki in $wikis)
    #if ($userReference.wikiReference.name == $wiki)
      #set ($userReferenceString = $services.model.serialize($userReference, 'local'))
    #else
      #set ($userReferenceString = $services.model.serialize($userReference, 'default'))
    #end
    #set ($pageCount = $pageCount + $services.query.xwql($statement).setWiki($wiki).addFilter('unique'
      ).bindValue('user', $userReferenceString).count())
  #end
#end

#macro (validateNewAuthor $newAuthorReference $requiredRight)
  #set ($newAuthorReference = $services.model.resolveDocument($newAuthorReference, 'user', $doc.documentReference))
  #set ($wikiPrefsRef = $services.model.createDocumentReference($newAuthorReference.wikiReference.name, 'XWiki',
    'XWikiPreferences'))
  #jsonResponse({
    'valid': $services.security.authorization.hasAccess($requiredRight, $newAuthorReference, $wikiPrefsRef)
  })
#end

#macro (doView)
  ## We include new settings from the Wiki Manager (only if it is not the main wiki).
  #set ($wikiManagerUserRef = $services.model.createDocumentReference('', 'WikiManager', 'WikiUsers'))
  #if (!$xcontext.isMainWiki() && $xwiki.exists($wikiManagerUserRef))
    {{include reference="WikiManager.WikiUsers" /}}
  #end
  ## The Users management is enabled:
  ## - on the main wiki
  ## - on a subwiki where local users are enabled
  ## - on a subwiki if there is no service "$services.wiki.user"
  #if ($xcontext.isMainWiki() || "$!services.wiki.user" == '' || "$!services.wiki.user.userScope" != 'GLOBAL_ONLY')
    ##
    ## Inject needed JS and CSS files
    ##
    #set ($discard = $xwiki.ssx.use("XWiki.XWikiUserSheet"))
    #set ($discard = $xwiki.ssx.use("XWiki.AdminUsersSheet"))
    #set ($discard = $xwiki.jsx.use("XWiki.AdminUsersSheet"))

    {{html clean="false"}}
    #displayUsersLiveData()
    #createUserModal()
    #editUserModal()
    #deleteUserModal()
    {{/html}}
  #end
#end
{{/velocity}}

{{velocity}}
#if ($request.data == 'deleteUserModalContent' && "$!request.userReference" != '')
  #deleteUserModalContent($request.userReference)
#elseif ($request.data == 'validateNewAuthor' && "$!request.newAuthor" != '' && "$!request.requiredRight" != '')
  #validateNewAuthor($request.newAuthor $request.requiredRight)
#else
  #doView
#end
{{/velocity}}
