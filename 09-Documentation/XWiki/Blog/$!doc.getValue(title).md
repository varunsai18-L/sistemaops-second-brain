---
id: xwiki-Blog.BlogPostSheet
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907580000
sync_date: 2026-08-25 21:14:29
tags:
  - xwiki/documentation
  - space/blog
---
# $!doc.getValue("title")

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907580000
- **Source:** [$!doc.getValue("title")](https://wiki.systemaops.in/bin/view/Blog/Blog.BlogPostSheet)

---

{{include reference="Blog.BlogCode"/}}

{{include reference="Blog.CategoriesCode"/}}

{{velocity}}
$xwiki.jsx.use('Blog.ManageCategories', {'mode' : 'select'})##
$xwiki.ssx.use('Blog.ManageCategories')##
#getEntryObject($doc $entryObj)
#if("$!entryObj" == '')
  {{warning}}{{translation key='blog.sheet.notpost'/}}{{/warning}}
## Keep testing the inline action for backward compatibility with older blog posts.
#elseif($xcontext.action != 'edit' && $xcontext.action != 'inline')
  ## View mode
  #getBlogDocument ($doc.space $blogDoc)
  #getBlogPostsLayout($blogDoc $postsLayout)
  #set ($layoutParams="useSummary=false|displayTitle=false")
  #if ($postsLayout != 'full')
    #set ($layoutParams="$!{layoutParams}|displayCalendar=false")
  #end
  {{blogPostLayoutFull reference="$doc.fullName.replaceAll('~', '~~').replaceAll('"', '~"')"  params="$!layoutParams.replaceAll('~', '~~').replaceAll('"', '~"')" /}}
#else
  #if ("$!request.title" != '')
    ## Use the page title specified on the request, if available, as blog post title. This is needed for instance when
    ## we create the blog post using the Create Page wizard with the blog post template provider (the user is specifying
    ## the page title).
    #set ($discard = $entryObj.set('title', $request.title))
  #end
  #getBlogCategoriesLocation($doc.space $categoriesLocation)
  #set ($defaultPostCategory = "${categoriesLocation}.WebHome")
  ## Since 9.15, category data may exist in Blog or Blog.Categories. Code supports both paths to maintain backward compatibility.
  #if ($categoriesLocation == 'Blog')
    #set ($defaultPostCategory = 'Blog.Categories')
  #end
  #set($discard = $xwiki.jsx.use('Blog.BlogPostSheet'))
  #set($discard = $xwiki.ssx.use('Blog.BlogPostSheet'))
  (% class="xform" %)(((
  {{html clean="false" wiki="true"}}
  ; <label>{{translation key='blog.sheet.title'/}}</label>
  : $doc.display('title', 'edit', $entryObj)
  ; <label>{{translation key='blog.sheet.content'/}}</label>
  : $doc.display('content', 'edit', $entryObj)
  ; <label>{{translation key='blog.sheet.summary'/}}</label>
  : $doc.display('extract', 'edit', $entryObj)

  <div class="row">
    <div class="col-xs-12 col-sm-4 col-lg-3">
      <dl>
        <dt>
          #set ($layoutTranslations = [
            $services.localization.render('Blog.BlogClass_postsLayout_image'),
            $services.localization.render('Blog.BlogClass_postsLayout_cards'),
            $services.localization.render('Blog.BlogClass_postsLayout_compact')
          ])
          <label>$services.localization.render('blog.sheet.image') <a href="javascript:;" title="${escapetool.xml($services.localization.render('blog.sheet.image.info', $layoutTranslations))}"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span></a> :</label>
        </dt>
        <dd>
{{/html}}

{{attachmentSelector classname="Blog.BlogPostClass" property="image" filter="png,jpeg,jpg,gif" displayImage="true" buttontext="$services.localization.render('blog.sheet.choose_image')" width="300" cssClass="blogImageSelector"/}}

{{html clean="false" wiki="true"}}
        </dd>
      </dl>
    </div>
    <div class="col-xs-12 col-sm-8 col-lg-9">
      <dl>
        <dt><label>{{translation key='blog.sheet.category'/}}</label></dt>
        <dd>
          #displayCategoryManagementTree($categoriesLocation 'selectable') <input type="hidden" name="Blog.BlogPostClass_0_category" id="defaultPostCategory"/><input type="hidden" id="blogCategoriesWebHome" value="${escapetool.xml($defaultPostCategory)}"/>
          #if ($blogDoc.getValue('forceCategorySelection') == 1)
            #checkCategorySelectionModal
          #end
        </dd>
      </dl>
    </div>
  </div>
  {{/html}}
)))
  #if ($doc.isNew())
    ## We're creating a new blog post. We handle this case differently because #isPublished returns true when the
    ## property is not set (object missing) and thus the new blog post will appear as published. See also the comment
    ## from the else branch below.
    #set ($isPublished = false)
  #else
    ## We're editing an existing blog post. We need to check the original document because the current one can have
    ## unsaved changes, which happens for instance after returning from preview.
    #set ($originalDocument = $xwiki.getDocument($doc.documentReference))
    #getEntryObject($originalDocument $originalEntryObj)
    #isPublished($originalEntryObj $isPublished)
  #end
  #if($isPublished)
    #if($hasEdit)
      #set($hideArticle = ${doc.display('hidden', 'edit', $entryObj)})
      (% class="post-state-blk plainmessage" %)(((
      (% class="publish-message" %)((($services.icon.render('world') $services.localization.render('blog.sheet.publicationdate', [${doc.display('publishDate', 'view', $entryObj)}]))))
      (% class="hide-message" %)((($services.icon.render('unlock') $services.localization.render('blog.sheet.hidearticle', [${hideArticle}]))))
      )))
    #end
  #else
    #set($defaultDate = $xwiki.getDocument($blogPostTemplate).getObject($blogPostClassname).getProperty('publishDate').value.time)
    #if($entryObj.getProperty('publishDate').value.time == $defaultDate)
      ## The publish date was not set, force it to be the creation date
      $entryObj.set('publishDate', $doc.creationDate)
    #end
    {{html clean="false" wiki="true"}}
    #publishMessageBox("$services.localization.render('blog.sheet.notpublished') <label>**$services.localization.render('blog.sheet.publish') ${doc.display('published', 'edit', $entryObj)}**</label>\\<label>$services.localization.render('blog.sheet.setdate') ${doc.display('publishDate', 'edit', $entryObj)}</label>")
    {{/html}}
  #end
#end
{{/velocity}}
