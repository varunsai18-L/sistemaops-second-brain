---
id: xwiki-xwiki:WikiManager.WikiCreationJobStatusService
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906683000
sync_date: 2026-07-21 11:02:13
tags:
  - xwiki/documentation
  - space/wikimanager
---
# WikiCreationJobStatusService

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906683000
- **Source:** [WikiCreationJobStatusService](https://wiki.systemaops.in/bin/view/WikiManager/xwiki:WikiManager.WikiCreationJobStatusService)

---

{{velocity}}
#if($xcontext.action == 'get' && "$!{request.outputSyntax}" == 'plain')
  #set($wikiId = $request.wikiId)
  #set($status = $services.wiki.creationjob.getJobStatus($wikiId))
  #set($lastError = $status.logTail.getLastLogEvent('ERROR'))
  #set($hasErrorLog = false)
  #if ($lastError)
    #set($hasErrorLog = true)
  #end
  #set($errorMessage = "")
  #if ($status.error)
    ## The last error log is what actually stopped the job
    #set($errorMessage = $lastError.getFormattedMessage())
  #end
  ## Log
  #template('logging_macros.vm')
  #template('extension.vm')
  ## Hack to be able to use macros from extension.vm that are supposed to be used inside Extension Manager
  #set ($olddoc = $doc)
  #set ($doc = $xwiki.getDocument('XWiki.AddExtensions'))
  ## Note: it's important for the state to be the same when calling `printLogs` and for the `status` field of $map,
  ## otherwise if the state is changed to FINISHED while `printLogs` is called, a spinner will be displayed on the last
  ## item, even tough the job is finished.
  #set ($state = $status.state)
  #set ($loading = $state != 'FINISHED')
  #set ($logs = "#printLogs($status.logTail $loading)")
  #set ($doc = $olddoc)
  #set ($map = {
    'wikiId': $wikiId,
    'progress': $status.progress.offset,
    'status': $state,
    'error': $errorMessage, 
    'hasErrorLog': $hasErrorLog,
    'logs': $logs
  })
  #jsonResponse($map)
#end
{{/velocity}}
