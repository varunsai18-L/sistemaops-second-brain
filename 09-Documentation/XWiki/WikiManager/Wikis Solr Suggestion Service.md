---
id: xwiki-xwiki:WikiManager.WikisSuggestSolrService
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906674000
sync_date: 2026-07-21 11:02:05
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Wikis Solr Suggestion Service

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906674000
- **Source:** [Wikis Solr Suggestion Service](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.WikisSuggestSolrService)

---

{{include reference="XWiki.SuggestSolrMacros" /}}

{{velocity}}
#if ("$!request.query" != '' && "$!request.input" != '')
  #getSearchSuggestResults($results)
  #set ($discard = $response.setContentType('text/xml'))
  <?xml version="1.0" encoding="UTF-8"?>
  <results>
    #foreach ($result in $results)
      #set ($documentReference = $services.solr.resolveDocument($result))
      #set ($wikiId = $stringtool.substringAfter($documentReference.name, 'XWikiServer').toLowerCase())
      #set ($wikiDescriptor = $services.wiki.getById($wikiId))
      #if ($wikiDescriptor)
        #set ($name = $wikiDescriptor.prettyName)
        #if ("$!name.trim()" == '')
          #set ($name = $wikiDescriptor.id)
        #end
        #set ($url = $xwiki.getURL($wikiDescriptor.mainPageReference))
        <rs id="$escapetool.xml($wikiId)" type="wiki" url="$escapetool.xml($url)">$escapetool.xml($name)</rs>
      #end
    #end
  </results>
#else
  {{info}}
    This service provides search results for the search suggest UI component.
    Examples:
    * [[$doc.getExternalURL('get', $escapetool.url({
        'outputSyntax': 'plain',
        'query': 'class:XWiki.XWikiServerClass AND propertyname:wikiprettyname AND propertyvalue__:__INPUT__*',
        'input': 'home'
      }))]]
  {{/info}}
#end
{{/velocity}}
