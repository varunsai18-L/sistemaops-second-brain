---
id: xwiki-xwiki:Help.Applications.Movies.Code.MoviesSheet
type: XWiki Page
space: "Help.Applications.Movies.Code"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781909447000
sync_date: 2026-07-21 11:03:23
tags:
  - xwiki/documentation
  - space/help.applications.movies.code
---
# MoviesSheet

- **Space:** Help.Applications.Movies.Code
- **Author:** XWiki.superadmin
- **Last Modified:** 1781909447000
- **Source:** [MoviesSheet](https://wiki.systemaops.in/bin/view/Help.Applications.Movies.Code/xwiki:Help.Applications.Movies.Code.MoviesSheet)

---

{{velocity}}
{{html wiki="true"}}
#set ($discard = $doc.use('Help.Applications.Movies.Code.MoviesClass'))
(% class="xform" %)
(((
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_title1"#end>$escapetool.xml($doc.displayPrettyName('title1', false, false))</label>
  : $doc.display('title1')
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_longText1"#end>$escapetool.xml($doc.displayPrettyName('longText1', false, false))</label>
  : $doc.display('longText1')
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_staticList1"#end>$escapetool.xml($doc.displayPrettyName('staticList1', false, false))</label>
  : $doc.display('staticList1')
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_date1"#end>$escapetool.xml($doc.displayPrettyName('date1', false, false))</label>
  : $doc.display('date1')
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_number1"#end>$escapetool.xml($doc.displayPrettyName('number1', false, false))</label>
  : $doc.display('number1')
  #if ($context.display == 'edit')
    ; <label for="Help.Applications.Movies.Code.MoviesClass_0_boolean1">$doc.display('boolean1')$escapetool.xml($doc.displayPrettyName('boolean1', false, false))</label>
  #else
    ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_boolean1"#end>$escapetool.xml($doc.displayPrettyName('boolean1', false, false))</label>
    : $doc.display('boolean1')
  #end
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_databaseList1"#end>$escapetool.xml($doc.displayPrettyName('databaseList1', false, false))</label>
  : $doc.display('databaseList1')
  ; <label#if ($xcontext.action == 'edit') for="Help.Applications.Movies.Code.MoviesClass_0_content1"#end>$escapetool.xml($doc.displayPrettyName('content1', false, false))</label>
  : $doc.display('content1')
)))
{{/html}}
{{/velocity}}
