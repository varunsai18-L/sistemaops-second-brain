---
id: xwiki-Blog.Migration
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907415000
sync_date: 2026-08-19 20:23:36
tags:
  - xwiki/documentation
  - space/blog
---
# Blog migration

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907415000
- **Source:** [Blog migration](https://wiki.systemaops.in/bin/view/Blog/Blog.Migration)

---

{{velocity filter="none"}}
#if($request.migrate && $!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
  #set($newContent = '#includeForm("Blog.BlogPostSheet")')
  #set($query = ", BaseObject obj where obj.name = doc.fullName and obj.className = 'XWiki.ArticleClass'")
  #foreach($article in $services.query.hql($query).execute())
    #if($xwiki.hasAccessLevel('edit', $xcontext.user, $article))
      #set($articleDoc = $xwiki.getDocument($article))
    #set($articleObj = $articleDoc.getObject('XWiki.ArticleClass'))
      #set($entryObj = $articleDoc.newObject('Blog.BlogPostClass'))
      #foreach($property in ['title', 'content', 'extract', 'category'])
        $!entryObj.set($property, $articleObj.getProperty($property).value)
      #end
      $!entryObj.set('published', 1)
      $!entryObj.set('publishDate', $articleDoc.creationDate)
      $!entryObj.set('hidden', 0)
      #set($discard = $articleDoc.removeObjects('XWiki.ArticleClass'))
      $articleDoc.setContent($newContent)
      $!articleDoc.save($services.localization.render('blog.migration.migrated'), true)
      * $services.localization.render('blog.migration.updated') [[$entryObj.title>>${article}]] ($services.localization.render('blog.migration.inspace') [[$articleDoc.space>>${articleDoc.space}.WebHome]])
    #else
      * $services.localization.render('blog.migration.skipping') [[$article]]
    #end
  #end
  $services.localization.render('blog.migration.done') [[$services.localization.render('blog.migration.backtoblog')>>Blog.WebHome]]
#else
$services.localization.render('blog.migration.pleaseconfirm')

{{html clean="false" wiki="true"}}
  <form action="$doc.getURL()" method="post">
    <div>
    <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
    <input type="submit" name="migrate" value="$services.localization.render('blog.migration.confirm')"/>
    </div>
  </form>
{{/html}}

[[$services.localization.render('blog.migration.backtoblog')>>Blog.WebHome]]
#end
{{/velocity}}
