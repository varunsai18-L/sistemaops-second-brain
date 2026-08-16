---
id: xwiki-Blog.CategorySheet
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907587000
sync_date: 2026-08-16 20:02:31
tags:
  - xwiki/documentation
  - space/blog
---
# $doc.getObject('Blog.CategoryClass').get('name')

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907587000
- **Source:** [$doc.getObject('Blog.CategoryClass').get('name')](https://wiki.systemaops.in/bin/view/Blog/Blog.CategorySheet)

---

{{include reference="Blog.CategoriesCode"/}}

{{velocity}}
#set ($discard = $xwiki.ssx.use("Blog.ManageCategories"))
#set ($discard = $xwiki.jsx.use("Blog.ManageCategories"))
#set ($obj = $doc.getObject($blogCategoryClassname))
#if ($obj)
  #if ($tdoc.content.trim() != '')
    {{include reference="" author="target"/}}

  #end
  {{html wiki=true}}
  #displayCategoryPosts($doc $obj)
  {{/html}}
#elseif ($doc.fullName == $blogCategorySheet)
  {{translation key="blog.categories.sheetmessage"/}}
#else
  {{warning}}{{translation key="blog.categories.notcategory"/}}{{/warning}}
#end
{{/velocity}}
