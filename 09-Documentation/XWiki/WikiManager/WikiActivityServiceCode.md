---
id: xwiki-WikiManager.WikiActivityServiceCode
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906684000
sync_date: 2026-08-16 20:01:44
tags:
  - xwiki/documentation
  - space/wikimanager
---
# WikiActivityServiceCode

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906684000
- **Source:** [WikiActivityServiceCode](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.WikiActivityServiceCode)

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
