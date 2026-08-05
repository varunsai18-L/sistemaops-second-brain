---
id: xwiki-xwiki:XWiki.XWikiUserSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906372000
sync_date: 2026-07-21 11:01:46
tags:
  - xwiki/documentation
  - space/xwiki
---
# Profile of XWikiUserSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906372000
- **Source:** [Profile of XWikiUserSheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.XWikiUserSheet)

---

{{velocity}}
#########################
## CSS & Javascripts
#########################
#set($discard = $xwiki.ssx.use("XWiki.XWikiUserSheet"))
#set($discard = $xwiki.jsx.use("XWiki.XWikiUserSheet"))
#########################
## Setting categories
#########################
#set($categories = [])

## load the user menu from the 'org.xwiki.plaftorm.user.profile.menu' UIXP.
#foreach ($uix in $services.uix.getExtensions('org.xwiki.plaftorm.user.profile.menu', {'sortByParameter': 'priority'}))
  #if(!$uix.parameters.containsKey('isActive') || $uix.parameters.get('isActive') != 'false')
    #if (!$uix.parameters.containsKey('id'))
      ## when no id is explicitly provided, we use the id of the UIX.
      #set ($discard = $uix.parameters.put('id', $uix.id))
    #end
    #if ($uix.parameters.containsKey('icon'))
      #set ($discard = $uix.parameters.put('glyphicon', $uix.parameters.get('icon')))
    #end
    #set ($discard = $uix.parameters.put('uix', $uix))
    #set($discard = $categories.add($uix.parameters))
  #end
#end
#########################
## Current category
#########################
#set($currentCategory = "$!request.category")
#if($currentCategory == "")
  #set($currentCategory = $categories[0].get('id'))
#end
#########################
## Creating vertical menu
#########################
#set($userMenu = [{
  'id'       : 'settings',
  'cssClass' : 'user-menu-title',
  'children' : $categories
  }
])
## Setting automaticaly url & css fields of each category
#foreach($category in $userMenu)
  #foreach($subcategory in $category.get('children'))
    #set($id = $subcategory.get('id')) 
    #set($discard = $subcategory.put('url', "?category=${id}"))
    #set($discard = $subcategory.put('cssClass', "user-menu-$id category-tab"))
  #end
#end
#########################
## Display the left menu
#########################
(% id="user-menu-col" %)
(((
  ############
  ## Avatar
  ############
  (% id="avatar" %)
  (((
    #if($request.xpage == 'edituser')
      {{html clean="false"}}
        #resizedUserAvatar($doc.fullName 180)
      {{/html}}
    #else
      ## By specifying the image width we enable server side resizing. The width value we use is greater than the
      ## available space because we don't want to loose too much of the image quality (we rely on the browser to fit the
      ## image in the available space).
      {{attachmentSelector classname="XWiki.XWikiUsers" object="$obj.number" property="avatar" #if ($hasEdit) savemode="direct" #end defaultValue="XWiki.XWikiUserSheet@noavatar.png" width="180" alternateText="$xwiki.getUserName($doc.fullName, false)" buttontext="$services.localization.render('platform.core.profile.changePhoto')" displayImage="true" filter="png,jpg,jpeg,gif"/}}
    #end
  )))
  ##########
  ## Menu
  ##########
  (% id="user-vertical-menu" %)
  (((
    #verticalNavigation($userMenu, {'translationPrefix' : 'platform.core.profile.category.', 'crtItemId' : $currentCategory, 'cssClass' : 'profile-menu'})
  )))
)))
#########################
## Display the page content
#########################
(% id="user-page-content" %)
(((
  #foreach($category in $userMenu)
    #foreach($subcategory in $category.get('children'))
      #set($tabKey = $subcategory.get('id')) 
      (% id="${tabKey}Pane" class="user-page-pane#if($tabKey != $currentCategory) hidden#end" %)
      (((
        {{html}}$services.rendering.render($subcategory.uix.execute(), 'html/5.0'){{/html}}
      )))
    #end
  #end
)))
#########################
## END
#########################
{{html clean="false"}}
  #if($xcontext.action == 'edit' || $xcontext.action == 'inline')
    <input type='hidden' name='category' value="$!{escapetool.xml($currentCategory)}" />
  #end
  <div class="clearfloats">&nbsp;</div>
{{/html}}
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
