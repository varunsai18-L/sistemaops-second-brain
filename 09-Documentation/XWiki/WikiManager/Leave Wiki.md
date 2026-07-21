---
id: xwiki-xwiki:WikiManager.LeaveWiki
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906657000
sync_date: 2026-07-21 11:02:02
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Leave Wiki

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906657000
- **Source:** [Leave Wiki](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.LeaveWiki)

---

{{velocity}}
#set ($wikiId = $request.wikiId)
#set ($form_token = $request.form_token)
##
#if ("$!wikiId" == '')
  {{error}}{{translation key="platform.wiki.error.oneParameterNotSpecified" parameters="wikiId"/}}{{/error}}
#else
  ## FIXME: add plugin dependency checks.
  ##
  #set ($wiki = $services.wiki.getById($wikiId))
  ##
  #if ("$!wiki" == '')
    #if ("$!{$services.wiki.lastError}" != '')
      {{error}}$services.localization.render('platform.wiki.error.exceptionWithMessage', [$services.wiki.lastError.message]){{/error}}
    #else
      {{error}}{{translation key="platform.wiki.error.wikidoesnotexist" parameters="$wikiId"/}}{{/error}}
    #end
  #else
    #set ($wikiName = $wiki.prettyName)
    #if ("$!wikiName" == '')
      #set ($wikiName = $wikiId)
    #end
    #set ($currentUser = "${xcontext.mainWikiName}:${xcontext.user}")
    #set ($wikiMainPage = $wiki.mainPageReference)
    #set ($wikiMainPageLinkStart = '')
    #set ($wikiMainPageLinkEnd = '')
    #if ($xwiki.exists($wikiMainPage))
      #set ($wikiMainPageLinkStart = '[[')
      #set ($wikiMainPageLinkEnd = ">>${wikiMainPage}]]")
    #end
    ##
    #set ($members = $services.wiki.user.getMembers($wikiId))
    #if (!$members || !$members.contains($currentUser))
      {{error}}$services.localization.render('platform.wiki.users.userNotMemberOfWiki', ['[[', $currentUser, ">>$currentUser]]", $wikiMainPageLinkStart, $wikiName, $wikiMainPageLinkEnd]){{/error}}
    #elseif ($wiki.ownerId == $currentUser)
      {{error}}$services.localization.render('platform.wiki.users.leave.error.userIsOwner', ['[[', $currentUser, ">>$currentUser]]", $wikiMainPageLinkStart, $wikiName, $wikiMainPageLinkEnd]){{/error}}
    #else
      #if (!$services.csrf.isTokenValid($form_token))
        #set ($browseDocumentReference = $services.model.createDocumentReference($services.wiki.mainWikiId, 'WikiManager', 'WebHome'))
        #set ($backUrl = $xwiki.getURL($browseDocumentReference))
        #if("$!form_token" != '')

          {{warning}}
           {{translation key="platform.wiki.csrf.error" /}}
          {{/warning}}

        #end
        {{box}}
          $services.localization.render('platform.wiki.users.leave.confirmation', [$wikiMainPageLinkStart, $wikiName, $wikiMainPageLinkEnd])
          ((({{html}}
            <form action="$doc.getURL()" method="post">
              <fieldset>
                <input type="hidden" name="wikiId" value="$!escapetool.xml($wikiId)" />
                <input type="hidden" name="form_token" value="$!escapetool.xml($services.csrf.getToken())" />
                <span class="buttonwrapper"><button class="button">$services.localization.render('platform.wiki.users.leave.confirmation.yes')</button> <a class="button" href="$backUrl">$services.localization.render('platform.wiki.users.leave.confirmation.no')</a></span>
              </fieldset>
            </form>
          {{/html}})))
        {{/box}}
      #else
        #set ($result = $services.wiki.user.leave($currentUser, $wikiId))
        #if ($result)
          {{success}}$services.localization.render('platform.wiki.users.leave.success', ['[[', $currentUser, ">>$currentUser]]", $wikiMainPageLinkStart, $wikiName, $wikiMainPageLinkEnd]){{/success}}
        #else
          #printException($services.wiki.user.lastError.message)
        #end
      #end
    #end
  #end
#end
{{/velocity}}
