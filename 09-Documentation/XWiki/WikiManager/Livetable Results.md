---
id: xwiki-xwiki:WikiManager.WikisLiveTableResults
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906671000
sync_date: 2026-07-21 11:02:04
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Livetable Results

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906671000
- **Source:** [Livetable Results](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.WikisLiveTableResults)

---

{{include reference="WikiManager.WikisLiveTableResultsMacros" /}}

{{velocity wiki="false"}}
#set($from =  "")
#set($extra = "")
#set($params = [])
## Restrict to the list of wiki I can see
#set ($extra = "${extra} and doc.name IN (")
#set ($separator = "")
#foreach ($wiki in $services.wiki.getAll())
  #try("wikisListException")
    ## XWiki.XWikiComments is a mandatory document that it must exists and we should have acces to it
    #set ($testPageReference = $services.model.createDocumentReference($wiki.id, 'XWiki', 'XWikiComments'))
    #if ($xwiki.hasAccessLevel('view', $xcontext.user, $testPageReference) ||
      ($services.wiki.user.getUserScope($wiki.id) != 'LOCAL_ONLY' && $services.wiki.user.getMembershipType($wiki.id) != 'INVITE') ||
      $services.wiki.user.hasPendingInvitation($xcontext.userReference, $wiki.id))
      #set ($extra = "${extra}${separator}'XWikiServer${stringtool.capitalize($wiki.id)}'")
      #set ($separator = ",")
    #end
  #end
  #if ("$!wikisListException" != '')
    $services.logging.getLogger("WikiManager.WikisLiveTableResultsMacros")
      .warn("An error occurred while listing wiki [${wiki.id}].", $wikisListException)
  #end
#end
#set ($extra = "${extra})")
## Restrict to templates only
#if("$!request.onlyTemplates" == '1')
  #set($from = "${from}, BaseObject objTemplate, IntegerProperty propTemplate")
  #set($extra = "${extra} AND doc.fullName = objTemplate.name AND objTemplate.className='WikiManager.WikiTemplateClass' AND objTemplate.id = propTemplate.id AND propTemplate.name='iswikitemplate' AND propTemplate.value='1'")
#end
#set($columns = [])
#foreach($c in $request.collist.split(","))
  #if($c != 'membershipType')
    #set($discard = $columns.add($c))
  #end
#end
#gridresultwithfilter("$!request.classname" $columns "${from}" "${extra}" $params)
{{/velocity}}
