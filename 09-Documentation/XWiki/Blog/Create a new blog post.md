---
id: xwiki-Blog.CreatePost
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907782000
sync_date: 2026-08-16 20:02:34
tags:
  - xwiki/documentation
  - space/blog
---
# Create a new blog post

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907782000
- **Source:** [Create a new blog post](https://wiki.systemaops.in/bin/view/Blog/Blog.CreatePost)

---

{{include reference="Blog.BlogCode"/}}

{{velocity}}
## In case this page is called from  the blogPostCreate macro
#if ("$!targetBlogDoc" != '')
  #set ($doc = $targetBlogDoc)
#end
{{html clean="false" wiki="true"}}
#set($name = "$!request.entryTitle.trim()")
#set($title = $name)
#if($name == '')
  ## If there's also a form_token passed it means the user has entered an empty blog post title, let the user know about it!
  #if ("$!request.form_token" != '')
    {{error}}$services.localization.render('blog.post.titleEmptyError'){{/error}}

  #end
  ## First step, display the create form
  #if($hasEdit)
  $xwiki.jsx.use($blogScriptsDocumentName)##
  #set($space = "$!request.entrySpace")
  #if($space == '')
    #set($space = $doc.space)
  #end
  <form action='$doc.getURL()' method="post" class="xformInline newBlogPostForm">
  <div>
    <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
    <input type="hidden" name="entrySpace" value="$!{escapetool.xml($services.rendering.escape($space,$doc.syntax))}"/>
    #if($doc.getObject($blogCategoryClassname))
      <input type="hidden" name="category" value="$services.rendering.escape(${escapetool.xml(${doc.fullName})}, $doc.syntax)"/>
    #end
    $services.icon.renderHTML('add')<label class="createPost" for="entryTitle">$services.localization.render('blog.post.createpost') </label>
    <input type="text" id="entryTitle" name="entryTitle" size="30" placeholder="$services.localization.render('blog.post.title')"/> <span class="buttonwrapper">
    <input type="submit" value="${escapetool.xml($services.localization.render('blog.post.create'))}" class="btn btn-primary button"/></span>
  </div>
  </form>
  #elseif("$!request.entryTitle" != '')## !hasEdit && form submitted
    #template('accessdenied.vm')
  #end## hasEdit
#else
  ## Second step, form submitted, create the document
  #set($space = "$!request.entrySpace")
  #getBlogPostsLocation($space $blogPostsLocation)
  #if($blogPostsLocation == '')
    #set($blogPostsLocation = 'Main')
  #end
  ## Since XWiki 12.0RC1 it is possible to use a naming strategy at wiki level and the blog application should respect it.
  #if("$!services.modelvalidation" != '' && $services.modelvalidation.configuration.useTransformation())
    #set($name = $services.modelvalidation.transformName($name))
  #else
    ## Remove . and : from the document name, as they have a special meaning in XWiki document names
    #set($name = $name.replaceAll('[.:]', ''))
  #end
  #set($blogPostsLocationReference = $services.model.resolveSpace($blogPostsLocation))
  #set($postDocRef = $services.model.createDocumentReference($name, $blogPostsLocationReference))
  ## Make sure blog name is new
  #if($xwiki.exists($postDocRef))
    #set($name = $xwiki.getUniquePageName($blogPostsLocation, $name))
    #set($postDocRef = $services.model.createDocumentReference($name, $blogPostsLocationReference))
  #end
  ## Get the target blog document, to set it as the parent
  #getBlogDocument($space $blogDoc)
  #set($parent = "$!{escapetool.url($blogDoc.fullName)}")
  #set($title = "$!{escapetool.url($title)}")
  #set($category = "")
  #if("$!request.category" != '')
    #set($category = "&${blogPostClassname}_${blogPostObjectNumber}_category=${escapetool.url(${request.category})}")
  #end
  $response.sendRedirect($xwiki.getURL($postDocRef, 'edit', "template=${blogPostTemplate}&parent=${parent}&title=${title}&${blogPostClassname}_0_title=${title}$!{category}&form_token=$!{request.getParameter('form_token')}"))
#end## name == ''
{{/html}}
{{/velocity}}
