---
id: xwiki-Blog.CategoriesSheet
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907493000
sync_date: 2026-08-25 21:14:19
tags:
  - xwiki/documentation
  - space/blog
---
# All categories

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907493000
- **Source:** [All categories](https://wiki.systemaops.in/bin/view/Blog/Blog.CategoriesSheet)

---

{{include reference="Blog.CategoriesCode"/}}

{{velocity filter="none"}}
#if ($doc.fullName == $blogCategoriesSheet)
  {{translation key="blog.categories.webhome_sheetmessage"/}}
#else
{{html clean="false" wiki="true"}}
#if ("$!request.action" == 'manage')
  $xwiki.ssx.use('Blog.ManageCategories')
  $xwiki.jsx.use('Blog.ManageCategories', {'minify':false})

  #set ($categoriesLocation = $doc.space)
  #set ($defaultCategoryParent = $doc.fullName)
  #displayCategoryManagementTree($categoriesLocation 'editable')
#else
  #set ($discard = $xwiki.ssx.use("Blog.ManageCategories"))
  #set ($discard = $xwiki.jsx.use("Blog.ManageCategories"))
  #displayCategoryPosts($doc $NULL)
#end
{{/html}}
#end
{{/velocity}}

