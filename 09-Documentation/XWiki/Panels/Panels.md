---
id: xwiki-xwiki:Panels.WebHome
type: XWiki Page
space: "Panels"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906953000
sync_date: 2026-07-21 11:03:00
tags:
  - xwiki/documentation
  - space/panels
---
# Panels

- **Space:** Panels
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906953000
- **Source:** [Panels](https://wiki.systemaops.in/bin/view/Panels/xwiki:Panels.WebHome)

---

{{velocity}}
#if($hasAdmin)
= $services.localization.render('xe.panels.create') =
{{include reference="Panels.CreatePanel"/}}
#end
= $services.localization.render('panels.available') =
#if ($hasAdmin)
  {{box}}
    $services.icon.render('wand') $services.localization.render('panels.customize', ["[[$services.localization.render('panelwizard.panelwizard')>>Panels.PanelWizard]]"]).
  {{/box}}
#end
#set ($liveDataConfig = {
  'meta': {
    'propertyDescriptors': [
      { 'id': 'name', 'displayer': 'link' }
    ]
  }
})
#set ($sourceParameters = $escapetool.url({
  'className': 'Panels.PanelClass',
  'translationPrefix' : 'panels.',
  'queryFilters': 'currentlanguage'
}))

{{liveData
  id='panels'
  source='liveTable'
  sourceParameters="$sourceParameters"
  properties='name,description,type,category,_actions'
  limit=30
}}$jsontool.serialize($liveDataConfig){{/liveData}}
{{/velocity}}


---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
