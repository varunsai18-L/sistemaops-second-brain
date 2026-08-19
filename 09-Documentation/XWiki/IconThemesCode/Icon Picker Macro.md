---
id: xwiki-IconThemesCode.IconPickerMacro
type: XWiki Page
space: "IconThemesCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905601000
sync_date: 2026-08-19 20:22:26
tags:
  - xwiki/documentation
  - space/iconthemescode
---
# Icon Picker Macro

- **Space:** IconThemesCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905601000
- **Source:** [Icon Picker Macro](https://wiki.systemaops.in/bin/view/IconThemesCode/IconThemesCode.IconPickerMacro)

---

= Usage =
{{code}}
{{iconPicker id="" class="" prefix="" /}}
{{/code}}

**Where:**
|=id (optional)|DOM id of the input field where the picker will apply
|=class (optional)|CSS class of inputs where the picker will apply
|=prefix (optional)|Prefix to add before the name of the icon in the input field (default: "{{{image:icon:}}}")
== Live example ==
{{code}}
{{html}}
  <p><label>Field 1: <input type="text" id="myPicker" /></label></p>
  <p><label>Field 2: <input type="text" class="fieldWithPicker" /></label></p>
{{/html}}

{{iconPicker id="myPicker" class="fieldWithPicker" prefix="icon:" /}}
{{/code}}
== Play with it ==
{{html}}
  <p><label>Field 1: <input type="text" id="myPicker" /></label></p>
  <p><label>Field 2: <input type="text" class="fieldWithPicker" /></label></p>
{{/html}}

{{iconPicker id="myPicker" class="fieldWithPicker" prefix="icon:" /}}
