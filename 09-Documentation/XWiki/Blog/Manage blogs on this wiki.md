---
id: xwiki-Blog.Management
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907664000
sync_date: 2026-08-16 20:02:37
tags:
  - xwiki/documentation
  - space/blog
---
# Manage blogs on this wiki

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907664000
- **Source:** [Manage blogs on this wiki](https://wiki.systemaops.in/bin/view/Blog/Blog.Management)

---

{{include reference="Blog.BlogCode"/}}

{{template name="locationPicker_macros.vm" /}}

{{velocity}}
#if($hasAdmin)
##
##
## List existing blogs.
## TODO: Display the number of articles in each blog
## TODO: Provide some management links: delete, edit title, configure...
##
#set ($discard = $xwiki.jsx.use('Blog.Management'))
== $services.localization.render('blog.manage.existing') ==

{{blogs/}}
##
##
## New blog
##

== $services.localization.render('blog.manage.createnew') ==

#if ("$!request.createBlog" != '')
  #set($title = "$!request.blogTitle")
  #if($title != '')
    #set($blogParentPage = "$!request.blogParent")
    #set($blogPageName = "$!request.blogName")

    #if($blogPageName == '')
      {{warning}}$services.localization.render('blog.manage.nopage'){{/warning}}

    #else
      #set($blogDocName = "${blogPageName}")
      #if ("$!blogParentPage" != '')
        #set($blogDocName = "${blogParentPage}.${blogDocName}")
      #end
      #if ($xwiki.exists("${blogDocName}.WebHome"))
        {{warning}}$services.localization.render('blog.manage.unallowed_page'){{/warning}}

      #else
        #if (!$services.csrf.isTokenValid("$!request.form_token"))
          {{error}}$services.localization.render('platform.wiki.csrf.error'){{/error}}

        #else
          ## Create the Blog
          #set ($blogDoc = $xwiki.getDocument("${blogDocName}.WebHome"))
          #set ($blogObj = $blogDoc.getObject('Blog.BlogClass', true))
          #set ($discard = $blogObj.set('title', $title))
          #set ($discard = $blogObj.set('displayType', 'paginated'))
          #set ($discard = $blogObj.set('itemsPerPage', 10))
          #set ($categoriesLocation = "${blogDocName}.Categories")
          #set ($postsLocation = "${blogDocName}")
          #set ($discard = $blogObj.set('categoriesLocation', $categoriesLocation))
          #set ($discard = $blogObj.set('postsLocation', $postsLocation))
          #if ("$!request.postsLayout" != '')
            #set ($discard = $blogObj.set('postsLayout', $request.postsLayout))
          #end
          #set ($discard = $blogDoc.save())

          ## Create the categories page
          #set ($categoriesDoc = $xwiki.getDocument("${categoriesLocation}.WebHome"))
          #set ($sheetBindingObj = $categoriesDoc.getObject('XWiki.DocumentSheetBinding', true))
          #set ($discard = $sheetBindingObj.set('sheet', 'Blog.CategoriesSheet'))
          #set ($discard = $categoriesDoc.save())

          ## Create the Default categories
          #if ("$!request.createDefaultCategories" != '')
            #foreach($categoryName in ['News', 'Other', 'Personal'])
              #set ($discard = $xwiki.copyDocument("Blog.${categoryName}", "${categoriesLocation}.${categoryName}"))
              #set ($categoryDoc = $xwiki.getDocument("${categoriesLocation}.${categoryName}"))
              #set ($discard = $categoryDoc.setParent("${categoriesLocation}.WebHome"))
              #set ($discard = $categoryDoc.save())
            #end
          #end

          ## Create the WebPreferences page
          #if ("$!request.enablePanels" != '')
            #set ($webPreferencesName = "${blogDocName}.WebPreferences")
            #set ($webPreferencesDoc = $xwiki.getDocument($webPreferencesName))
            #set ($discard = $webPreferencesDoc.setHidden(true))
            #set ($xwikiPreferencesObj = $webPreferencesDoc.getObject('XWiki.XWikiPreferences', true))
            #set ($discard = $xwikiPreferencesObj.set('showRightPanels', 1))
            #set ($discard = $xwikiPreferencesObj.set('rightPanels', 'Blog.RecentPostsPanel,Blog.UnpublishedPanel,Blog.CategoriesPanel,Blog.ArchivePanel,Blog.RelatedBlogsPanel,Blog.AllBlogsPanel'))
            #set ($discard = $webPreferencesDoc.save())
          #end

          $response.sendRedirect($blogDoc.getURL())
        #end
      #end
    #end
  #else
    {{warning}}$services.localization.render('blog.manage.notitle'){{/warning}}

  #end
#end
##
## Show the form
{{html clean="false" wiki="true"}}
<form action="${xwiki.getURL('Blog.Management')}" id="newBlog" method="post" class="xform">
#locationPicker({
    'id': 'blogLocation',
    'title': {
      'label': 'blog.manage.location.title',
      'hint': 'blog.manage.location.title.hint',
      'name': 'blogTitle',
      'value': '',
      'placeholder': 'blog.manage.location.title.placeholder'
    },
    'preview': {
      'label': 'core.create.locationPreview.label',
      'hint': 'blog.manage.locationPreview.hint'
    },
    'parent': {
      'label': 'core.create.spaceReference.label',
      'hint': 'core.create.spaceReference.hint',
      'name': 'blogParent',
      'reference': $doc.documentReference.parent.parent,
      'placeholder': 'core.create.spaceReference.placeholder'
    },
    'name': {
      'label': 'core.create.name.label',
      'hint': 'core.create.name.hint',
      'name': 'blogName',
      'value': '',
      'placeholder': 'core.create.name.placeholder'
    }
  })
<div>
  <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
  <input type="hidden" name="createBlog" value="1"/>
  <dl>
    <dt>
      <label for="blogSpace">$services.localization.render('blog.manage.categories_location')</label>
      <span class="xHint">$services.localization.render('blog.manage.categoriesLocationPreview.hint')</span>
    </dt>
    <dd><div id="catLocation">
      <div class="breadcrumb-container">
        <ol id="blogCategoriesLocation" class="breadcrumb"></ol>
      </div>
    </dd>
  </dl>
  <dl>
    <dt><label for="blogSpace">$services.localization.render('blog.manage.enable_panels')</label>
      <input type="checkbox" name="enablePanels" value="1" checked="checked" />
    </dt>
  </dl>
  <dl>
    <dt><label for="blogSpace">$services.localization.render('blog.manage.create_default_categories')</label>
      <input type="checkbox" name="createDefaultCategories" value="1" checked="checked" />
    </dt>
  </dl>
  <dl>
    <dt><label for="blogSpace">$services.localization.render('blog.manage.post.layout')</label>
      #set ( $class = $xwiki.getClass("Blog.BlogClass"))
      #set ($postLayouts = $class.get('postsLayout').getMapValues())
      #set ($postLayoutsList = $class.get('postsLayout').getListValues())
      #set ($firstLayout = '')
      #if ($postLayoutsList.size() > 0)
        #set ($firstLayout = $postLayoutsList[0])
      #end
      <select name="postsLayout">
        #foreach ($item in $postLayouts.entrySet())
        #set ($translation = $services.localization.get("Blog.BlogClass_postsLayout.${item.key}"))
        <option value="${escapetool.xml($item.key)}" #if("$!item.key" == $firstLayout)selected="selected"#end >
          #if ("$!translation" != '')
            $!services.localization.render("Blog.BlogClass_postsLayout.${item.key}")
          #else
            $!item.value.value
          #end
        </option>
        #end
      </select>
    </dt>
  </dl>
  <input class="button" type="submit" value="${escapetool.xml($services.localization.render('blog.manage.create'))}"/>
</div>
</form>
{{/html}}
#else
  {{html}}
  #xwikimessageboxstart($services.localization.render('error') $services.localization.render('notallowed'))
  #xwikimessageboxend()
  {{/html}}
#end
{{/velocity}}
