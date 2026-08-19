---
id: xwiki-Blog.BlogRss
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907773000
sync_date: 2026-08-19 20:23:45
tags:
  - xwiki/documentation
  - space/blog
---
# Blog RSS Feed generator

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907773000
- **Source:** [Blog RSS Feed generator](https://wiki.systemaops.in/bin/view/Blog/Blog.BlogRss)

---

{{include reference="Blog.RssCode"/}}

{{velocity filter="none"}}
#if("$!{request.xpage}" == 'plain' || "$!{request.xpage}" == 'rdf')
$response.setContentType('application/rss+xml')
{{html clean="false" wiki="false"}}
##
##
##
#if ("$!doc.getObject($blogClassname)" != '')
  #set ($blogDoc = $doc)
#else
  #getTargetBlog($blogDoc)
#end
#getBlogEntries($blogDoc $entries)
#set($entries = $xwiki.wrapDocs($entries))
#displayBlogRss($blogDoc $entries)
{{/html}}
#end
{{/velocity}}
