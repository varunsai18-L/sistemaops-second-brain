---
id: xwiki-xwiki:Blog.CategoryRss
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907492000
sync_date: 2026-07-21 11:03:28
tags:
  - xwiki/documentation
  - space/blog
---
# Blog category RSS Feed Generator

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907492000
- **Source:** [Blog category RSS Feed Generator](https://wiki.systemaops.in/bin/view/Blog/xwiki:Blog.CategoryRss)

---

{{include reference="Blog.RssCode"/}}

{{include reference="Blog.CategoriesCode"/}}

{{velocity filter="none"}}
#if("$!{request.xpage}" == 'plain' || "$!{request.xpage}" == 'rdf')
$response.setContentType('application/rss+xml')
{{html clean="false" wiki="false"}}
##
##
##
#macro(getTargetCategory $categoryDoc)
  #set($category = "$!{request.category}")
  #if($category == '')
    #set ($categoryDoc = $doc)
    ## Since 9.15, category data may exist in Blog or Blog.Categories. Code supports both paths to maintain backward compatibility.
    ## This code checks whether a category exists in its original location (e.g., Blog.News).
    ## If the category is not found, it assumes a migration has occurred and automatically sets the category to its new location in the Blog.Categories namespace (e.g., Blog.Categories.News).
    #if (!$services.blog.hasLegacyCategoryAssignments())
      #set ($oldCategoryRef = $categoryDoc.documentReference)
      ## When accessing "Blog/News?xpage=plain&sheet=Blog.CategoryRss" and the Blog.News document is missing, the current doc is Blog.News.WebHome and that needs to be translated into the migrated category Blog.Categories.News.
      #if ($oldCategoryRef.name == 'WebHome')
        #set ($oldCategoryRef = $categoryDoc.documentReference.parent)
      #end
      #set ($newCategoriesSpaceRef = $services.model.createSpaceReference('Categories', $oldCategoryRef.parent))
      #set ($newCategoryRef = $services.model.createDocumentReference($oldCategoryRef.name, $newCategoriesSpaceRef))
      #if ($xwiki.exists($newCategoryRef))
        #set ($categoryDoc = $xwiki.getDocument($newCategoryRef))
      #end
    #end
    #if("$!categoryDoc.getObject($blogCategoryClassname)" != '' || $categoryDoc.getObject('XWiki.DocumentSheetBinding').sheet == 'Blog.CategoriesSheet')
      #set ($category = $categoryDoc.fullName)
    #else
      #set($category = $defaultCategoryParent)
    #end
  #end
  #set ($categoryDoc = $NULL)
  #setVariable ("$categoryDoc" $xwiki.getDocument($category))
#end
#getTargetCategory($categoryDoc)
#set($tempCategoryDoc = $categoryDoc)
#getEntriesForCategory($tempCategoryDoc.fullName $entries $totalEntries)
#set($categoryDoc = $tempCategoryDoc)
#set($entries = $xwiki.wrapDocs($entries))
#displayBlogCategoryRss($categoryDoc $categoryDoc $entries)
{{/html}}
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
