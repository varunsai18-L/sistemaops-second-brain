---
id: xwiki-JobMacro.JobProgressMacro
type: XWiki Page
space: "JobMacro"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907400000
sync_date: 2026-08-25 21:14:22
tags:
  - xwiki/documentation
  - space/jobmacro
---
# Job Progress Macro

- **Space:** JobMacro
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907400000
- **Source:** [Job Progress Macro](https://wiki.systemaops.in/bin/view/JobMacro/JobMacro.JobProgressMacro)

---

{{template name="job_macros.vm"/}}

{{velocity output="false"}}
#macro(jobMessage $jobStatus)
  #set($finished = $jobStatus.state.name() == 'FINISHED')
  #if ($finished)
    #if ($jobStatus.log.getLogs('ERROR').isEmpty())
       <div class="box successmessage">
         $services.localization.render('jobmacro.log.message.success')
       </div>
    #else
       <div class="box errormessage">
         $services.localization.render('jobmacro.log.message.errors')
       </div>
    #end
  #end
#end
{{/velocity}}

{{velocity wiki="false"}}
#if ($xcontext.action == 'get')
  #set($jobStatus = $services.job.getJobStatus($request.jobid.split('/')))
  #getJobStatusJSON($jobStatus $json)
  #set ($json.message = "#jobMessage($jobStatus)")
  $response.setContentType('application/json')
  $jsontool.serialize($json)
#end
{{/velocity}}

{{velocity}}
#if ($xcontext.action != 'get')
{{info}}This is a helper macro for displaying log progress used by the Job Macro.{{/info}}
#end
{{/velocity}}

