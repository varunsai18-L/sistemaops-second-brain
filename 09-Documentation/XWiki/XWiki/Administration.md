---
id: xwiki-XWiki.AdminSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906188000
sync_date: 2026-08-16 19:44:58
tags:
  - xwiki/documentation
  - space/xwiki
---
# Administration

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906188000
- **Source:** [Administration](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminSheet)

---

{{include reference="XWiki.ConfigurableClassMacros" /}}

{{velocity output="false"}}
#if ($request.xaction == 'switchContext')
  $response.sendRedirect($request.target)
  #stop
#end

#set ($adminAction = 'admin')
#set ($crtCategoryId = "$!{request.category}")
#if ($crtCategoryId != '')
  #set ($crtCategoryId = $numbertool.toNumber($crtCategoryId).intValue())
#end
#set ($crtSectionId = "$!{request.section}")

##
## Admin menu map
##
## displayInSection: menu.name | sectionOrder: 200 | page: Menu.MenuConfigurationSection
## displayInSection: panels.applications | sectionOrder: 400 | page: PanelsCode.ApplicationsPanelConfigurable
## displayInSection: panels.navigation | sectionOrder: 500 | page: PanelsCode.NavigationConfigurationSection
#set($adminMenu = [
  {
    'id' : 'lf',
    'icon': 'columns',
    'displayBeforeCategory': 'content',
    'children': [
       {'id' : 'Themes', 'perSpace' : true, 'order' : 100},
       {'id' : 'Panels.PanelWizard', 'perSpace' : true, 'order' : 300},
       {'id' : 'Presentation', 'perSpace' : true, 'order' : 600}
    ]
  },
  {
    'id' : 'usersgroups',
    'icon': 'group',
    'displayBeforeCategory': 'extensionmanager',
    'children': [
       {'id' : 'Users', 'order' : 100},
       {'id' : 'Groups', 'order' : 200},
       {'id' : 'Rights', 'perSpace' : false, 'order' : 300},
       {'id' : 'PageAndChildrenRights', 'perSpace' : true, 'order' : 300, 'global': false},
       {'id' : 'PageRights', 'perSpace' : true, 'order' : 350, 'global': false},
       {'id' : 'UserProfile', 'order' : 400},
       {'id' : 'Registration', 'order' : 500}
    ]
  },
  {
    'id' : 'other',
    'icon': 'wrench',
    'children' : []
  }
])

##
## Fill in the list of custom applications to configure
##
#findCustomSectionsToConfigure($adminMenu)
##
## Filter only the sections that are valid in the context
##
#set ($categoriesToRemove = [])
#foreach ($category in $adminMenu)
  #set ($sectionsToRemove = [])
  #foreach ($section in $category.children)
    #if ($editor == 'spaceadmin' && !$section.perSpace)
      #set ($discard = $sectionsToRemove.add($section))
    #elseif ($editor == 'globaladmin' && "$!section.global" == "false")
      ## For retro-compatibility, all sections are global unless the 'global' field is explicitly marked as false
      #set ($discard = $sectionsToRemove.add($section))
    #end
  #end
  #set ($discard = $category.children.removeAll($sectionsToRemove))
  #if ($category.children.size() == 0)
    #set ($discard = $categoriesToRemove.add($category))
  #end
#end
#set ($discard = $adminMenu.removeAll($categoriesToRemove))
#if ("$!crtCategoryId" != '' && $crtCategoryId >= $adminMenu.size())
  #set ($crtCategoryId = '')
#end

##
## Prepare the Admin menu map for processing
##
#set ($filteredAdminMenu = [])
#set ($crtSection = $NULL)
#set ($crtCategory = $NULL)
#foreach ($category in $adminMenu)
  ## "Standard" URLs and icons for categories
  #set ($category.url = $xwiki.getURL($currentDoc, $adminAction, "category=${mathtool.sub($foreach.count, 1)}"))
  #if ($xwiki.getDocument('XWiki.AdminSheet').getAttachment("${category.id}.png"))
    #set ($category.iconReference = "XWiki.AdminSheet@${category.id}.png")
  #else
    #set ($category.iconReference = "XWiki.ConfigurableClass@DefaultAdminSectionIcon.png")
  #end
  #set ($category.description = $services.localization.render("admin.${category.id}.description").trim())
  #set ($category.cssClass = "${category.id}Icon")
  #set ($category.name = $services.localization.render("admin.${category.id}").trim())
  #if ("$!{crtCategoryId}" != '' && $foreach.count == $mathtool.add($crtCategoryId, 1))
    #set ($crtCategory = $category)
  #end
  ##
  ## Process each admin section
  #set ($filteredCategoryChildren = [])
  #foreach ($section in $category.children)
    #if ($xwiki.exists($section.id) || $xwiki.exists("XWiki.Admin${section.id}Sheet"))
      #if ($crtSectionId == $section.id)
        #set ($crtSection = $section)
        #set ($crtCategory = $category)
      #end
      #set ($section.iconReference = '')
      #if ($section.id.indexOf('.') > 0)
        #set ($sectionDoc = $xwiki.getDocument($section.id))
        #set ($section.name = $sectionDoc.getDisplayTitle())
        #if ($sectionDoc.getAttachment('icon.png'))
          #set ($section.iconReference = "${sectionDoc}@icon.png")
        #else
          #set ($section.iconReference = 'XWiki.ConfigurableClass@DefaultAdminSectionIcon.png')
        #end
      #else
        #set ($sectionDoc = $xwiki.getDocument('XWiki.AdminSheet'))
        #set ($section.name = $services.localization.render("admin.${section.id.toLowerCase()}"))
        #set ($iconName = "${section.id.toLowerCase()}.png")
        #if ($sectionDoc.getAttachment($iconName))
          #set ($section.iconReference = "${sectionDoc}@${iconName}")
        #else
          #set ($section.iconReference = 'XWiki.ConfigurableClass@DefaultAdminSectionIcon.png')
        #end
      #end
      #set ($query = "editor=$escapetool.url(${editor})&section=$escapetool.url(${section.id})")
      #if ($editor != 'globaladmin')
        #set ($query = $query + "&space=$escapetool.url(${currentSpace})")
      #end
      #set ($action = "$!{section.action}")
      #if ($action == '')
        #set ($action = $adminAction)
      #end
      #set ($section.url = $xwiki.getURL($currentDoc, $action, $query))
      #set ($key = "admin.${section.id.toLowerCase()}.description")
      #if ($services.localization.get($key))
        #set ($section.description = $services.localization.render($key))
      #end
      #set ($discard = $filteredCategoryChildren.add($section))
    #elseif ($section.configurable)
      #if ($section.readOnly)
        #set ($section.cssClass = 'readOnly')
      #end
      #if ($crtSectionId == $section.id)
        #set ($crtSection = $section)
        #set ($crtCategory = $category)
      #end
      #set ($discard = $filteredCategoryChildren.add($section))
    #end
  #end
  #set ($category.children = $filteredCategoryChildren)
  #if ($filteredCategoryChildren.size() > 0)
    #set ($discard = $filteredAdminMenu.add($category))
  #end
#end
#set ($adminMenu = $filteredAdminMenu)

## Mark the active category/section. We use this flag when displaying the menu.
#if ($crtCategory)
  #set ($crtCategory.active = true)
  #if ($crtSection)
    #set ($crtSection.active = true)
  #else
    #set ($crtSectionId = $NULL)
  #end
#else
  #set ($crtCategoryId = $NULL)
#end

#**
 * Displays the sections from an administration category
 *
 * Expected format:
 * sections = vector of items
 * item = map with the following fields:
 *        'id'       : mandatory
 *        'name'     : the text displayed for the corresponding menu item;
 *                     optional, defaults to
 *                     $services.localization.render("$!{translationPrefix}${item.id}")
 *        'description' : the description displayed for the corresponding section;
 *                     optional
 *        'link'     : the "action" of the menu item; mandatory
 *        'cssClass' : a specific css class for the menu item for custom
 *                     styling; optional, defaults to ''
 *
 * @param $sections the sections list, in the format described above
 * @param $translationPrefix the translation prefix added to the id of each
 *        item, in order to generate the name and description; ignored when
 *        name or description are specified
 *#
#macro(admin_displayCategory $sections $translationPrefix)
(% class="admin-category" %)
  #set ($sortedSections = [])
  #sortCollectionOfMapsByField($sections, 'order', 9999, 'asc', $sortedSections)
  #foreach ($section in $sortedSections)
    * [[[[image:${section.iconReference}]] **${section.name}**>>path:${section.url}]] (% class="description" %)$!{section.description}
  #end
#end


#**
 * Displays the administration categories
 *
 * Expected format:
 * sections = vector of items
 * item = map with the following fields:
 *        'id'       : mandatory
 *        'name'     : the text displayed for the corresponding menu item;
 *                     optional, defaults to
 *                     $services.localization.render("$!{translationPrefix}${item.id}")
 *        'description' : the description displayed for the corresponding section;
 *                     optional
 *        'link'     : the "action" of the menu item; mandatory
 *        'cssClass' : a specific css class for the menu item for custom
 *                     styling; optional, defaults to ''
 *
 * @param $sections the sections list, in the format described above
 * @param $translationPrefix the translation prefix added to the id of each
 *        item, in order to generate the name and description; ignored when
 *        name or description are specified
 *#
#macro(admin_displayCategories $adminMenu $translationPrefix)
(% class="admin-category" %)
  #foreach ($category in $adminMenu)
    * [[[[image:${category.iconReference}]] **${category.name}**>>path:${category.url}]] (% class="description" %)$!{category.description}
  #end
#end

#macro (verticalNavigation $menu $options)
  {{html clean="false"}}
  <nav id="$!options.id" class="panel-group $!options.cssClass"
    aria-label="$escapetool.xml($services.localization.render('administration.menu.label'))">
    <div class="panel xform">
      <label for="adminsearchmenu" class="hidden">$services.localization.render('search')</label>
      <input type="text" class="form-control panel-group-filter" autocomplete="off" id="adminsearchmenu"
        placeholder="$escapetool.xml($services.localization.render('administration.menu.search.hint'))"
        ## Disable the search input initially until the JavaScript code that handles the search is ready.
        disabled="disabled" />
    </div>
    #foreach ($item in $menu)
      #verticalNavigationItem($item $options)
    #end
    <div class="panel panel-default noitems hidden">
      <div class="panel-heading collapsed">
        $escapetool.xml($services.localization.render('administration.menu.search.noResults'))
      </div>
    </div>
  </nav>
  {{/html}}
#end

#macro (verticalNavigationItem $item $options)
  #set ($escapedId = $escapetool.xml($item.id))
  #set ($name = "$!item.name")
  #if ($name == '')
    #set ($name = $services.localization.render("$!options.translationPrefix$item.id"))
  #end
  #set ($isActive = $item.active == true)
  #set ($hasChildren = $item.children && $item.children.size() > 0)
  #if ($hasChildren)
    #set ($children = [])
    #sortCollectionOfMapsByField($item.children, 'order', 99999, 'asc', $children)
    <div class="panel panel-default">
      <a class="panel-heading#if (!$isActive) collapsed#end" id="panel-heading-$escapedId"
      href="$!item.url" data-toggle="collapse"#if ("$!options.id" != '') data-parent="#$options.id" #end
      data-target="#panel-body-$escapedId" aria-expanded="$isActive" aria-controls="panel-body-$escapedId"
      title="$!escapetool.xml($item.description)">
        <span>$!services.icon.renderHTML($item.icon)$escapetool.xml($name)</span>
        <div>$services.icon.renderHTML('caret-down')</div>
      </a>
      <section class="panel-collapse collapse#if ($isActive) in#end" id="panel-body-$escapedId"
          aria-labelledby="panel-heading-$escapedId">
        <div class="list-group">
          #foreach ($child in $children)
            #verticalNavigationItem($child $options)
          #end
        </div>
      </section>
    </div>
  #else
    <a class="list-group-item#if ($isActive) active#end" data-id="$escapedId"
      href="$!item.url" title="$!escapetool.xml($item.description)"
      >$!services.icon.renderHTML($item.icon)$escapetool.xml($name)</a>
  #end
#end
{{/velocity}}

{{velocity}}
##**************************************************************************************************
## Administration Sheet, used to display a common UI for some wiki features (presentation, users,
## groups, rights etc.) at global / space level and also for several applications.
##**************************************************************************************************
#if($xcontext.action == 'view' && "$!request.viewer" == '')
  $response.sendRedirect($xwiki.getURL($doc.getFullName(), 'admin', $request.getQueryString()))##
#else
  $xwiki.jsx.use('XWiki.AdminSheet')##
  ## Construct the SSX parameter map.
  #set ($parameterMap = {})
  #if ($themeDoc)
    #set ($discard = $parameterMap.put('colorTheme', $themeDocFullName))
  #end
  $xwiki.ssx.use('XWiki.AdminSheet', $parameterMap)##
  #if ("$!crtSectionId" != '' && $crtSectionId.indexOf('.') > 0 && $xwiki.exists($crtSectionId))
    #set ($sectionName = $xwiki.getDocument($crtSectionId).getDisplayTitle())
  #elseif ($crtSectionId != '' && $services.localization.get("admin.${crtSectionId.toLowerCase()}"))
    #set ($sectionName = $services.localization.render("admin.${crtSectionId.toLowerCase()}"))
  #elseif ("$!crtSectionId" != '')
    #set ($sectionName = $crtSectionId)
  #elseif ("$!crtCategoryId" != '')
    #set ($sectionName = $services.localization.render("admin.$crtCategory.id"))
  #elseif ($editor == 'globaladmin')
    #set ($sectionName = $services.wiki.getById($xcontext.database).prettyName)
    #if ("$!sectionName" == '')
      #set ($sectionName = $xcontext.database)
    #end
  #else
    #set ($sectionName = $currentSpace)
  #end

{{html}}
#template('hierarchy.vm')
{{/html}}

## Determine the administration level.
#set ($level = '')
#if ($doc.documentReference.name == 'WebPreferences')
  #set ($level = '.page')
#elseif ($doc.fullName == 'XWiki.XWikiPreferences')
  #if ($xcontext.isMainWiki())
    #set ($level = '.global')
  #else
    #set ($level = '.wiki')
  #end
#end
(% id="document-title" %)(((
  = $services.localization.render("administration.sectionTitle$level", 'xwiki/2.1', [$sectionName]) =
  ## Display the category/section description below the title.
  #set ($categoryOrSectionId = $crtCategory.id)
  #if ("$!crtSection.id" != '')
    #set ($categoryOrSectionId = $crtSection.id)
  #end
  #set ($descriptionTranslationKey = "admin.$!{categoryOrSectionId.toLowerCase()}.description")
  #if ($services.localization.get($descriptionTranslationKey))
    (% class = "noitems" %)(((
      $services.localization.render($descriptionTranslationKey)
    )))
  #end

  ----
)))

  #verticalNavigation($adminMenu {
    'id': 'administration-menu',
    'translationPrefix': 'admin.',
    'cssClass': 'admin-menu'
  })

  ##-----------------------------------------
  ## admin-page display
  ##-----------------------------------------
    #if(!$crtSection && !$crtCategory)
      #admin_displayCategories($adminMenu)
    #elseif (!$crtSection)
      #admin_displayCategory($crtCategory.children)
    #else
      (% id="admin-page-content" %)(((
        ##------------------------------------------------------------------------------------------------------------
        ## The Administration allows editing other pages from different applications inside the admin context (UI)
        ##------------------------------------------------------------------------------------------------------------
        #if ($xwiki.exists("XWiki.Admin${section}Sheet"))
          ## Handle known XWiki administration sections
          {{include reference="XWiki.Admin${section}Sheet" /}}
        #elseif ($xwiki.exists($section))
          {{html clean="false"}}#includeForm($section){{/html}}
        #end
        #if ($crtSection.configurable)

          {{include reference="XWiki.ConfigurableClass" /}}
        #end
      ))) ## admin-page-content
    #end
#end
{{/velocity}}
