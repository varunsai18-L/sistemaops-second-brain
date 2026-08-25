---
id: xwiki-Blog.BlogSheet
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907429000
sync_date: 2026-08-25 21:14:24
tags:
  - xwiki/documentation
  - space/blog
---
# #evaluate($!{doc.getValue('title')})

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907429000
- **Source:** [#evaluate($!{doc.getValue('title')})](https://wiki.systemaops.in/bin/view/Blog/Blog.BlogSheet)

---

{{include reference="Blog.BlogCode"/}}

{{velocity}}
{{html clean="false" wiki="true"}}
##
##
##
#showBlogInfo($doc)
## Keep testing the inline action for backward compatibility with older blog posts.
#if($xcontext.action != 'edit' && $xcontext.action != 'inline')
  #printBlog($doc)
#end
{{/html}}
{{/velocity}}
