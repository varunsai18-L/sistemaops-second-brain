---
id: xwiki-xwiki:WikiManager.AdminWikiDescriptorSheet
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906219000
sync_date: 2026-07-21 11:01:26
tags:
  - xwiki/documentation
  - space/wikimanager
---
# AdminWikiDescriptorSheet

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906219000
- **Source:** [AdminWikiDescriptorSheet](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.AdminWikiDescriptorSheet)

---

{{velocity}}
#if ($hasGlobalAdmin)
  #set ($descriptor = $services.wiki.currentWikiDescriptor)
  #set ($sheetDocName = 'AdminWikiDescriptorSheet')
  #set ($sheetDocFullName = "WikiManager.${sheetDocName}")
  ##
  #if ($request.ajax == 'true' && $xcontext.action == 'get')
    ##
    ## Handle AJAX requests.
    ##
    #set ($prettyName  = "$!request.prettyName")
    #set ($description = "$!request.description")
    #set ($owner       = "$!request.owner")
    #set ($homepage    = "$!request.homepage")
    #if ("$!homepage" != '' && $services.csrf.isTokenValid("$!{request.form_token}"))
      #if ("$!owner" != '')
        ## There is a security check in $services.wiki.saveDescriptor() to avoid an admin who is not the current owner
        ## to take the ownership of the wiki.
        ## So we can fill the descriptor safely.
        #set ($discard = $descriptor.setOwnerId($owner))
      #end
      #set ($discard = $descriptor.setPrettyName($prettyName))
      #set ($discard = $descriptor.setDescription($description))
      #set ($homepageReference = $services.model.resolveDocument($homepage))
      #set ($discard = $descriptor.setMainPageReference($homepageReference))
      ##
      #set ($discard = $services.wiki.saveDescriptor($descriptor))
      #if ($services.wiki.lastError)
        $response.setStatus(500)
        #set ($responseText = $!{services.wiki.lastError.message})
        #if ("$!responseText" == '')
          #set ($responseText = $!{services.wiki.lastError.class})
        #end
        $responseText
      #end
    #else
      $response.setStatus(400)
      #if (!$services.csrf.isTokenValid("$!{request.form_token}"))
        $services.localization.render('platform.wiki.admin.wiki.csrfInvalidError')
      #else
        $services.localization.render('platform.wiki.admin.wiki.requiredFieldsError')
      #end
    #end
  #else
    ##
    ## Display the UI.
    ##
    #set ($discard = $xwiki.jsfx.use('js/xwiki/actionbuttons/actionButtons.js', true))
    ## In case of conflict issue we want to display the diff properly
    #set ($discard = $xwiki.ssfx.use('uicomponents/viewers/diff.css', true))
    #set ($discard = $xwiki.jsfx.use('uicomponents/viewers/diff.js'))
    #if ($doc.documentReference.name != $sheetDocName)
      #set ($discard = $xwiki.jsx.use($sheetDocFullName))
      #set ($discard = $xwiki.ssx.use($sheetDocFullName))
    #end
    {{html}}
    <div class='xform'>
      <form method='post' action="$xwiki.getURL($sheetDocFullName, 'get', 'outputSyntax=plain')">
        <fieldset>
          <dl>
            <dt>
              <label for='prettyName'>$services.localization.render('platform.wiki.sheet.prop.wikiprettyname')</label>
              <span class='xHint'>$services.localization.render('platform.wiki.sheet.desc.wikiprettyname')</span>
            </dt>
            <dd>
              <input id='prettyName' name='prettyName' type='text' size='30' value="$!{escapetool.xml($descriptor.prettyName)}" />
            </dd>

            <dt>
              <label for='description'>$services.localization.render('platform.wiki.sheet.prop.description')</label>
              <span class='xHint'>$services.localization.render('platform.wiki.sheet.desc.description')</span>
            </dt>
            <dd>
              <textarea id='description' name='description'>$!{escapetool.xml($descriptor.description)}</textarea>
            </dd>

            <dt>
              <label for='homepage'>
                $services.localization.render('platform.wiki.sheet.prop.homepage') <span class="xRequired">$services.localization.render('core.validation.required')</span>
              </label>
              <span class='xHint'>$services.localization.render('platform.wiki.sheet.desc.homepage')</span>
            </dt>
            <dd>
              #if ($descriptor.mainPageReference)
                #set ($homepage = $services.model.serialize($descriptor.mainPageReference, 'local'))
              #else
                #set ($homepage = '')
              #end
              #set ($pagePickerParams = {
                'id': 'homepage',
                'name': 'homepage',
                'value': $homepage
              })
              #pagePicker($pagePickerParams)
            </dd>

            ## Only show the owner change form element if the current user is the current owner or a global admin (has edit on the wiki's descriptor document).
            #set ($currentUserString   = $services.model.serialize($xcontext.userReference, 'default'))
            #set ($descriptorReference = $services.model.createDocumentReference($services.wiki.mainWikiId, 'XWiki', "XWikiServer${stringtool.capitalize($descriptor.id)}"))
            #set ($descriptorFullName  = $services.model.serialize($descriptorReference))
            #set ($hasEditOnDescriptor = $xwiki.hasAccessLevel('edit', $currentUserString, $descriptorFullName))
            #if ($currentUserString == "$!{services.wiki.currentWikiDescriptor.ownerId}" || $hasEditOnDescriptor)
              <dt>
                <label for='owner'>
                  $services.localization.render('platform.wiki.sheet.prop.owner') <span class="xRequired">$services.localization.render('core.validation.required')</span>
                </label>
                <span class='xHint'>$services.localization.render('platform.wiki.sheet.desc.owner')</span>
              </dt>
              <dd>
                #set ($userPickerParams = {
                  'id': 'owner',
                  'name': 'owner',
                  'value': $descriptor.ownerId
                })
                #userPicker(false $userPickerParams)
              </dd>

              <dd class='warning'>
                <label for='owner'>
                  <span class='xErrorMsg'>$services.localization.render('platform.wiki.admin.wiki.ownerWarning')</span>
                </label>
              </dd>
            #end

          </dl>
        </fieldset>

        <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />

        <span class="buttonwrapper">
          <input name='action_saveandcontinue' type='submit' class='button' value="$services.localization.render('admin.save')" />
        </span>
      </form>
    </div>
    {{/html}}
  #end
#else
  {{html}}
    #xwikimessageboxstart($services.localization.render('error') $services.localization.render('notallowed'))
    #xwikimessageboxend()
  {{/html}}
#end
{{/velocity}}


---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
