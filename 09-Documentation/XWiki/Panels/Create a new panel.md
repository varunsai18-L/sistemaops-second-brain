---
id: xwiki-xwiki:Panels.CreatePanel
type: XWiki Page
space: "Panels"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906884000
sync_date: 2026-07-21 11:02:50
tags:
  - xwiki/documentation
  - space/panels
---
# Create a new panel

- **Space:** Panels
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906884000
- **Source:** [Create a new panel](https://wiki.systemaops.in/bin/view/Panels/xwiki:Panels.CreatePanel)

---

{{velocity output="false"}}
#macro (displayCreatePanelForm)
{{html clean="false"}}
  <form method="post" action="$doc.getURL('view', 'xpage=plain')" class="form-inline" onsubmit="cancelCancelEdit()">
    <div>
      <input type="hidden" name="form_token" value="$!escapetool.xml($services.csrf.token)" />
      <input type="hidden" name="create" value="1"/>
      <input type="hidden" name="parent" value="Panels.WebHome"/>
      <label for="panelTitle" class="hidden">
        $escapetool.xml($services.localization.render('xe.panels.create.title'))
      </label>
      <input type="text" id="panelTitle" name="panelTitle"
          placeholder="$escapetool.xml($services.localization.render('xe.panels.create.title'))" />
      <input type="submit" class="btn btn-success"
          value="$escapetool.xml($services.localization.render('create'))"/>
    </div>
  </form>
{{/html}}##
#end

#macro (createPanel $title)
  #set ($pageName = $services.modelvalidation.transformName($title))
  #set ($newPanelDoc = $xwiki.getDocument($services.model.createDocumentReference('', '', $pageName)))
  #if (!$newPanelDoc.isNew())
    #set ($redirecturl = $newPanelDoc.getURL('view', 'xpage=docalreadyexists'))
  #else
    #set ($template = "$!{request.getParameter('template')}")
    #if ($template == '')
      #set ($template = 'Panels.PanelTemplate')
    #end
    #set ($pcontent = "{{velocity}}${util.newline}${escapetool.h}panelheader('${title.replace('''', '''''')}')${util.newline}${util.newline}${escapetool.h}panelfooter()${util.newline}{{/velocity}}")
    #set ($redirectparams = "template=${escapetool.url($template)}&Panels.PanelClass_0_name=${escapetool.url($title)}&Panels.PanelClass_0_content=${escapetool.url($pcontent)}&parent=${escapetool.url($!request.parent)}&form_token=${request.form_token}")
    #set ($redirecturl = $newPanelDoc.getURL('edit', $redirectparams))
  #end
  $response.sendRedirect($redirecturl)
#end
{{/velocity}}

{{velocity}}
#if("$!{request.create}" == '')
  #displayCreatePanelForm()
#else
  #createPanel("$!{request.panelTitle.trim()}")
#end
{{/velocity}}
