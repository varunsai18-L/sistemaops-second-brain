---
id: xwiki-Blog.BlogPostsMigration
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907541000
sync_date: 2026-08-16 20:02:35
tags:
  - xwiki/documentation
  - space/blog
---
# Blog posts migration

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907541000
- **Source:** [Blog posts migration](https://wiki.systemaops.in/bin/view/Blog/Blog.BlogPostsMigration)

---

{{info}}In order to not break the actual blog use cases and to be able to aggregate posts of blogs using the same categories location we need to set the category property of the old blog posts to a default value when the post category is not set by the user.{{/info}}

{{velocity}}
#if ($hasAdmin)
#set ($excludedPostsQuery = "select doc1.fullName from XWikiDocument doc1, BaseObject as obj1, DBStringListProperty as category left join category.list catList 
where doc1.fullName <> 'Blog.BlogPostTemplate' and
obj1.name=doc1.fullName and obj1.className='Blog.BlogPostClass' and obj1.id=category.id.id and category.id.name='category' and catList Like '%.%'")

#set ($query = ", BaseObject as obj where doc.fullName <> 'Blog.BlogPostTemplate' and
obj.name=doc.fullName and obj.className='Blog.BlogPostClass' and doc.fullName not in ($excludedPostsQuery)")
#set ($results = $services.query.hql($query).execute())

#if ("$!request.confirm" == 'true')
  #set ($logger = $services.logging.getLogger("org.xwiki.contrib.blog.${doc.fullName}"))
  #set ($discard = $logger.info('Migration started...'))
  #set ($migrated = false)
   == Migrated blog posts ==
  #foreach($post in $results)
    #set($postDoc = $xwiki.getDocument($post))
    #set($postObj = $postDoc.getObject('Blog.BlogPostClass'))
    #if ("$!postObj.category" == '')
      #set($discard = $postObj.set('category', 'Blog.Categories.WebHome'))
      #set($discard = $postDoc.save('Save post after initializing it category by the default category', true))
      #set ($discard = $logger.info('  Migration of the blog post [{}]', $post))
      #set ($migrated = true)
      * [[$post>>$post]] (/)
    #end
  #end
  #if (!$migrated)
  {{warning}}There is no blog posts to migrate{{/warning}}
  #end
  #set ($discard = $logger.info('Migration complete.'))
#else
  #if($results.size() > 0)
    == Blog posts to migrate ($results.size()): ==
    #foreach($post in $results)
     * [[$post>>$post]]
    #end
  #else
    {{warning}}There is no blog posts to migrate{{/warning}}
  #end
#end

#if ("$!request.confirm" != 'true' && $results.size() > 0)
  {{html}}<a href="$doc.getURL('view', 'confirm=true')" class='button'>Start</a>{{/html}}
#end
#else
{{error}}You are not allowed to execute the blog posts migration{{/error}}
#end
{{/velocity}}

