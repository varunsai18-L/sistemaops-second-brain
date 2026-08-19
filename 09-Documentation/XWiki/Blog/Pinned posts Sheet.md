---
id: xwiki-Blog.PinnedPostsSheet
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907629000
sync_date: 2026-08-19 20:23:47
tags:
  - xwiki/documentation
  - space/blog
---
# Pinned posts Sheet

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907629000
- **Source:** [Pinned posts Sheet](https://wiki.systemaops.in/bin/view/Blog/Blog.PinnedPostsSheet)

---

{{velocity output="false"}}
#macro (stripHTMLMacro $displayOutput)
  $stringtool.removeEnd($stringtool.removeStart($displayOutput, '{{html clean="false" wiki="false"}}'), '{{/html}}')
#end
{{/velocity}}

{{velocity}}
#set ($discard = $xwiki.jsx.use('Blog.PinnedPostsSheet'))
{{html clean="false"}}
<div class="row">
  <div class="col-md-12">
    <h3>
      $services.localization.render('blog.post.layout.cards.pinnedposts.edit')
    </h3>
    <div id="pinnedPostsContainer">
      <form id="pinnedPostsForm" action="$doc.getURL('save')" method="post">
        #if ("$!doc.getObject('Blog.PinnedPostsClass')" != '')
          #set ($vdoc = $doc)
        #else
          #set ($vdoc = $xwiki.getDocument("Blog.PinnedPostsTemplate"))
        #end
        #set ($displayOutput = $vdoc.display('posts', 'edit'))
        #stripHTMLMacro($displayOutput)
        #set ($orderedPosts = $vdoc.getObject('Blog.PinnedPostsClass').getValue('orderedPosts'))
        <input type="hidden" id="Blog.PinnedPostsClass_0_orderedPosts" name="Blog.PinnedPostsClass_0_orderedPosts" value="$escapetool.xml($orderedPosts)"/>
        <input type="hidden" name="form_token" value="$services.csrf.token"/>
        <div>
          <input class="btn btn-primary" type="submit" name="action_save" value="$escapetool.xml($services.localization.render('blog.post.layout.cards.pinnedposts.save'))" id="savePinnedPostsBtn"/>
        </div>
      </form>
      <div id="errors-container"></div>
    </div>
  </div>
</div>
{{/html}}
{{/velocity}}
