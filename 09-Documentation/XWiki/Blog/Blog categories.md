---
id: xwiki-xwiki:Blog.Categories
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907577000
sync_date: 2026-07-21 11:03:44
tags:
  - xwiki/documentation
  - space/blog
---
# Blog categories

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907577000
- **Source:** [Blog categories](https://wiki.systemaops.in/bin/view/Blog/xwiki:Blog.Categories)

---

{{include reference="Blog.CategoriesCode"/}}

{{velocity filter="none"}}
{{html clean="false" wiki="true"}}
$xwiki.ssx.use('Blog.ManageCategories')##
$xwiki.jsx.use('Blog.ManageCategories')##

<div class="blog-categories-list">
#getCategoriesHierarchy($doc.space $tree)
#displayCategoriesHierarchyRecursive($tree $doc.fullName 1 'editable')
#if($xwiki.hasAccessLevel('edit', $xcontext.user, $doc.fullName))
* (% class="blog-add-category-label"%)$services.icon.renderHTML('add')
[[$services.localization.render('blog.categories.addcategory')>>Blog.ManageCategories||queryString="xaction=showAddCategory&parentCategory=${escapetool.url(${doc.fullName})}"]](%%)(%%)
##
#if("$!{request.xaction}" == 'showAddCategory' && "$!{request.parentCategory}" == ${doc.fullName}) #addCategoryForm() #end
##
#end

</div>
<div class="clearfloats"></div>
{{/html}}
{{/velocity}}
