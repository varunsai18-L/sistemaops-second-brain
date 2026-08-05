---
id: xwiki-xwiki:XWiki.XWikiUserProfileSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906350000
sync_date: 2026-07-21 11:01:40
tags:
  - xwiki/documentation
  - space/xwiki
---
# XWikiUserProfileSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906350000
- **Source:** [XWikiUserProfileSheet](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.XWikiUserProfileSheet)

---

{{velocity}}
#if ($hasAdmin && "$!request.userId" != "" && ($request.action == "disable" || $request.action == "enable") && $services.csrf.isTokenValid($request.csrf))
#set ($user = $xwiki.getUser($request.userId))
## TODO: User#getUser() requires Programming Rights. To be fixed, see https://jira.xwiki.org/browse/XWIKI-21238
#set ($isCurrentUser = $user.getUser().userReference.equals($xcontext.userReference))
#if (!$isCurrentUser && $user.getUser().exists($xcontext.context))
  #set ($disabled = ($request.action == "disable"))
  #set ($discard = $user.setDisabledStatus($disabled))
  #set ($success = ($disabled && $user.isDisabled()) || (!$disabled && !$user.isDisabled()))
#else
  #set ($success = false)
#end
#jsonResponse({
    'success': $success
  })
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
