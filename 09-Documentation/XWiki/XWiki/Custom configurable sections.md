---
id: xwiki-xwiki:XWiki.ConfigurableClass
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905873000
sync_date: 2026-07-21 11:01:15
tags:
  - xwiki/documentation
  - space/xwiki
---
# Custom configurable sections

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905873000
- **Source:** [Custom configurable sections](https://wiki.systemaops.in/bin/view/XWiki/xwiki:XWiki.ConfigurableClass)

---

{{include reference="XWiki.ConfigurableClassMacros" /}}

{{velocity}}
#*
 * This part takes the configuration from any documents containing XWiki.ConfigurableClass objects and creates a form
 * for each. To includeForm this document, you may specify:
 *
 * $section - String - The section which we are administrating eg: "Registration", "Users", or "Import".
 *                     If none is specified then it checks for a request parameter called "section" and uses that,
 *                     if no parameter, then this code assumes that it is part of the admin icons sheet and adds icons
 *                     for any section which is not in $sections, in that event, this code assumes it is being run
 *                     inside of a <ul> block.
 *
 * $sections - List<String> - If section is not specified, any sections on this list will not have icons made for them,
 *                            the assumption being that the icons are already there. If section is specified then this
 *                            is not taken into account and may safely be undefined.
 *
 * $currentDoc - String (document.fullName) - The administration document, users who don't have permission to edit
 *                                            it will not be able to include applications (possibly injecting
 *                                            arbitrary code.) if none specified then $doc.getFullName() is used.
 *
 * $globaladmin - boolean - If set true then we will assume we are administrationg the entire wiki.
 *                          If not set then we look for a request parameter called "editor" if that exists and equals
 *                          "globaladmin" then $globaladmin is true, if it doesn't exist then we check to see if
 *                          $currentDoc.getFullName() equals "XWiki.XWikiPreferences".
 *###
##
## Form submission depends on this.
$xwiki.jsfx.use('js/xwiki/actionbuttons/actionButtons.js', true)
## In case of conflict issue we want to display the diff properly
#set ($discard = $xwiki.ssfx.use('uicomponents/viewers/diff.css', true))
#set ($discard = $xwiki.jsfx.use('uicomponents/viewers/diff.js'))
##
#if(!$section)
  #set($section = $request.getParameter('section'))
#end
#if(!$currentDoc)
  #set($currentDoc = $doc.getFullName())
#end
## Get value of $globaladmin if not specified.
#if("$!globaladmin" == '')
  #if($editor != 'globaladmin'
      && $request.getParameter('editor') != 'globaladmin'
      && $currentDoc != 'XWiki.XWikiPreferences')
  ##
    #set($globaladmin = false)
  #else
    #set($globaladmin = true)
  #end
#end
#set($currentSpace = $xwiki.getDocument($currentDoc).getSpace())
##
##------------------------------------------------------------------------------------------------------------
## If $section exists then we are viewing the admin page for a particular section.
## eg: 'Registration', 'Presentation', 'Import' etc.
##------------------------------------------------------------------------------------------------------------
##
#if($section && $section != '')
  ##
  ## This is for keeping track of whether we have shown the heading yet or not.
  ## If the heading doesn't need to be shown, but an error occurs in processing, then we show the heading
  ## so that the user knows what the error relates to.
  #set($headingShowing = false)
  ##
  ## Searches the database for names of apps to be configured
  #set($outputList = [])
  #findNamesOfAppsToConfigure($section, $globaladmin, $xwiki.getDocument($currentDoc).getSpace(), $outputList)
  ##
  #foreach($appName in $outputList)
    ##
    ## Make sure the current user has permission to edit the configurable application.
    ## Unless we are in the page administration which is never about modifying the application configuration page
    #set($userHasAccessToDocument = $level == '.page' || $xcontext.hasAccessLevel('edit', $appName))
    ##
    ## If the document was not last saved by a user with edit privilege on this page
    ## then we can't safely display the page but we should warn the viewer.
    #if($userHasAccessToDocument)
      ## Get the configurable application
      #set($app = $xwiki.getDocument($appName))
      ##
      #set($documentSavedByAuthorizedUser = false)
      #checkDocumentSavedByAuthorizedUser($app, $currentDoc, $documentSavedByAuthorizedUser)
    #end
    ##
    ## There is no need to display a heading unless:
    ## 1. There was already a section before this document.
    ## 2. This is not the first document in this section.
    ##
    ## If we are displaying the heading and there is an error to be shown Javascript will not strip the heading.
    #if(!$appName.equals($outputList.get(0)) || $sections.contains($section))
      ## Create a document heading.
      #showHeading($appName, $headingShowing)
    #end
    ##
    #if(!$userHasAccessToDocument)
      #showHeading($appName, $headingShowing)

      {{error}}{{translation key="xe.admin.configurable.noPermissionThisApplication"/}}{{/error}}

    #elseif(!$documentSavedByAuthorizedUser)
      #showHeading($appName, $headingShowing)

      {{error}}{{translation key="xe.admin.configurable.applicationAuthorNoAdmin" parameters="$app.Author"/}}{{/error}}

    ##
    ##------------------------------------------------------------------------------------------------------------
    ## If the document is locked and not by the current user and forceEdit is not set true,
    #elseif($app.getLocked() && $app.getLockingUser() != $xcontext.getUser() && !$request.getParameter('forceEdit'))
      #set($requestURL = "$request.getRequestURL()")
      #if($requestURL.indexOf('?') == -1)
        #set($requestURL = "${requestURL}?$request.queryString")
      #end
      #showHeading($appName, $headingShowing)

      {{error}}{{translation key="doclockedby"/}} $app.getLockingUser() [[{{translation key="forcelock"/}}>>${requestURL}&forceEdit=1]]{{/error}}

    #else
      ## If the document is not already locked, attempt to acquire the lock.
      #if(!$app.getLocked())

        {{html wiki=true}}
          <noscript>

            {{warning}}{{translation key="xe.admin.configurable.cannotLockNoJavascript"/}}{{/warning}}

          </noscript>
        {{/html}}

        {{html clean=false}}
          <script>
            document.observe("xwiki:dom:loaded", function() {
              XWiki.DocumentLock && new XWiki.DocumentLock('$escapetool.javascript($app.prefixedFullName)').lock();
            });
          </script>
        {{/html}}
      #end
      ##------------------------------------------------------------------------------------------------------------
      ## Done Locking.
      ##
      ## Get all objects of the "ConfigurableClass" from this document.
      #set($allConfigurableObjs = $app.getObjects($nameOfThisDocument))
      ## Separate out the objects which are for this section.
      #set($configurableObjs = [])
      #foreach($configurableObj in $allConfigurableObjs)
        #if($app.getValue('displayInSection', $configurableObj) == $section)
          #set($discard = $configurableObjs.add($configurableObj))
        #end
      #end
      #if($configurableObjs.size() == 0)
        ## Internal error, not translated.
        #showHeading($appName, $headingShowing)

        {{error}}Internal error: All objects were filtered out for application:
        $services.rendering.escape($appName, 'xwiki/2.1').{{/error}}

      #else
        #set($formAction = $xwiki.getURL($app.getFullName(), 'save'))
        #set($formId = "${section.toLowerCase()}_${app.getFullName()}")
        #set($escapedAppName = $escapetool.xml($app.getFullName()))
        #foreach($configurableObj in $configurableObjs)
          #set ($heading = $app.getValue('heading', $configurableObj))
          #set ($codeToExecute = "$!app.getValue('codeToExecute', $configurableObj)")
          ## If linkPrefix is set, then we will make each property label a link which starts with that prefix.
          #set ($linkPrefix = "$!app.getValue('linkPrefix', $configurableObj)")
          #if (!$app.restricted)
            #set ($evaluatedConfigurableObj = $configurableObj.evaluate())
            #set ($heading = $evaluatedConfigurableObj.heading)
            #set ($linkPrefix = $evaluatedConfigurableObj.linkPrefix)
          #end
          ## Display the header if one exists.
          #if($heading && $heading != '')
            == $services.rendering.escape($heading, 'xwiki/2.1') ==
          #end
          ## Display code to execute
          #if ($codeToExecute != '')
            (%class="codeToExecute"%)(((##
              $configurableObj.display('codeToExecute', 'view', false)
            )))
          #end
          ##
          ## If propertiesToShow is set, then we will only show the properties contained therein.
          #set($propertiesToShow = $app.getValue('propertiesToShow', $configurableObj))
          #if(!$propertiesToShow || $propertiesToShow.getClass().getName().indexOf('List') == -1)
            #set($propertiesToShow = [])
          #end
          ##
          ## If the Configurable object specifies a configuration class, use it,
          ## otherwise assume custom forms are used instead.
          #set($configClassName = "$!app.getValue('configurationClass', $configurableObj)")
          #if($configClassName != '')
            #set($objClass = $xwiki.getDocument($configClassName).getxWikiClass())
            #if(!$objClass || $objClass.getClass().getName().indexOf('.Class') == -1)
              #showHeading($appName, $headingShowing)

              {{error}}{{translation key="xe.admin.configurable.configurationClassNonexistant"/}}{{/error}}

            #else
              ## Use the first object from the document which is of the configuration class.
              #set($obj = $app.getObject($objClass.getName()))
              ##
              #if(!$obj || $obj.getClass().getName().indexOf('.Object') == -1)
                #showHeading($appName, $headingShowing)

                {{error}}
                  #set($escapedObjClassName =
                    $services.rendering.escape($escapetool.java($objClass.getName()), 'xwiki/2.1'))
                  #set($translationEscapedAppName =
                    $services.rendering.escape($escapetool.java($app.getFullName()), 'xwiki/2.1'))
                  {{translation key="xe.admin.configurable.noObjectOfConfigurationClassFound"
                    parameters="~"$escapedObjClassName~", ~"$translationEscapedAppName~""/}}
                {{/error}}

              #else
                ##
                ## Merge save buttons, remove headings from subsections, and make information links into popups.
                ## This is not done if there is only a custom defined form.
                $xwiki.jsx.use($nameOfThisDocument)##
                ##
                ## We don't begin the form until we have content for it so that a configurable can specify a
                ## custom form in codeToExecute and if that configurable object is the first of it's kind in that
                ## document, the custom form will not be put inside of our form.
                #if(!$insideForm)
                  ## We are opening a form and fieldset without closing it, thus we cannot clean this html.

                  {{html clean=false}}
                    <form id="$formId" method="post" action="$formAction" class="xform">
                      <fieldset>
                  {{/html}}
                  #set($insideForm = true)
                #end

                {{html}}
                  $formHtml.toString()
                {{/html}}
              #end## If object exists
            #end## If class exists
          #end## If class name is specified.
        #end## Foreach configurable object found in this document
        ## If a form was started then we end it.
        #if($insideForm)

          ## This is closing an open form which was opened above, we cannot clean this html.
          {{html clean=false}}
          ## We add in a redirect field to prevent the user from being carried away when they save
          ## if they don't have javascript.
          #set($thisURL = $request.getRequestURL())
          #if($request.getQueryString() && $request.getQueryString().length() > 0)
            #set($thisURL = "${thisURL}?$request.getQueryString()")
          #end
          <input type="hidden" id="${escapedAppName}_redirect" name="$redirectParameter" value="$escapetool.xml($thisURL)" />
          <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
          </fieldset>
          <div class="bottombuttons">
            <p class="admin-buttons">
              <span class="buttonwrapper">
                ## Text to display on the button. If there is a heading then this button should be labeled
                ## that it is for saving this section. Otherwise it should be a generic "save" button.
                #if($headingShowing)
                  #set($buttonText = "$services.localization.render('admin.save') $escapedAppName")
                #else
                  #set($buttonText = "$services.localization.render('admin.save')")
                #end
                <input class="button" type="submit" name="action_saveandcontinue" value="$buttonText" />
              </span>
            </p>
          </div> ## bottombuttons
          </form>
          #set($insideForm = false)
          {{/html}}
        #end
      #end## If there are configurable objects
    #end## If document is not locked or forceEdit is enabled
  #end## Foreach document name in names to configure

  {{html}}
  <script>
  /* <![CDATA[ */
  ## Alt+Shift+S presses the first saveAndContinue button it finds, not what we want so we will disable edit shortcuts.
  document.observe('xwiki:dom:loaded', function() {
    XWiki.actionButtons.EditActions = Object.extend(XWiki.actionButtons.EditActions, {addShortcuts : function() { }});
  });
  //]]>
  </script>
  {{/html}}##
  ##
#elseif ($currentDoc != 'XWiki.ConfigurableClass')
  ##
  ##------------------------------------------------------------------------------------------------------------
  ## If section is not set then we are viewing the main administration page.
  ##------------------------------------------------------------------------------------------------------------
  ##
  ## If there is no list called sections then we set sections to an empty list.
  #if(!$sections || $sections.getClass().getName().indexOf('List') == -1)
    #set($sections = [])
  #end
  ##
  ## We have to create a list of documents which the current user doesn't have permission to view.
  ## So we can add an error message to the bottom of the page if there are any.
  #set($appsUserCannotView = [])
  ##
  ## A list of sections (to be added) which the user is not allowed to edit, icons will be displayed with a message
  #set($sectionsUserCannotEdit = [])
  ## List of sections to be added, in order by creationDate of oldest contained application.
  #set($sectionsToAdd = [])
  ## Map of URL of icon to use by the name of the section to use that icon on.
  #set($iconBySection = {})
  ##
  #set($outputList = [])
  #findNamesOfAppsToConfigure("", $globaladmin, $currentSpace, $outputList)
  ##
  #foreach($appName in $outputList)
    ##
    ## Get the configurable application
    #set($app = $xwiki.getDocument($appName))
    ##
    ## If getDocument returns null, then warn the user that they don't have view access to that application.
    #if(!$app)
      #set($discard = $appsUserCannotView.add($appName))
    #end
    ##
    #set($configurableObjects = $app.getObjects($nameOfThisDocument))
    #foreach($configurableObject in $configurableObjects)
      #set($displayInSection = $app.getValue('displayInSection', $configurableObject))
      ##
      ## If there is no section for this configurable or if the section cannot be edited, then check if the
      ## application can be edited by the current user, if so then we display the icon from the current app and
      ## don't display any message to tell the user they can't edit that section.
      #if(!$sections.contains($displayInSection) || $sectionsUserCannotEdit.contains($displayInSection))
        ##
        ## If there is no section for this configurable, then we will have to add one.
        #if(!$sections.contains($displayInSection) && !$sectionsToAdd.contains($displayInSection))
          #set($discard = $sectionsToAdd.add($displayInSection))
        #end
        ##
        ## If an attachment by the filename iconAttachment exists and is an image
        #set($attachment = $app.getAttachment("$app.getValue('iconAttachment', $configurableObject)"))
        #if($attachment && $attachment.isImage())
          ## Set the icon for this section as the attachment URL.
          #set($discard = $iconBySection.put($displayInSection, $app.getAttachmentURL($attachment.getFilename())))
        #end
        ##
        ## If the user doesn't have edit access to the application, we want to show a message on the icon
        #if(!$xcontext.hasAccessLevel("edit", $app.getFullName()))
          #if(!$sectionsUserCannotEdit.contains($displayInSection))
            #set($discard = $sectionsUserCannotEdit.add($displayInSection))
          #end
        #elseif($sectionsUserCannotEdit.contains($displayInSection))
          ## If the user didn't have access to the section before but does have access to _this_ app which is
          ## configured in the section, then the section becomes accessible.
          #set($discard = $sectionsUserCannotEdit.remove($displayInSection))
        #end
      #end## If section doesn't exist or user doesn't have access.
    #end## Foreach configurable object in this app.
  #end## Foreach application which is configurable.
  ##
  ## Now we go through sectionsToAdd and generate icons for them
  #set($defaultIcon = $xwiki.getAttachmentURL($nameOfThisDocument, 'DefaultAdminSectionIcon.png'))
  #if($globaladmin)
    #set($queryString = "editor=globaladmin&amp;section=")
  #else
    #set($queryString = "space=$escapetool.url($currentSpace)&amp;section=")
    #if($request.getParameter('editor'))
      #set($queryString = "editor=$escapetool.url($request.getParameter('editor'))&amp;$queryString")
    #end
  #end

  ## This is an html fragment and thus cannot be cleaned
  {{html clean=false}}
  #foreach($sectionToAdd in $sectionsToAdd)
    #set($icon = $iconBySection.get($sectionToAdd))
    #if(!$icon)
      #set($icon = $defaultIcon)
    #end
    <li class="$escapetool.xml($sectionToAdd).replaceAll(' ', '_')">
      #set($hasAccess = !$sectionsUserCannotEdit.contains($sectionToAdd))
      #if($hasAccess)
        <a href="$xwiki.getURL($currentDoc, $xcontext.getAction(), "$queryString$escapetool.url($sectionToAdd)")">
      #else
        <a title="$services.localization.render('xe.admin.configurable.sectionIconNoAccessTooltip')">
      #end
      <span>
      <img src="$icon" alt="$escapetool.xml($sectionToAdd) icon"/>
      ## Try to translate the names of the sections, build the key by adding an "admin." in front.
      ## Not the best way to translate, but very inline with the way the translations are done in XWiki.AdminSheet for individual administration page titles.
      ## If there is no translation (translated message is equals to key), don't display the message key, but the section name instead.
      #if($services.localization.get("admin.${sectionToAdd.toLowerCase()}"))
        #set($sectionDisplayName = $services.localization.render("admin.${sectionToAdd.toLowerCase()}"))
      #else
        #set($sectionDisplayName = $sectionToAdd)
      #end
      $escapetool.xml($sectionDisplayName)
      </span>
      #if(!$hasAccess)
        <br/>#inlineError($services.localization.render('xe.admin.configurable.sectionIconNoAccess'))
      #end
      </a>
    </li>
  #end
  {{/html}}

  ## Finally we display an error message if there are any applications which we were unable to view.
  #if($appsUserCannotView.size() > 0)
    {{error}}$services.localization.render('xe.admin.configurable.noViewAccessSomeApplications',
      'xwiki/2.1', [$appsUserCannotView]){{/error}}

  #end
#end## If we should be looking at the main administration page.
{{/velocity}}
