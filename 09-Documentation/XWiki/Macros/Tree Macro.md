---
id: xwiki-xwiki:Macros.Tree
type: XWiki Page
space: "Macros"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905510000
sync_date: 2026-07-21 11:00:43
tags:
  - xwiki/documentation
  - space/macros
---
# Tree Macro

- **Space:** Macros
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905510000
- **Source:** [Tree Macro](https://wiki.systemaops.in/bin/view/Macros/xwiki:Macros.Tree)

---

== Static tree ==

{{tree}}
* [[Chapter 1>>Main.WebHome]]
** Section 2.1
** Section 2.2
*** Paragraph 2.2.1
**** Once upon a time...
*** Paragraph 2.2.2
* [[Chapter 2>>Sandbox.WebHome]]
* [[Chapter 3>>http://www.xwiki.org]]
** Section 3.1
*** Paragraph 3.1.1
** Section 3.2
{{/tree}}

=== Static tree with opened path ===

{{tree}}
{{velocity}}
{{html}}
<ul>
  <li class="jstree-open">
    <a href="$xwiki.getURL('Main.WebHome')">One</a>
    <ul>
      <li class="jstree-open">
        <a href="http://www.xwiki.org">Two</a>
        <ul>
          <li>
            <a href="#section" class="jstree-clicked">Three</a>
          </li>
        </ul>
      </li>
    </ul>
  </li>
</ul>
{{/html}}
{{/velocity}}
{{/tree}}

=== Static tree with custom icons ===

{{tree}}
{{html}}
<ul>
  <li data-jstree='{"opened":true,"selected":true}'>Users
    <ul>
      <li data-jstree='{"disabled":true}'>Alice</li>
      <li data-jstree='{"icon":"http://jstree.com/tree.png"}'>Bob</li>
      <li data-jstree='{"icon":"glyphicon glyphicon-leaf"}'>Carol</li>
    </ul>
  </li>
</ul>
{{/html}}
{{/tree}}

== Dynamic Tree ==

{{tree reference="XWiki.DocumentTree" /}}

=== Dynamic Sub-tree with Checkboxes ===

{{tree reference="doc:XWiki.DocumentTree" root="document:xwiki:Sandbox.WebHome" checkboxes="true" /}}
