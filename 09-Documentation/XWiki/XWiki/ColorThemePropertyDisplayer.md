---
id: xwiki-xwiki:XWiki.ColorThemePropertyDisplayer
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906201000
sync_date: 2026-07-21 11:01:20
tags:
  - xwiki/documentation
  - space/xwiki
---
# ColorThemePropertyDisplayer

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906201000
- **Source:** [ColorThemePropertyDisplayer](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.ColorThemePropertyDisplayer)

---

{{velocity}}
################################
## Globals
################################
#set ($isSubWiki = $services.wiki.currentWikiId != $services.wiki.mainWikiId)
#set ($flamingoThemesFromThisWiki = [])
#set ($flamingoThemesFromMainWiki = [])
#set ($colibriThemesFromThisWiki  = [])
#set ($colibriThemesFromMainWiki  = [])
#getFlamingoThemes($services.wiki.currentWikiId, $flamingoThemesFromThisWiki)
#getColibriThemes ($services.wiki.currentWikiId, $colibriThemesFromThisWiki )
#if ($isSubWiki)
  #getFlamingoThemes($services.wiki.mainWikiId,    $flamingoThemesFromMainWiki)
  #getColibriThemes ($services.wiki.mainWikiId,    $colibriThemesFromMainWiki )
  ## Enable the JavaScript for subwiki only
  #set ($discard = $xwiki.jsx.use('XWiki.ColorThemePropertyDisplayer'))
#end
#set ($currentScope = 'local')
#if ("$!value" != '' && $services.model.resolveDocument($value).wikiReference.name == $services.wiki.mainWikiId)
  #set ($currentScope = 'global')
#end
################################
## Get Flamingo themes
################################
#macro(getFlamingoThemes $wiki $return)
  #set ($results = [])
  #set ($xwql = "from doc.object(FlamingoThemesCode.ThemeClass) obj WHERE doc.fullName <> 'FlamingoThemesCode.ThemeTemplate' ORDER BY doc.name")
  #getThemesFromQuery ($xwql, $wiki, $results)
  #set ($return = $NULL)
  #setVariable ("$return", $results)
#end
################################
## Get Colibri themes
################################
#macro(getColibriThemes $wiki $return)
  #set ($results = [])
  #set ($xwql = "from doc.object(ColorThemes.ColorThemeClass) obj WHERE doc.fullName <> 'ColorThemes.ColorThemeTemplate' ORDER BY doc.name")
  #getThemesFromQuery ($xwql, $wiki, $results)
  #set ($return = $NULL)
  #setVariable ("$return" $results)
#end
################################
## Get themes from a query
################################
#macro(getThemesFromQuery $xwql $wiki $return)
  #set ($wikiReference = $services.model.createWikiReference($wiki))
  #set ($themes = $services.query.xwql($xwql).setWiki($wiki).execute())
  #set ($themesRef = [])
  #foreach ($theme in $themes)
    #set ($themeRef = $services.model.resolveDocument($theme, 'default', $wikiReference))
    #if ($services.security.authorization.hasAccess('view', $xcontext.userReference, $themeRef))
      #set ($discard = $themesRef.add($themeRef))
    #end
  #end
  #set ($return = $NULL)
  #setVariable("$return" $themesRef)
#end
################################
## Display an <option> line
################################
#macro(displayLine $themeRef $scope)
  #set($themeDoc = $xwiki.getDocument($themeRef))
  #if ($scope == 'local')
    #set($fullName = $services.model.serialize($themeRef, 'local'))
  #else
    #set($fullName = $services.model.serialize($themeRef, 'default'))
  #end
  <option value="$fullName"#if ($fullName.equals($value)) selected="selected"#end>
    $themeDoc.plainTitle
    #if ($isSubWiki && $scope == 'local')
      ($themeRef.wikiReference.name)
    #end
  </option>
#end
################################
## Display lines for a skin
################################
#macro(displaySkinLines $themesRef $name $scope)
  #if (!$themesRef.isEmpty())
    <optgroup label="$name" data-scope="$scope">
    #foreach ($themeRef in $themesRef)
      #displayLine($themeRef, $scope)
    #end
    </optgroup>
  #end
#end
################################
## Displayer
################################
{{html}}
  <div class="XWikiColorThemeDisplayer">
    #set ($colorThemeExists = $xwiki.exists($services.model.resolveDocument($value)))
    #if ("$!value" != '' && !$colorThemeExists)
      #error($services.localization.render('admin.colorthemes.invalidtheme', $escapetool.xml($value)))
    #end

    #if ($isSubWiki && (!$flamingoThemesFromMainWiki.isEmpty() || !$colibriThemesFromMainWiki.isEmpty()))
      <ul class="nav nav-tabs" role="tablist">
        <li role="presentation" #if ($currentScope=='local')class="active"#end><a href="#local" role="tab" data-toggle="tab" data-scope="local">$escapetool.xml($services.localization.render('admin.colorthemes.local'))</a></li>
        <li role="presentation" #if ($currentScope=='global')class="active"#end><a href="#global" role="tab" data-toggle="tab" data-scope="global">$escapetool.xml($services.localization.render('admin.colorthemes.global'))</a></li>
      </ul>
    #end

    <select name="${prefix}${name}" id="${prefix}${name}" data-current-scope="$currentScope">
      #if (!$colorThemeExists)
        <option value="$!escapetool.xml($value)" selected="selected">---</option>
      #else
        <option value=""#if ("$!value" == '')selected="selected"#end>---</option>
      #end
      #displaySkinLines($flamingoThemesFromThisWiki, $services.localization.render('admin.colorthemes.flamingothemes'), 'local')
      #displaySkinLines($colibriThemesFromThisWiki,  $services.localization.render('admin.colorthemes.colibrithemes'), 'local')
      #if ($isSubWiki)
        #displaySkinLines($flamingoThemesFromMainWiki, $services.localization.render('admin.colorthemes.flamingothemes'), 'global')
        #displaySkinLines($colibriThemesFromMainWiki,  $services.localization.render('admin.colorthemes.colibrithemes'), 'global')
      #end
    </select>
  </div>
{{/html}}
{{/velocity}}
