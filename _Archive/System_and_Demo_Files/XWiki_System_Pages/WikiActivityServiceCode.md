---
id: xwiki-xwiki:WikiManager.WikiActivityServiceCode
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906684000
sync_date: 2026-07-21 11:02:10
tags:
  - xwiki/documentation
  - space/wikimanager
---
# WikiActivityServiceCode

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906684000
- **Source:** [WikiActivityServiceCode](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.WikiActivityServiceCode)

---

{{velocity}}
#set ($parameterName = 'wikiName')
#set ($wikiNames = $request.getParameterValues($parameterName))
#if ("$!wikiNames" == '' || $wikiNames.size() == 0)
  {{translation key="platform.wiki.users.profile.activity.hint"/}}

  {{error}}{{translation key="platform.wiki.error.oneParameterNotSpecified" parameters="$parameterName"/}} {{translation key="platform.wiki.error.parameterAcceptsMultipleValues"/}}{{/error}}
#else
  #set ($wikiNamesList = '')
  #foreach ($wikiName in $wikiNames)
    #if ("$!wikiName" != '')
      #set ($wikiNamesList = "$wikiName, $wikiNamesList")
    #end
  #end
  #set ($wikiNamesList = $wikiNamesList.replaceAll(',\s$',''))
  = #if ($wikiNames.size() == 1)$services.localization.render('platform.wiki.users.profile.activity.title', [$wikiNamesList])#{else}$services.localization.render('platform.wiki.users.profile.activity.multipletitle', [$wikiNamesList])#end =
  {{notifications useUserPreferences="false" displayOwnEvents="true" displayRSSLink="false" wikis="$wikiNamesList"}}
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
