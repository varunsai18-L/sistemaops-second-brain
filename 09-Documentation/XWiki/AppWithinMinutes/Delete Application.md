---
id: xwiki-AppWithinMinutes.DeleteApplication
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906793000
sync_date: 2026-08-16 19:45:30
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# Delete Application

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906793000
- **Source:** [Delete Application](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.DeleteApplication)

---

{{velocity output="false"}}
#**
 * Retrieve the list of pages that contain application data.
 *#
#macro (getApplicationDataPages $classReference $pageReferences)
  #set ($statement = ', BaseObject as obj where doc.fullName = obj.name and ' +
    'obj.className = :class and doc.fullName <> :template')
  #set ($query = $services.query.hql($statement))
  #set ($classLocalReference = $services.model.serialize($classReference, 'local'))
  #set ($discard = $query.bindValue('class', $classLocalReference))
  #set ($discard = $query.bindValue('template', "$stringtool.removeEnd($classLocalReference, 'Class')Template"))
  #foreach ($entryLocalReference in $query.execute())
    #set ($discard = $pageReferences.add($services.model.resolveDocument($entryLocalReference)))
  #end
#end

#**
 * Retrieve the list of pages that contain application code.
 *#
#macro (getApplicationCodePages $appReference $classReference $pageReferences)
  #set ($discard = $pageReferences.add($appReference))
  #if (!$classReference.hasParent($appReference))
    ## The code pages are outside of the application page tree.
    #set ($discard = $pageReferences.add($classReference.parent))
  #end
#end

#macro (bulkDelete $entities)
  #set ($errorLog = $NULL)
  #set ($deleteJob = $services.refactoring.delete($entities))
  #try()
    #set ($discard = $deleteJob.join())
    #set ($deleteJobStatus = $services.job.getJobStatus($deleteJob.request.id))
    #set ($errorLog = $deleteJobStatus.logTail.getFirstLogEvent('ERROR'))
  #end
#end

#macro (askForDeleteConfirmation $appReference $scope)
  ## Confirmation dialog
  #set ($appTitle = $xwiki.getDocument($appReference).plainTitle)
  #if ($scope == 'entries')
    #set ($confirmationMessage = $services.localization.render(
      'platform.appwithinminutes.deleteAppEntriesConfirmation', [$escapetool.xml($appTitle)]))
  #else
    #set ($confirmationMessage = $services.localization.render('platform.appwithinminutes.deleteAppConfirmation',
      [$escapetool.xml($appTitle)]))
  #end
  #set ($cancelURL = $doc.getURL())
  #set ($confirmParams = {
    'appName': $services.model.serialize($appReference, 'local'),
    'resolve': true,
    'scope': $scope,
    'confirm': 1,
    'form_token': $services.csrf.token
  })
  #if ("$!request.xredirect" != '')
    #getSanitizedURLAttributeValue('a','href',$request.xredirect,$doc.getURL(),$cancelURL)
    ## We don't sanitize those parameters as the sanitation will be handled server side.
    #set ($confirmParams.xredirect = $request.xredirect)
  #end
  #set ($confirmURL = $doc.getURL($xcontext.action, $escapetool.url($confirmParams)))
  {{html}}
  #xwikimessagebox($services.localization.render('core.delete') $confirmationMessage $confirmURL
    $escapetool.xml($cancelURL) $services.localization.render('yes') $services.localization.render('no'))
  {{/html}}
#end
{{/velocity}}

{{velocity}}
#if ("$!request.appName" != '')
  #set ($displayDocExtra = false)
  #if ($request.resolve == 'true')
    #set ($appReference = $services.model.resolveSpace($request.appName))
  #else
    #set ($appReference = $services.model.createSpaceReference($request.appName,
      $doc.documentReference.wikiReference))
  #end
  #set ($appHomeReference = $services.model.resolveDocument('', 'default', $appReference))
  #set ($scope = $request.scope)
  ## Make sure a valid application name has been passed, otherwise stop here.
  #set ($appDescriptor = $xwiki.getDocument($appReference).getObject('AppWithinMinutes.LiveTableClass'))
  #if ($appDescriptor)
    #if ($request.confirm == '1')
      ## CSRF protection.
      #if(!$services.csrf.isTokenValid($request.form_token))
        $response.sendRedirect($services.csrf.getResubmissionURL())
        #stop
      #end
      ##
      #set ($classLocalReference = $appDescriptor.getValue('class'))
      #set ($classReference = $services.model.resolveDocument($classLocalReference, 'explicit', $appHomeReference))
      ##
      #set ($pageReferences = [])
      #getApplicationDataPages($classReference $pageReferences)
      #if ($scope != 'entries')
        #getApplicationCodePages($appReference $classReference $pageReferences)
      #end
      #bulkDelete($pageReferences)
      ##
      #if ($errorLog)
        {{error}}$errorLog{{/error}}
      #elseif ($request.xredirect)
        ## If requested, redirect the UI after the work is complete.
        $response.sendRedirect($request.xredirect)
      #end
    #else
      #askForDeleteConfirmation($appReference $scope)
    #end
  #else
    ## Unusable application name.
    #if (!$xwiki.exists($appHomeReference))
      {{error}}$services.localization.render('platform.appwithinminutes.deleteAppDoesNotExistError'){{/error}}
    #else
      {{error}}$services.localization.render('platform.appwithinminutes.deleteAppInvalidAppError'){{/error}}
    #end
  #end
#else
  {{error}}$services.localization.render('platform.appwithinminutes.deleteAppNotSpecifiedError'){{/error}}
#end
{{/velocity}}

