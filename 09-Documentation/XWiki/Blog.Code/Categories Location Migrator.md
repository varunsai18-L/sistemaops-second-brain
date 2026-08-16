---
id: xwiki-Blog.Code.CategoriesLocationMigrator
type: XWiki Page
space: "Blog.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907600000
sync_date: 2026-08-16 19:46:06
tags:
  - xwiki/documentation
  - space/blog.code
---
# Categories Location Migrator

- **Space:** Blog.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907600000
- **Source:** [Categories Location Migrator](https://wiki.systemaops.in/bin/view/Blog.Code/Blog.Code.CategoriesLocationMigrator)

---

{{job id="{{velocity}}$!request.jobId{{/velocity}}" start="{{velocity}}$!request.confirm{{/velocity}}"}}
{{groovy}}
  services.blog.migrateCategoryLocation(services.wiki.currentWikiId)
{{/groovy}}
{{/job}}

{{velocity}}
#if ($hasAdmin && $services.blog.hasLegacyCategoryAssignments())
  #if ("$!request.jobId" == '')
    #set ($jobId = "$datetool.get('yyyy-MM-dd')/$datetool.get('HH-mm-ss-SSS')")
    #set ($categoryStatement = "from doc.object(Blog.CategoryClass) as category where doc.space = 'Blog' and doc.name <> 'CategoryTemplate'")
    #set ($categories = $services.query.xwql($categoryStatement).execute())
    #set ($categoriesSize = $categories.size())
    #if ($categoriesSize > 0)
      $services.localization.render('blog.migration.status.categories', [$services.wiki.currentWikiId, $categoriesSize])
      #foreach ($result in $categories)
        $result
      #end
      [[$services.localization.render('blog.migration.start')>>$doc.fullName||queryString="jobId=$!{escapetool.url($jobId)}&confirm=true" class="btn btn-primary"]]
    #end
  #elseif ($!request.confirm)
    $response.sendRedirect($doc.getURL('view',"jobId=$request.jobId"))
  #end
#end
{{/velocity}}
