---
id: xwiki-Blog.BlogPostLayoutMacros
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907602000
sync_date: 2026-08-25 21:14:32
tags:
  - xwiki/documentation
  - space/blog
---
# BlogPostLayoutMacros

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907602000
- **Source:** [BlogPostLayoutMacros](https://wiki.systemaops.in/bin/view/Blog/Blog.BlogPostLayoutMacros)

---

{{velocity output='false'}}
#**
 * Extract the layout parameters from a string.
 * 
 * @param layoutParamsString The string representation of the layout parameters.
 * It should contain a String following this format "paramName1=Value1|paramName2=Value2|...|paramNameK=ValueK"
 * @param layoutsParameters The resulting layout parameters Map.
 *###
#macro(extractLayoutParametersFromString $layoutParamsString $layoutsParameters)
  #set ($layoutsParameters = $NULL)
  #set ($macro.layoutParams = {})
  #if ("$!layoutParamsString" != '')
    #set ($macro.paramsArr = $layoutParamsString.split('\|'))
    #foreach ($item in $macro.paramsArr)
      #set ($itemSplit = $item.split('='))
      #if ($itemSplit.size() == 2)
        #set ($discard = $macro.layoutParams.put($itemSplit[0].trim(), $itemSplit[1].trim()))
      #end
    #end
  #end
  #setVariable("$layoutsParameters" $macro.layoutParams)
#end
{{/velocity}}

