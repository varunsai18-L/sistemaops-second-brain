---
id: xwiki-XWiki.DocumentTree
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905664000
sync_date: 2026-08-16 20:01:19
tags:
  - xwiki/documentation
  - space/xwiki
---
# Document Tree

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905664000
- **Source:** [Document Tree](https://wiki.systemaops.in/bin/view/XWiki/XWiki.DocumentTree)

---

{{include reference="XWiki.DocumentTreeMacros" /}}

{{velocity wiki="false"}}
#if ($xcontext.action == 'get')
  #updateDocTreeConfigFromRequest
  #handleDocumentTreeRequest
#end
{{/velocity}}

{{velocity}}
#if ($xcontext.action != 'get')
  == Document Hierarchy Tree ==

  {{documentTree /}}

  === Compact Document Hierarchy Tree ===

  {{documentTree compact="true" /}}

  == Wiki > Space > Page Tree ==

  {{documentTree showWikis="true" showSpaces="true" showTranslations="false" showAttachments="false" showChildDocuments="false" /}}

  == Full Entity Tree ==

  {{documentTree showWikis="true" showWikiPrettyName="false" showSpaces="true" showDocumentTitle="false"
    showChildDocuments="false" showObjects="true" showClassProperties="true" /}}
#end
{{/velocity}}
