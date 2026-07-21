---
id: xwiki-xwiki:XWiki.AdminFieldsDisplaySheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906148000
sync_date: 2026-07-21 11:00:17
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminFieldsDisplaySheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906148000
- **Source:** [AdminFieldsDisplaySheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.AdminFieldsDisplaySheet)

---

{{velocity output="false"}}
#macro (__displayXProperty $prop)
  #set ($title = $services.localization.render($prop.name))
  #if ($title == $prop.name)
    #set ($title = $prop.prettyName)
  #end
  #if ($services.localization.get("${obj.xWikiClass.name}_${prop.name}"))
    #set ($title = $services.localization.render("${obj.xWikiClass.name}_${prop.name}"))
  #end
  #set ($hint = $services.localization.render("${obj.xWikiClass.name}_${prop.name}.hint"))
  #if ($hint == "${obj.xWikiClass.name}_${prop.name}.hint")
    #set($hint = $NULL)
  #end
  <dt>
  #set ($out = $configDoc.display($prop.name, 'edit', $obj).replaceAll('(^..html.*?}})|(../html..$)', ''))
  #set ($newId = "${configClassName}_${obj.number}_${prop.name}")
  <label#if ($out.matches("(?s).*id=['""]${newId}['""].*")) for="${newId}"#end class="$prop.name">##
  #if ($out.indexOf('type=''checkbox''') != -1 && $out.indexOf('class="xwiki-form-listclass"') == -1)
    $out ##
    #set ($out = '')
  #end
  $escapetool.xml($title)
  #if ($prop.name == 'skin')
    #set ($skin = $xwiki.skin)
    <span class="buttonwrapper">
      <a href="$xwiki.getURL($skin, 'edit')"#if ($skin.indexOf('.') < 0) class="hidden"#end>
        $escapetool.xml($services.localization.render('admin.customize'))
      </a>
    </span>
  #end
  #if ($prop.name == 'colorTheme')
    #if ($editor == 'globaladmin')
      #set ($colorThemeName = $xwiki.getXWikiPreference('colorTheme'))
    #else
      #set ($colorThemeName = $xwiki.getSpacePreference('colorTheme'))
      #set ($wikiColorTheme = $xwiki.getDocument($xwiki.getXWikiPreference('colorTheme')))
      #if (!$wikiColorTheme.isNew())
        #set ($colorThemeHint = $escapetool.xml($services.localization.render('admin.colortheme.wikiSetting', ['__LINK__'])).replaceAll('__LINK__', "<a href='$wikiColorTheme.getURL()'>$wikiColorTheme.plainTitle</a>"))
      #end
    #end
    #if ($xwiki.exists($services.model.createDocumentReference('', 'FlamingoThemes', 'WebHome')))
      #set ($colorThemeHint = "$!{colorThemeHint} <strong><a href=""$xwiki.getURL($services.model.createDocumentReference('', 'FlamingoThemes', 'WebHome'))"">$escapetool.xml($services.localization.render('admin.colortheme.manage'))</a></strong>")
    #elseif ($xwiki.exists($services.model.createDocumentReference('', 'ColorThemes', 'WebHome')))
      #set ($colorThemeHint = "$!{colorThemeHint} <strong><a href=""$xwiki.getURL($services.model.createDocumentReference('', 'ColorThemes', 'WebHome'))"">$escapetool.xml($services.localization.render('admin.colortheme.manage'))</a></strong>")
    #end
    <span class="buttonwrapper">
      <a href="$xwiki.getURL($colorThemeName, 'edit')"#if ($colorThemeName.indexOf('.') < 0) class="hidden"#end>
        $escapetool.xml($services.localization.render('admin.customize'))
      </a>
    </span>
  #end
  </label>
  #if ($hint)<span class="xHint">$escapetool.xml($hint)</span>#end
  </dt>
  #if ($out != '')
    <dd>$out</dd>
  #else
    ## We always display a dd element to avoid having a last dt element alone, which would lead to an invalid html.
    <dd class="hidden"></dd>
  #end
  #if ($prop.name == 'colorTheme' && $colorThemeHint)
    <dd class="xHint">$colorThemeHint</dd>
  #end
#end
{{/velocity}}

{{velocity}}
### Sheet used to generically display the XWikiPreferences object fields in the administration sheets.
### Input variables:
### - $params (mandatory): list of properties to display and their associated sections
### - $paramDoc (optional): document object which contains the $paramClass
### - $paramClass (optional): name of the xclass type for the xobject from which to read/save from
### - $objectPolicy (since 14.10) (optional): the update policy to use when saving the form
#if ("$!section" != '')
  ## clean="false" due to bug #XWIKI-4122 - the <legend> element is dropped.
  {{html clean="false"}}
  #if ("$!paramDoc" != '')
    #set($configDoc = $paramDoc)
  #else
    #set($configDoc = $doc)
  #end
  #if ("$!paramClass" != '')
    #set($configClassName = $paramClass)
    #set($formId = "${section.toLowerCase()}_${configClassName}")
  #else
    #set($configClassName = 'XWiki.XWikiPreferences')
    #set($formId = $section.toLowerCase())
  #end
  <form id="$escapetool.xml($formId)" method="post"
      action="$escapetool.xml($xwiki.getURL($configDoc, 'saveandcontinue'))"
      onsubmit="cancelCancelEdit()"
      class="xform">
    #set($obj = $configDoc.getObject($configClassName))
    #foreach ($entry in $params.entrySet())
      #set ($fields = $entry.value)
      <fieldset class="$escapetool.xml($entry.key)">
      ## If there is only one section, don't display the legend
      #if ($params.size() > 1)
        <legend>$escapetool.xml($services.localization.render("admin.$entry.key"))</legend>
      #end
      #if ($fields.size() > 0)
        <dl>
      #end
      #foreach ($field in $fields)
        #set ($prop = $obj.xWikiClass.get($field))
        #if ($prop)
          #__displayXProperty($prop)
        #elseif ($field.html)
          $field.html
        #end
      #end
      #if ($fields.size() > 0)
        </dl>
      #end
      </fieldset>
    #end
    <div class="hidden">
      <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
      <input type="hidden" name="xcontinue" value="$xwiki.getURL($currentDoc, 'admin', "editor=${escapetool.url(${editor})}&amp;section=${escapetool.url(${section})}&amp;space=${escapetool.url(${currentSpace})}")" />
      <input type="hidden" name="xredirect" value="$xwiki.getURL($currentDoc, 'admin', "editor=${escapetool.url(${editor})}&amp;section=${escapetool.url(${section})}&amp;space=${escapetool.url(${currentSpace})}")" />
      <input type="hidden" name="classname" value="$escapetool.xml($configClassName)" />
      #if ("$!objectPolicy" != '')
      <input type="hidden" name="objectPolicy" value="$escapetool.xml($objectPolicy)" />
      #end
    </div>
    <div class="bottombuttons">
      <p class="admin-buttons">
        <span class="buttonwrapper"><input class="button" type="submit" name="formactionsac" 
          value="$escapetool.xml($services.localization.render('admin.save'))" /></span>
      </p>
    </div> ## bottombuttons
  </form>
  {{/html}}
#end
{{/velocity}}
