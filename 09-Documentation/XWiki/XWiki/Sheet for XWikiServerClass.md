---
id: xwiki-XWiki.XWikiServerClassSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906684000
sync_date: 2026-08-25 21:13:40
tags:
  - xwiki/documentation
  - space/xwiki
---
# Sheet for XWikiServerClass

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906684000
- **Source:** [Sheet for XWikiServerClass](https://wiki.systemaops.in/bin/view/XWiki/XWiki.XWikiServerClassSheet)

---

{{velocity}}
#############################
##        GLOBALS
#############################
#set ($wikiId = $doc.documentReference.name.replaceAll('XWikiServer', '').toLowerCase())
#set ($wiki = $services.wiki.getById($wikiId))
#set ($descriptorObj = $doc.getObject('XWiki.XWikiServerClass'))
#set ($templateObj = $doc.getObject('WikiManager.WikiTemplateClass'))
#set ($aliases = $doc.getObjects('XWiki.XWikiServerClass'))
#############################
##       CONTROLLER
#############################
#controller()
#macro(controller)
  #if ($doc.fullName == "XWiki.XWikiServerClassSheet" || $doc.fullName == "XWiki.XWikiServerClassTemplate")
    = Document "$doc.documentReference.name" =
  #elseif ($request.action == 'create' && "$!request.domain" != '' && $request.domain.trim().length() > 0)
    #createAlias()
  #elseif ($request.action == 'delete' && "$!request.domain" != '' && $request.domain.trim().length() > 0)
    #deleteAlias()
  #elseif ($xcontext.action == 'edit')
    #edit()
  #else
    #view()
  #end
#end
#############################
##         VIEW
#############################
#macro(view)
  #set($adminPageRef = $services.model.createDocumentReference($wiki.id, 'XWiki', 'XWikiPreferences'))
  #set($adminPageLink = "[[$services.localization.render('platform.wiki.sheet.descriptor.admin')>>$adminPageRef]]")
  {{translation key="platform.wiki.sheet.descriptor" parameters="${wiki.id},${adminPageLink}"/}} $adminPageLink
  
  {{toc /}}
  #displaySettings()
  #displayAliases()
  #createAliasForm()
#end
#############################
##         EDIT
#############################
#macro(edit)
  {{toc /}}
  #displaySettings()
  #displayAliases()
#end
#############################
##      CREATE ALIAS
#############################
#macro(createAlias)
  #if (!${services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})

    {{error}}{{translation key="notallowed"/}}{{/error}}

  #elseif (!$wiki.aliases.contains($request.domain))
    #set ($alias = $doc.newObject("XWiki.XWikiServerClass"))
    #set ($discard = $alias.set("server", $request.domain))
    #set ($discard = $alias.set("homepage", "Main.WebHome"))
    #set ($discard = $doc.save())
    $response.sendRedirect($doc.getURL())
  #else

    {{error}}{{translation key="platform.wiki.sheet.erroraliasalreadynotexists" parameters="~"${services.rendering.escape($escapetool.java($request.domain), 'xwiki/2.1')}~""/}}{{/error}}

  #end
#end
#############################
##      DELETE ALIAS
#############################
#macro(deleteAlias)
  #if (!${services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})

    {{error}}{{translation key="notallowed"/}}{{/error}}
    
  #elseif ($wiki.aliases.contains($request.domain))
    #set ($alias = $doc.getObject('XWiki.XWikiServerClass', 'server', $request.domain))
    #set ($removed = $doc.removeObject($alias))
    #set ($discard = $doc.save())
    $response.sendRedirect($doc.getURL())
  #else
  
    {{error}}{{translation key="platform.wiki.sheet.erroraliasdoesnotexists" parameters="~"${services.rendering.escape($escapetool.java($request.domain), 'xwiki/2.1')}~""/}}{{/error}}
    
  #end
#end
#############################
##    DISPLAY SETTINGS
#############################
#macro(displaySettings)
  (% id="HWikiProperties" %)
  = {{translation key="platform.wiki.sheet.title.settings"/}} =
  {{html wiki="true" clean="false"}}
  <div class="xform">
  <dl>
    #displayField('wikiprettyname', $descriptorObj)
    #displayField('owner', $descriptorObj)
    #displayField('secure', $descriptorObj)
    #displayField('port', $descriptorObj)
    #displayField('iswikitemplate', $templateObj)
    #displayField('server', $descriptorObj)
    #displayField('description', $descriptorObj)
    #displayField('homepage', $descriptorObj, "#homePagePicker($descriptorObj)")
  </dl>
  </div>
  {{/html}}
#end
#############################
##      DISPLAY FIELD
#############################
#macro(displayField $fieldName $object $customDisplay)
  #if ("$!object" != '')
    <dt>
      #if ($xcontext.action=='edit')
        <label for="${object.xWikiClass.name}_${object.number}_${fieldName}">
      #else
        <label>
      #end
      {{translation key="platform.wiki.sheet.prop.${fieldName}" /}}:
      </label>
      <span class="xHint">{{translation key="platform.wiki.sheet.desc.${fieldName}" /}}</span>
    </dt>
    <dd>#if ("$!customDisplay" != '')$customDisplay#else$object.get($fieldName)#end</dd>
  #end
#end
#macro (homePagePicker $object)
  #if ($xcontext.action == 'edit')
    ## The wiki descriptor is stored on the main wiki so we need to configure the page picker to give suggestions from
    ## the corresponding wiki (not from the main wiki).
    #set ($id = "${object.xWikiClass.name}_${object.number}_homepage")
    #set ($homePagePickerParams = {
      'id': $id,
      'name': $id,
      'value': $object.getValue('homepage'),
      'data-search-scope': "wiki:$wikiId"
    })
    #pagePicker($homePagePickerParams)
  #end
#end
#############################
##    DISPLAY ALIASES
#############################
#macro(displayAliases)
  (% id="HWikiViewAliases" %)
  = {{translation key="platform.wiki.sheet.title.viewaliases"/}} =
  {{translation key="platform.wiki.sheet.aliases"/}}
  #if ($aliases.size() > 1)
    #foreach ($alias in $aliases)
      #if ($foreach.count > 1)
        == $alias.display('server', 'view') ==
        {{html wiki="true" clean="false"}}
        <div class="xform">
          <dl>
            #displayField('description', $alias)
            #displayField('homepage', $alias)
          </dl>
        </div>
        {{/html}}
        #if ($xcontext.action == 'view')
          #deleteButton($alias)
        #end
      #end
    #end 
  #end
#end
#############################
##   DELETE ALIAS BUTTON
#############################
#macro(deleteButton $alias)
  #if($xcontext.action == 'view')

    {{html}}
      <form method="get" action="$doc.getURL('view')">
        <fieldset>
          <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
          <input type="hidden" name="action" value="delete"/>
          <input type="hidden" name="domain" value="$alias.server"/>
          <input type="submit" class="button" value="$services.localization.render('delete')"/>
        </fieldset>
      </form>
    {{/html}}

  #end
#end
#############################
##   CREATE ALIAS FORM
#############################
#macro(createAliasForm)
  (% id="HWikiCreateNewAlias" %)
  = {{translation key="platform.wiki.sheet.title.createnewalias"/}} =
  
  {{html}}
    <form method="get" action="$doc.getURL('view')">
      <fieldset>
        <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
        <input type="hidden" name="action" value="create"/>
        <label for="inputdomain">$services.localization.render('platform.wiki.sheet.prop.server')</label>:
        <input id="inputdomain" type="text" name="domain" class="wikialiasinput"/>
        <input type="submit" class="button" value="$services.localization.render('create')"/>
      </fieldset>
    </form>
  {{/html}}
  
#end
{{/velocity}}
