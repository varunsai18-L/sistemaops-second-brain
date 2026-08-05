---
id: xwiki-xwiki:XWiki.XWikiClassesLiveTableResults
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906696000
sync_date: 2026-07-21 11:02:17
tags:
  - xwiki/documentation
  - space/xwiki
---
# XWikiClassesLiveTableResults

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906696000
- **Source:** [XWikiClassesLiveTableResults](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.XWikiClassesLiveTableResults)

---

{{include reference="XWiki.LiveTableResultsMacros" /}}

{{velocity wiki="false"}}
#if ($xcontext.action == 'get' && $request.outputSyntax == 'plain')
  ## Include only the pages that have a class definition.
  #set ($extra = "and (doc.xWikiClassXML is not null and doc.xWikiClassXML like '<%')")
  #set ($params = {})
  #addLivetableLocationFilter($extra $params $!request.location)
  #set ($output = {})
  #gridresultwithfilter_buildJSON('' $request.collist.split(',') '' $extra $params $output)
  ## Compute the page count for each class.
  #foreach ($row in $output.rows)
    #set ($statement = ', BaseObject as obj where doc.translation = 0 and ' +
      'doc.fullName = obj.name and obj.className = :className')
    ## Note: the unique filter is required as otherwise pages are returned once for each contained XObjects, leading
    ## to larger counts than expected.
    #set ($hqlQuery = $services.query.hql($statement).bindValue('className', $row.doc_fullName).addFilter('unique'))
    #set ($row.pageCount = $hqlQuery.count())
  #end
  #jsonResponse($output)
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
