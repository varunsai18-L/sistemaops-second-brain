---
id: xwiki-XWiki.LiveTableResults
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905334000
sync_date: 2026-08-16 19:44:42
tags:
  - xwiki/documentation
  - space/xwiki
---
# Livetable Results

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905334000
- **Source:** [Livetable Results](https://wiki.systemaops.in/bin/view/XWiki/XWiki.LiveTableResults)

---

{{include reference="XWiki.LiveTableResultsMacros" /}}

{{velocity wiki="false"}}
## the $extra variable is passed to the call to #gridresultwithfilter below and is used to perform some default
## filtering on the LiveTable data even when the user has not performed any column filtering yet.
## When users start using column filtering, the generated DB query will combine both the default filtering and what the
## user has entered in the column filters.
#set ($extra = '')
#set ($params = {})
#if ("$!request.space" != '')
  #set ($extra = "${extra} AND doc.space = :doc_space")
  #set ($discard = $params.put('doc_space', $request.space))
#end
## Use filterLocation since addLivetableLocationFilter is buggy when called several times (it'll add the
## same HQL binding name every time it's called! See https://jira.xwiki.org/browse/XWIKI-17463).
## Also note that we don't call addLocationFilter since we use a Map for $params.
#filterLocation($extra, $params, $!request.location, 'locationFilterValue1')
#if ("$!request.parent" != '')
  #set ($extra = "${extra} and doc.parent = :doc_parent")
  #set ($discard = $params.put('doc_parent', $request.parent))
#end
#if ("$!request.orphaned" == '1')
  #set ($homepage = $services.wiki.getById($services.wiki.currentWikiId).mainPageReference)
  #set ($homepageFullName = $services.model.serialize($homepage, 'local'))
  ## On Oracle the empty parent is actually null.
  #set ($extra = "${extra} and (doc.parent = '' or doc.parent is null) and doc.fullName <> :homepageFullName")
  #set ($discard = $params.put('homepageFullName', $homepageFullName))
#end
#gridresultwithfilter("$!request.classname" $request.collist.split(',') '' "${extra}" $params)
{{/velocity}}
