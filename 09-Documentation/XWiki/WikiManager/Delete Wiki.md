---
id: xwiki-WikiManager.DeleteWiki
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906681000
sync_date: 2026-08-16 20:01:43
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Delete Wiki

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906681000
- **Source:** [Delete Wiki](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.DeleteWiki)

---

{{velocity}}
#set ($docextras=[])
#macro (printException $exception)
  #if($exception.message)
    {{error}}$services.localization.render('platform.wiki.error.exceptionWithMessage', [$exception.message]){{/error}}
  #else
    {{error}}$exception.class{{/error}}
  #end
#end
##
#set ($wikiId = $request.wikiId)
#set ($wikiIdConfirm = ${request.wikiIdConfirm})
#set ($form_token = $request.form_token)
##
#if ("$!wikiId" == '')
  {{error}}{{translation key="platform.wiki.error.oneParameterNotSpecified" parameters="wikiId"/}}{{/error}}
#else
  ## FIXME: add plugin dependency checks.
  ##
  ##
  #set ($wiki = $services.wiki.getById($wikiId))
  ##
  #if (!$wiki)
    #if (!$services.wiki.lastError)
      #set ($escapedWikiId = $services.rendering.escape($escapetool.java($wikiId), 'xwiki/2.1'))
      {{error}}{{translation key="platform.wiki.error.wikidoesnotexist" parameters="~"${escapedWikiId}~""/}}{{/error}}
    #else
      #printException($services.wiki.lastError)
    #end
  #else
    #set ($currentUser = "${services.wiki.mainWikiId}:${xcontext.user}")
    #set ($wikiMainPage = $wiki.mainPageReference)
    #set ($wikiMainPageLinkStart = '')
    #set ($wikiMainPageLinkEnd = '')
    #if ($xwiki.exists($wikiMainPage))
      #set ($wikiMainPageLinkStart = '[[')
      #set ($wikiMainPageLinkEnd = ">>${wikiMainPage}]]")
    #end
    ##
    #if (!$services.wiki.canDeleteWiki($currentUser, $wikiId))
      {{error}}The user #if($xcontext.user != 'XWiki.XWikiGuest')[[$currentUser]]#{else}$xcontext.user#end is not allowed to delete the wiki ${wikiMainPageLinkStart}${wikiId}${wikiMainPageLinkEnd}.{{/error}}
    #else

      #set ($formTokenValid = $services.csrf.isTokenValid($form_token))
      #set ($wikiIdMatches = "$!wikiId" == "$!wikiIdConfirm")
      #if (!$formTokenValid || !$wikiIdMatches)
        #set ($browseDocumentReference = $services.model.createDocumentReference($services.wiki.mainWikiId, 'WikiManager', 'WebHome'))
        #set ($backUrl = $xwiki.getURL($browseDocumentReference))
        #if ("$!form_token" != '')
          #if (!$formTokenValid)

            {{warning}}
              {{translation key="platform.wiki.csrf.error" /}}
            {{/warning}}

          #end
          #if (!$wikiIdMatches)

            {{error}}
              {{translation key="platform.wiki.delete.error.wikiIdDoesNotMatch"/}}
            {{/error}}

          #end
        #end
        {{box}}
          $services.localization.render('platform.wiki.delete.confirmation', [$wikiMainPageLinkStart, $wikiId, $wikiMainPageLinkEnd])
          ((({{html}}
            <form action="$doc.getURL()" method="post">
              <input type="hidden" name="wikiId" value="$!escapetool.xml($wikiId)" />
              <input type="hidden" name="form_token" value="$!escapetool.xml($services.csrf.getToken())" />
              <p>
                <label for='wikiDeleteConfirmation'>$services.localization.render('platform.wiki.delete.confirmation.retypeWikiId')</label>
                <input type="text" name="wikiIdConfirm" value="$!{escapetool.xml($wikiIdConfirm)}" id="wikiDeleteConfirmation" class="required" />
              </p>
              <button class="btn btn-danger" id="confirmButton">$services.localization.render('delete')</button>
              <a class="btn btn-default" href="$backUrl">$services.localization.render('cancel')</a>
            </form>
          {{/html}})))
        {{/box}}
      #else
        ## The form_token is valid
        #set ($temp = $services.wiki.deleteWiki($wikiId))
        #if ($services.wiki.lastError)
          #printException($services.wiki.lastError)
        #else
          {{success}}$services.localization.render('platform.wiki.delete.success', ['[[', $currentUser, ">>$currentUser]]", $wikiId]){{/success}}
        #end
      #end
    #end
  #end
#end
{{/velocity}}
