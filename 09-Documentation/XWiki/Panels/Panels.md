---
id: xwiki-Panels.WebHome
type: XWiki Page
space: "Panels"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906953000
sync_date: 2026-08-16 20:02:11
tags:
  - xwiki/documentation
  - space/panels
---
# Panels

- **Space:** Panels
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906953000
- **Source:** [Panels](https://wiki.systemaops.in/bin/view/Panels/Panels.WebHome)

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

