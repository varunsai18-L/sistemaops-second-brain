---
id: xwiki-IconThemesCode.IconPicker
type: XWiki Page
space: "IconThemesCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905634000
sync_date: 2026-08-16 20:01:15
tags:
  - xwiki/documentation
  - space/iconthemescode
---
# Icon Picker

- **Space:** IconThemesCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905634000
- **Source:** [Icon Picker](https://wiki.systemaops.in/bin/view/IconThemesCode/IconThemesCode.IconPicker)

---

{{velocity}}
###########################
## DATA: ICON THEMES
###########################
#if ($request.action == 'data_iconthemes')
  #set ($map = {})
  #set ($discard = $map.put('iconThemes', $services.icon.iconSetNames))
  #set ($discard = $map.put('currentIconTheme', $services.icon.currentIconSetName))
  #jsonResponse($map)
###########################
## DATA: ICONS
###########################
#elseif ($request.action == 'data_icons')
  #set ($icons = [])
  #set ($iconTheme = $request.iconTheme)
  #set ($xwikiIcons = $collectiontool.sort($services.icon.getIconNames($iconTheme)))
  #set ($iconNamePrefix = $request.query.toLowerCase())
  #foreach ($xwikiIcon in $xwikiIcons)
    #if ("$!iconNamePrefix" == '' || $xwikiIcon.startsWith($iconNamePrefix))
      #set ($discard = $icons.add({
        'name': $xwikiIcon,
        'render': $services.icon.renderHTML($xwikiIcon, $iconTheme),
        'metadata': $services.icon.getMetaData($xwikiIcon, $iconTheme)
      }))
    #end
  #end
  #jsonResponse($icons)
#else
= Presentation =
The Icon Picker is a jQuery plugin written by XWiki to help user selecting an icon. See [[IconPickerMacro]] for using this picker easily. If you want to use it manually, read the following.

== Example ==
With Velocity and HTML:

{{code language="none"}}
// Enable the CSS of the picker:
\#set(\$discard = \$xwiki.ssx.use('IconThemesCode.IconPicker'))

// JavaScript code:
<script>

// Configure requirejs to load the picker code
require.config({
  paths: {
    'xwiki-icon-picker': '\$xwiki.getURL($services.model.createDocumentReference('', 'IconThemesCode', 'IconPicker'), 'jsx', "minify=$!request.minify")'
  }
});

// Require jquery and the icon picker
require(['jquery', 'xwiki-icon-picker'], function($) {
  // Here you can bind the picker to some elements.
  // Examples:
  $('#someElement').xwikiIconPicker(); // apply the picker to the field #someElement
  $('#someElement').xwikiIconPicker({prefix: 'image:icon:'}); // change the prefix inserted before the icon name
});

</script>
{{/code}}
#end
{{/velocity}}

