---
id: xwiki-XWiki.AdminUserProfileSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906328000
sync_date: 2026-08-19 20:22:44
tags:
  - xwiki/documentation
  - space/xwiki
---
# User Profile

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906328000
- **Source:** [User Profile](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminUserProfileSheet)

---

{{velocity}}
#set ($discard = $xwiki.ssx.use('XWiki.XWikiUserSheet'))
#set ($discard = $xwiki.ssx.use('XWiki.AdminUserProfileSheet'))
##
#set ($sheetDocumentReference = $services.model.createDocumentReference($xcontext.database, 'XWiki', 'AdminUserProfileSheet'))
#set ($sheetDocument = $xwiki.getDocument($sheetDocumentReference))
##
#set ($sectionsObjectClassName = 'XWiki.UserProfileSectionsClass')
#set ($sectionObjectClassName = 'XWiki.UserProfileSectionClass')
##
#set ($xredirect = $doc.getURL($xcontext.action, ${request.queryString}))
#set ($formToken = $services.csrf.getToken())
##
{{html clean='false' wiki='true'}}
  <form action="$sheetDocument.getURL('save')" method='post'>
  ## When in edit mode, the form above gets overriden so we need a div with class xform to cover all cases.
  <div class='xform'>
    #set ($sectionsObject = $sheetDocument.getObject($sectionsObjectClassName))
    <h2>$services.localization.render('platform.user.profileConfigureSectionsTitle')</h2>
    <dl>
      <dt>
        <label for="${sectionsObjectClassName}_${sectionsObject.number}_sections">$services.localization.render('platform.user.profileConfigureSectionsLabel')</label>
        <span class='xHint'>$services.localization.render('platform.user.profileConfigureSectionsHint')</span>
      </dt>
      <dd>$sheetDocument.display('sections', 'edit', $sectionsObject)</dd>
    </dl>
    <h2>$services.localization.render('platform.user.profileConfigureSectionsAllTitle')</h2>
    <dl>
      <dt>
        <a class='hasIcon icon-button add-button' href="$sheetDocument.getURL('objectadd', "classname=${sectionObjectClassName}&amp;xredirect=$escapetool.url(${xredirect})&amp;form_token=${formToken}")">$services.localization.render('platform.user.profileConfigureSectionAddButtonLabel')</a>
      </dt>
    #set ($sectionObjects = $sheetDocument.getObjects($sectionObjectClassName))
    #foreach ($sectionObject in $sectionObjects)
      <dt>
        <a class='hasIcon icon-button remove-button' href="$sheetDocument.getURL('objectremove', "classname=${sectionObjectClassName}&amp;classid=${sectionObject.number}&amp;xredirect=$escapetool.url(${xredirect})&amp;form_token=${formToken}")">$services.localization.render('platform.user.profileConfigureSectionRemoveButtonLabel')</a>
        <label for="${sectionObjectClassName}_${sectionObject.number}_id">$services.localization.render('platform.user.profileConfigureSectionIdLabel')</label>
        <span class='xHint'>$services.localization.render('platform.user.profileConfigureSectionIdHint')</span>
      </dt>
      <dd>$sheetDocument.display('id', 'edit', $sectionObject)</dd>

      <dt>
        <label for="${sectionObjectClassName}_${sectionObject.number}_name">$services.localization.render('platform.user.profileConfigureSectionNameLabel')</label>
        <span class='xHint'>$services.localization.render('platform.user.profileConfigureSectionNameHint', ['http://platform.xwiki.org/xwiki/bin/view/DevGuide/InternationalizingApplications'])</span>
      </dt>
      <dd>$sheetDocument.display('name', 'edit', $sectionObject)</dd>

      <dt>
        <label for="${sectionObjectClassName}_${sectionObject.number}_properties">$services.localization.render('platform.user.profileConfigureSectionPropertiesLabel')</label>
        <span class='xHint'>$services.localization.render('platform.user.profileConfigureSectionPropertiesHint', ['XWiki.XWikiUsers'])</span>
      </dt>
      <dd>$sheetDocument.display('properties', 'edit', $sectionObject)</dd>
    #end
    </dl>
    ## Avoid duplicating the save button for edit mode.
    #if ($xcontext.action != 'edit' && $xcontext.action != 'inline')
      <span class='buttonwrapper'>
        <input class='button' type='submit' name='save' value="$services.localization.render('platform.user.profileConfigureSaveButtonLabel')"/>
      </span>
      <input type='hidden' name='xredirect' value="$xredirect" />
      <input type='hidden' name='form_token' value="$formToken" />
    #end
  </div>
  </form>
{{/html}}
{{/velocity}}
