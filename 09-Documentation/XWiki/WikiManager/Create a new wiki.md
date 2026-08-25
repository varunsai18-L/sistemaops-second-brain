---
id: xwiki-WikiManager.CreateWiki
type: XWiki Page
space: "WikiManager"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906645000
sync_date: 2026-08-25 21:13:33
tags:
  - xwiki/documentation
  - space/wikimanager
---
# Create a new wiki

- **Space:** WikiManager
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906645000
- **Source:** [Create a new wiki](https://wiki.systemaops.in/bin/view/WikiManager/WikiManager.CreateWiki)

---

{{velocity}}
#######################################################
##         Create a new (sub)wiki - WIZARD
##
## This wizard let user create a new wiki.
## The 'controller' macro call the good submacro
## depending on the step
##
#######################################################
#########################
## STYLE
#########################
#set($docextras = {})
#########################
## PLUGINS DEPENDENCIES
#########################

## If all dependencies are OK, we call the controller
#if ($services.wiki && $services.wiki.creationjob)
  #controller()
#else
  {{error}}{{translation key="platform.wiki.dependencies.wiki.missing"/}}{{/error}}
#end

##################################
##         CONTROLLER
##################################
#macro(controller)
  #if($request.step == 'members')
    #stepMembers()
  #elseif($request.step == 'create')
    #create()
  #elseif($request.step == 'cleanUp')
    #cleanUp()
  #elseif($request.step == 'finalize')
    #finalize()
  #else
    ## Default step
    #stepType()
  #end
#end
##################################
##           HEADER
##
## Display the wizard header
##################################
#macro(wizardHeader $title $currentStepNumber)
  ## Display a step name in the header
  #macro(wizardHeaderStep $name $number $currentStepNumber)
    <li><span class="btn btn-xs number #if($currentStepNumber==$number)step-active#end">$number</span> <span class="name #if($currentStepNumber==$number)step-active#end">$name</span></li>
  #end

  <div class="wizard-header">
    <h1><span>$title</span></h1>
    #if($currentStepNumber)
      <ul class="steps">
        #wizardHeaderStep($services.localization.render('platform.wiki.create.wizard.step.nameAndType.shortname'), 1, $currentStepNumber)
        #wizardHeaderStep($services.localization.render('platform.wiki.create.wizard.step.users.shortname'), 2, $currentStepNumber)
      </ul>
    #end
    <div class="clearfloats"></div>
  </div>

#end
##################################
##           FOOTER
##
## Display the wizard footer
##################################
#macro(wizardFooter $prev $next $create $finalize $finalizeHidden $cleanUp $cleanupHidden)
  <div class="wizard-footer buttons">
    #if("$!prev" !='')
      <span class="buttonwrapper left">
        <button value="$prev" title="$services.localization.render('platform.wiki.create.wizard.step.previous')" name="step" id="wizard-previous" class="button secondary">$services.localization.render('platform.wiki.create.wizard.step.previous')</button>
      </span>
    #end
    #if("$!next" !='')
      <span class="buttonwrapper">
        <button value="$next" title="$services.localization.render('platform.wiki.create.wizard.step.next')" name="step" id="wizard-next" class="button">$services.localization.render('platform.wiki.create.wizard.step.next')</button>
      </span>
    #end
    #if("$!create" !='')
      <span class="buttonwrapper">
        <button value="$create" title="$services.localization.render('platform.wiki.create.wizard.step.create')" name="step" id="wizard-create" class="button">$services.localization.render('platform.wiki.create.wizard.step.create')</button>
      </span>
    #end
    #if("$!finalize" != '')
      <span class="buttonwrapper">
        <button value="finalize" title="$services.localization.render('platform.wiki.create.wizard.step.creation.go')" name="step" id="finalize" class="button #if($finalizeHidden)hidden#end">$services.localization.render('platform.wiki.create.wizard.step.creation.go')</button>
      </span>
    #end
    #if("$!cleanUp" != '')
      <span class="buttonwrapper">
        <button value="cleanUp" title="$services.localization.render('platform.wiki.create.wizard.step.provisioning.cleanUp')" name="step" id="cleanUp" class="button #if($cleanupHidden)hidden#end">$services.localization.render('platform.wiki.create.wizard.step.provisioning.cleanUp')</button>
      </span>
    #end
  </div>
#end
##################################
##           REQUIRED
##
## Add a required message
##################################
#macro(required)<span class='xRequired'>($services.localization.render('platform.wiki.form.requiredField'))</span>#end
##################################
##        TEMPLATE FIELDS
##
## Display the 'template' fields
##################################
#macro(displayTemplateFields $templates)
  #if ($templates.size() > 0)
    <select name="template" id="template">
      <option value="xwikinotemplate">$services.localization.render('platform.wiki.create.wizard.template.noTemplate')</option>
      #foreach ($template in $templates)
        #set ($name = $template.id)
        #if ($stringtool.isNotBlank("$!template.prettyName"))
          #set($name = "${template.prettyName} (${name})")
        #end
        #set($selected = '')
        #if($request.template == $template.id)
          #set($selected = 'selected="selected"')
        #end
        <option value="${template.id}" $selected>$name</option>
      #end
    </select>
  #end
  <div class="xformInline">
    #set ($isTemplate = '')
    #if ("$!request.set_as_template" != '')
      #set ($isTemplate = 'checked="checked"')
    #end
    <input type="checkbox" name="set_as_template" id="set_as_template" $isTemplate/>
    <label for="set_as_template" id="label_set_as_template">$services.localization.render('platform.wiki.create.wizard.setAsTemplate.label')</label>
  </div>
#end
##################################
##          STEP TYPE
##
## The type is the first step on the creation
##################################
#macro(stepType)
  #set($discard = $xwiki.ssfx.use('uicomponents/wizard/wizard.css', true))
  {{html}}
    <form class="xform" method="post" action="$doc.getURL()">
      #wizardHeader($services.localization.render('platform.wiki.create.wizard.step.nameAndType'), 1)
      ### WIZARD BODY ###
      <div class="wizard-body">
        ### SECOND STEP VALUES
        <input type="hidden" name="ownerId" value="$!escapetool.xml($request.getParameter('ownerId'))" />
        <input type="hidden" name="membershipType" value="$!escapetool.xml($request.getParameter('membershipType'))" />
        <input type="hidden" name="userScope" value="$!escapetool.xml($request.userScope)" />
        #addMembersAsHiddenInput()
        ### WIZARD FIRST HALF ###
        <div class="half">
          ### PRETTY NAME ###
          <dl>
            <dt>
              <label for="prettyname">$services.localization.render('platform.wiki.prop.wikiprettyname')#required()</label>
              <span class="xHint">$services.localization.render('platform.wiki.create.wizard.desc.wikiprettyname')</span>
              <span id="wikiprettynamevalidation" class="xErrorMsg"></span>
            </dt>
            <dd>
              <input size="60" id="prettyname" name="wikiprettyname" type="text" value="$!escapetool.xml($request.getParameter('wikiprettyname'))"/>
            </dd>
          </dl>
          ### WIKI NAME ###
          <dl>
            <dt>
              <label for="wikiname">$services.localization.render('platform.wiki.prop.wikiname')#required()</label>
              <span class='xHint'>$services.localization.render('platform.wiki.create.wizard.desc.wikiname')</span>
            </dt>
            <dd>
              <input size="60" id="wikiname" name="wikiname" type="text"  value="$!escapetool.xml($request.wikiname)"/>
              <span id="wikinamevalidation" class="xErrorMsg"></span>
            </dd>
          </dl>
          ### WIKI ALIAS ###
          #if(!$services.wiki.isPathMode())
            <dl>
              <dt>
                <label for="wikialias">$services.localization.render('platform.wiki.prop.wikialias')#required()</label>
                <span class='xHint'>$services.localization.render('platform.wiki.create.wizard.desc.wikialias')</span>
              </dt>
              <dd>
                <input size="60" id="wikialias" name="wikialias" type="text"  value="$!escapetool.xml($request.wikialias)"/>
              </dd>
            </dl>
          #end
          ### DESCRIPTION ###
            <dl>
              <dt>
                <label for="description">$services.localization.render('platform.wiki.prop.description')</label>
                <span class="xHint">$services.localization.render('platform.wiki.create.wizard.desc.description')</span>
              </dt>
              <dd>
                <textarea id="description" name="description" rows="7" cols="45">$!escapetool.xml($request.getParameter('description'))</textarea>
              </dd>
            </dl>
        ### END OF WIZARD FIRST HALF
        </div>
        ### WIZARD SECOND HALF
        <div class="half">
          ### TEMPLATE / FLAVOR ###
          #set ($templates = $services.wiki.template.getTemplates())
          #if (!$services.distribution.hasWikiDefaultUIExtension())
            #template('flavor/macros.vm')
            <dl>
              <dt>
                <label>$services.localization.render('platform.wiki.create.wizard.flavortemplate.label')</label>
                <span class="xHint">$services.localization.render('platform.wiki.create.wizard.flavortemplate.hint')</span>
              </dt>
              #set ($currentTab = 'flavors')
              #if ("$!request.template" != '' && $request.template != 'xwikinotemplate')
                #set ($currentTab = 'templates')
              #end
              <dd class="flavor_template">
                <ul class="xwikitabbar">
                  <li #if($currentTab=='flavors')class="active"#end><a href="#flavors">$services.localization.render('platform.wiki.create.wizard.flavortemplate.flavorTab')</a></li>
                  <li #if($currentTab=='templates')class="active"#end><a href="#templates">$services.localization.render('platform.wiki.create.wizard.flavortemplate.templateTab')</a></li>
                </ul>
                <div class="xwiki-createwiki-tabs-content">
                  #set ($defaultFlavor = "$!request.flavor")
                  #if ($defaultFlavor == '')
                    #set ($defaultFlavor = 'noFlavor')
                  #end
                  <div class="xwiki-createwiki-tab #if($currentTab=='flavors')active#{else}hidden#end" id="flavors-tab">
                    ## TODO: reload when the target subwiki id changes
                    #displayFlavorPicker('flavor', $defaultFlavor, true, 'xwiki-createwiki-flavor-picker', true, 'wiki:subwiki')
                  </div>
                  <div class="xwiki-createwiki-tab #if($currentTab=='templates')active#{else}hidden#end" id="templates-tab">
                    #displayTemplateFields($templates)
                  </div>
                </div>
              </dd>
            </dl>
          #else
            ## There is a default UI configured, so we do not display the flavor picker
            <dl>
              <dt>
                #if ($templates.size() > 0)
                  <label for="template">$services.localization.render('platform.wiki.create.wizard.template.label')</label>
                  <span class="xHint">$services.localization.render('platform.wiki.create.wizard.desc.newTemplateHint')</span>
                #else
                  <label>$services.localization.render('platform.wiki.create.wizard.template.label')</label>
                #end
              </dt>
              <dd>
                #displayTemplateFields($templates)
              </dd>
            </dl>
          #end
        ### END OF WIZARD SECOND HALF
        </div>
      ### END OF WIZARD BODY
      </div>
      <div class="clearfloats"></div>
      #wizardFooter('', 'members', '')
    </form>
  {{/html}}
#end
##################################
##          STEP MEMBERS
##
## The members step is the lasy
##################################
#macro(stepMembers)
  #set($discard = $xwiki.ssfx.use('uicomponents/wizard/wizard.css', true))
  {{html}}
    <form class="xform" method="post" action="$doc.getURL()">
      #wizardHeader($services.localization.render('platform.wiki.create.wizard.step.users'), 2)
      ### WIZARD BODY ###
      <div class="wizard-body">
        ### FIRST STEP VALUES
        <input type="hidden" name="wikiprettyname" value="$!escapetool.xml($request.getParameter('wikiprettyname'))" />
        <input type="hidden" name="wikiname" value="$!escapetool.xml($request.wikiname)" />
        <input type="hidden" name="wikialias" value="$!escapetool.xml($request.wikialias)" />
        <input type="hidden" name="description" value="$!escapetool.xml($request.getParameter('description'))" />
        <input type="hidden" name="template" value="$!escapetool.xml($request.template)" />
        <input type="hidden" name="flavor" value="$!escapetool.xml($request.flavor)" />
        <input type="hidden" name="set_as_template" value="$!escapetool.xml($request.set_as_template)" />
        <input type="hidden" name="form_token" value="$!escapetool.xml($services.csrf.getToken())" />
        ### WIZARD FIRST HALF ###
        <div class="half">
          ### OWNER ###
          ## Make this section available only to admins, so that only admins can create wikis in the name of other users.
          #if ($hasAdmin)
            <dl>
              <dt>
                <label for="owner">$services.localization.render('platform.wiki.prop.owner') <span class="xRequired">($services.localization.render('platform.wiki.form.requiredField'))</span></label>
                <span class="xHint">$services.localization.render('platform.wiki.create.wizard.desc.owner')</span>
              </dt>
              <dd>
                #set($value = $escapetool.xml($request.getParameter('ownerId')))
                #if("$!value" == "")
                  #set($value = $escapetool.xml($xcontext.user))
                #end
                #set ($userPickerParams = {
                  'id': 'owner',
                  'name': 'ownerId',
                  'value': $value
                })
                #userPicker(false $userPickerParams)
              </dd>
            </dl>
          #else
            <input id="owner" name="ownerId" type="hidden" value="${xcontext.mainWikiName}:${xcontext.user}"/>
          #end
          ### USERS SCOPE ###
          <dl>
            <dt>
              <label for="userScope">$services.localization.render('platform.wiki.create.wizard.userScope.label')</label>
              <span class="xHint">$services.localization.render('platform.wiki.create.wizard.userScope.hint')</span>
            </dt>
            <dd>
              #set($value = $escapetool.xml($request.getParameter('userScope')))
              #set ($wikiUserClassDocument = $xwiki.getDocument('WikiManager.WikiUserClass'))
              #set ($wikiUserClass = $wikiUserClassDocument.getxWikiClass())
              #set ($userScopeProperty = $wikiUserClass.get('userScope'))
              #set ($userScopePropertyValues = '')
              #set ($userScopePropertyValues = $userScopeProperty.getListValues())
              #set ($userScopeDetailsMap = $userScopeProperty.getMapValues())
              #foreach ($userScopeValue in $userScopePropertyValues)
                #set ($userScopeValueId = "userScope_${foreach.index}")
                <div>
                <label for="$userScopeValueId">
                #set($checked = '')
                #if($request.getParameter('userScope') == $userScopeValue || ("$!request.getParameter('userScope')"=='' && $foreach.index==0))
                  #set($checked = 'checked="checked"')
                #end
                <input type="radio" id="$userScopeValueId" name="userScope" value="$userScopeValue" $checked/>
                $services.localization.render("${wikiUserClassDocument.fullName}_${userScopeProperty.name}_${userScopeDetailsMap.get($userScopeValue).getValue()}")
                </label>
                </div>
              #end
            </dd>
          </dl>
        ### END OF WIZARD FIRST HALF
        </div>
        ### WIZARD SECOND HALF
        <div class="half">
          ### MEMBERSHIP TYPE
          #set ($membershipTypeProperty = $wikiUserClass.get('membershipType'))
          #set ($membershipTypeValues = '')
          #set ($membershipTypeValues = $membershipTypeProperty.getListValues())
          #set ($membershipTypeDetailsMap = $membershipTypeProperty.getMapValues())
          <dl>
            <dt>
              <label>$services.localization.render('platform.wiki.prop.membershipType.label')</label>
              <span class='xHint'>$services.localization.render('platform.wiki.prop.membershipType.hint')</span>
            </dt>
            <dd>
            #foreach ($membershipTypeValue in $membershipTypeValues)
              #set ($membershipTypeValueId = "membershipType_${foreach.index}")
              <div>
                <label for="$membershipTypeValueId">
                  #set($checked = '')
                  #if($request.getParameter('membershipType') == $membershipTypeValue || ("$!request.getParameter('membershipType')"=='' && $foreach.index==0))
                    #set($checked = 'checked="checked"')
                  #end
                  <input type="radio" id="$membershipTypeValueId" name="membershipType" value="$membershipTypeValue" $checked/>
                  $services.localization.render("${wikiUserClassDocument.fullName}_${membershipTypeProperty.name}_${membershipTypeDetailsMap.get($membershipTypeValue).getValue()}")
                </label>
              </div>
            #end
            </dd>
          </dl>
          ### MEMBERS
          <dl>
            <dt>
              <label for="members">$services.localization.render('platform.wiki.create.members')</label>
              <span class="xHint">$services.localization.render('platform.wiki.create.wizard.desc.members')</span>
            </dt>
            <dd>
              #set ($userPickerParams = {
                'id': 'members',
                'name': 'members',
                'value': $request.getParameterValues('members')
              })
              #userPicker(true $userPickerParams)
            </dd>
          </dl>
        ### END OF WIZARD SECOND HALF
        </div>
      ### END OF WIZARD BODY
      </div>
      <div class="clearfloats"></div>
      #wizardFooter('type', '', 'create')
    </form>
  {{/html}}
#end
##################################
##       GET REQUEST LIST
##
## Get the values for user pickers with multiple selection
##################################
#macro(getRequestList $paramlist $paramname)
  #set ($paramtable = [])
  #set ($paramtable = $request.getParameterValues($paramname))
  #if ($paramtable && $paramlist)
    #set ($ok = $paramlist.clear())
    #foreach($paramvalue in $paramtable)
      #set ($ok = $paramlist.add($paramvalue))
    #end
  #end
#end
##################################
##           CREATE
##
## The final step that eventually create the wiki
##################################
#macro(create)
  ## Job Status
  #set ($state = $services.wiki.creationjob.getJobStatus($request.wikiname).state)
  ## If a deleted wiki had the same name, the job status may still be there (with a 'FINISHED' status)
  ## So we have to check if the wiki really exists
  #if ($state == 'FINISHED' && !$services.wiki.exists($request.wikiname))
    ## If not, consider that the new job has not been launched yet
    #set($state = 'NONE')
  #end
  ## CSRF checkFailed to execute the [velocity] macro. Click on this m
  #if (!$services.csrf.isTokenValid($request.form_token))
    {{warning}}
      {{translation key="platform.wiki.csrf.error" /}}
    {{/warning}}
    
    #stepMembers()
  #elseif("$!state" != '' && $state != 'NONE')
    #creation()
  #else
    #createWiki()
  #end
#end
##################################
##         CREATE WIKI
##
## The macro that finaly starts the wiki creation job
##################################
#macro(createWiki)
  #set($wikialias = $request.wikialias)
  #if("$!wikialias" == '')
    #set($wikialias = $request.wikiname)
  #end
  #set($wikiCreationRequest = $services.wiki.creationjob.newWikiCreationRequest())
  #set($discard = $wikiCreationRequest.setWikiId($request.wikiname))
  #set($discard = $wikiCreationRequest.setAlias($wikialias))
  #set($discard = $wikiCreationRequest.setPrettyName($request.wikiprettyname))
  #set($discard = $wikiCreationRequest.setDescription($request.description))
  #if("$!request.set_as_template" != '')
    #set($discard = $wikiCreationRequest.setTemplate(true))
  #else
    #set($discard = $wikiCreationRequest.setTemplate(false))
  #end
  #set($ownerId = $request.ownerId)
  #if("$!ownerId" == '')
    ## If the ownerId is null, then set the current user
    #set($ownerId = $services.model.serialize($xcontext.userReference, 'default'))
  #else
    #set($ownerId = $services.model.serialize($services.model.resolveDocument($ownerId), 'default'))
  #end
  #set($discard = $wikiCreationRequest.setOwnerId($ownerId))
  #set($discard = $wikiCreationRequest.setUserScope($request.userScope))
  #set($discard = $wikiCreationRequest.setMembershipType($request.membershipType))
  #set($discard = $wikiCreationRequest.setFailOnExist(true))
  #if("$!request.template" != '' && $request.template != 'xwikinotemplate')
    ## Create a wiki from a template
    #set($discard = $wikiCreationRequest.setWikiSource('template'))
    #set($discard = $wikiCreationRequest.setTemplateId($request.template))
  #elseif("$!request.flavor" != '' && $request.flavor != 'noFlavor')
    ## Create a wiki from an extension
    #set($discard = $wikiCreationRequest.setWikiSource('extension'))
    #set($flavorExtension = $request.flavor.split(':::'))
    #set($discard = $wikiCreationRequest.setExtensionId($flavorExtension[0], $flavorExtension[1]))
  #elseif($services.distribution.hasWikiDefaultUIExtension())
    ## Default action when a default UI is configured for subwikis
    #set($discard = $wikiCreationRequest.setWikiSource('extension'))
    #set($discard = $wikiCreationRequest.setExtensionId($services.wiki.creationjob.defaultWikiExtensionId))
  #end
  ## Members
  #if ($request.userScope != 'local_only')
    #set ($members = [])
    #getRequestList($members 'members')
    ## Remove empty strings from the list of members (the user picker submits by default an empty string).
    #set ($discard = $members.removeAll(['']))
    #if ("$!members" != '' && $members.size() > 0)
      #set ($globalMembers = [])
      ## Enforce global users
      #foreach ($member in $members)
        #set($discard = $globalMembers.add($services.model.serialize($services.model.resolveDocument($member), 'default')))
      #end
      ## Add the members
      #set ($discard = $wikiCreationRequest.setMembers($globalMembers))
    #end
  #end
  ## Start the creation job
  #set($job = $services.wiki.creationjob.createWiki($wikiCreationRequest))
  #if (!$job)
    {{error}}$services.localization.render('platform.wiki.create.error', [$request.wikiname, $services.wiki.creationjob.lastError]){{/error}}
  #else
    #creation()
  #end
#end
##################################
##  ADD MEMBERS AS HIDDEN INPUT
##################################
#macro(addMembersAsHiddenInput)
  ### MEMBERS VALUES
  #set ($members = [])
  #getRequestList($members 'members')
  #set($membersValue = '')
  #foreach($m in $members)
    #if($m != '')
      <input type="hidden" name="members" value="$!escapetool.xml($m)" />
    #end
  #end
#end
##################################
##          CREATION
##
## This step display a progess bar during
## the wiki creation
##################################
#macro(creation)
  #set ($discard = $xwiki.ssfx.use('uicomponents/wizard/wizard.css', true))
  #set ($discard = $xwiki.ssfx.use('uicomponents/logging/logging.css', true))
  #set ($discard = $xwiki.jsfx.use('uicomponents/logging/logging.js', true))
  #set ($status = $services.wiki.creationjob.getJobStatus($request.wikiname))
  {{html clean="false"}}
    <form class="xform" method="post" action="$doc.getURL()">
    <input type="hidden" name="wikiId" id="wikiId" value="$!escapetool.xml($request.wikiname)" />
    <input type="hidden" name="csrf" id="csrf" value="$!escapetool.xml($services.csrf.getToken())" />
    #wizardHeader($services.localization.render('platform.wiki.create.wizard.step.creation'))
    <div class="wizard-body">
      #if ($status.state != 'FINISHED')
      <div class="ui-progress" id="ui-progress">
        $services.localization.render('platform.wiki.create.wizard.step.creation.wait')
        <div class="ui-progress-background">
          #set ($percent = $status.progress.offset)
          ## There is no progress information if the job was scheduled but hasn't started yet.
          #if (!$percent)
            #set ($percent = 0)
          #end
          #set ($percent = $numbertool.toNumber($mathtool.mul($percent, 100)).intValue())
          <div class="ui-progress-bar green" style="width:${percent}%" id="wikicreation-progress-bar"></div>
        </div>
      </div>
      #end
      #set($hasErrors = $status.logTail.hasLogLevel('ERROR'))
      {{/html}}
      
      {{success cssClass="successMessage #if($status.error || $state != 'FINISHED')hidden#end"}}
        {{html}}$services.localization.render('platform.wiki.create.wizard.step.creation.complete', ["<strong>$escapetool.xml($request.wikiname)</strong>"]){{/html}}
      {{/success}}
      
      {{warning cssClass="errorlogMessage #if(!$hasErrors || $state != 'FINISHED')hidden#end"}}
        {{html}}$services.localization.render('platform.wiki.create.wizard.step.creation.errorlog', ["<strong>$escapetool.xml($request.wikiname)</strong>"]){{/html}}
      {{/warning}}
      
      {{error cssClass="errorMessage #if(!$status.error || $state != 'FINISHED')hidden#end"}}
        {{html}}$services.localization.render('platform.wiki.create.wizard.step.creation.error', ["<strong>$escapetool.xml($request.wikiname)</strong>"]){{/html}}
      {{/error}}
      
      {{html clean="false"}}
    </div>
    ## Log
    #template('logging_macros.vm')
    #template('extension.vm')
    ## Hack to be able to use macros from extension.vm that are supposed to be used inside Extension Manager
    #set($olddoc = $doc)
    #set($doc = $xwiki.getDocument('XWiki.AddExtensions'))
    #set($loading = $status.state != 'FINISHED')
    <div id="creation-log">
      #printLogs($status.logTail, $loading)
    </div>
    #set($doc = $olddoc)
    #if($status.state == 'FINISHED')
      #if ($status.error)
        #set($finalizeHidden = true)
        #set($cleanUpHidden = false)
      #else
        #set($finalizeHidden = false)
        #set($cleanUpHidden = !$hasErrors)
      #end
    #else
      #set($finalizeHidden = true)
      #set($cleanUpHidden = true)
    #end
    #wizardFooter('', '', '', 'finalize', $finalizeHidden, 'cleanUp', $cleanUpHidden)
    </form>
  {{/html}}
#end
##################################
##           FINALIZE
##
## Just go the the created wiki
##################################
#macro(finalize)
  #set($wikiDescriptor = $services.wiki.getById($request.wikiId))
  $response.sendRedirect($xwiki.getURL($wikiDescriptor.mainPageReference))
#end
##################################
##           CLEAN UP
##
## Delete the wiki if errors has occured
##################################
#macro(cleanUp)
  #set($discard = $xwiki.ssfx.use('uicomponents/wizard/wizard.css', true))
  #if("$!request.deleteOk" == '')
    #if ($services.csrf.isTokenValid($request.csrf))
      #set($wikiId = $request.wikiId)
      #set($ok = $services.wiki.deleteWiki($wikiId))
      $response.sendRedirect($doc.getURL('view', "step=cleanUp&deleteOk=$ok&wikiId=$wikiId"))
    #else
      {{html}}
        #wizardHeader($services.localization.render('platform.wiki.create.wizard.step.cleaningUp'))
        <form action="$doc.getURL()" method="post">
        <div class="wizard-body">
          <p>$services.localization.render('platform.wiki.create.wizard.step.cleaningUp.confirmmessage', ["<strong>$request.wikiId</strong>"])</p>
          <input type="hidden" name="csrf" value="$!escapetool.xml($services.csrf.getToken())" />
          <input type="hidden" name="wikiId" value="$!escapetool.xml($request.wikiId)" />
          <div class="wizard-footer buttons">
            <span class="buttonwrapper">
              <button value="cleanUp" title="Confirm" name="step" id="cleanUp" class="button">$services.localization.render('platform.wiki.create.wizard.step.cleaningUp.confirm')</button>
            </span>
          </div>
        </div>
        </form>
       {{/html}}
    #end
  #else
    #set($wikiId = $request.wikiId)
    {{html clean="false"}}
      #wizardHeader($services.localization.render('platform.wiki.create.wizard.step.cleaningUp'))
      <div class="wizard-body">
      {{/html}}
        #if($request.deleteOk)
        
          {{success}}
            {{html}}$services.localization.render('platform.wiki.create.wizard.step.cleaningup.success', ["<strong>$wikiId</strong>"]){{/html}}
          {{/success}}
          
        #else
        
          {{error}}
            {{html}}$services.localization.render('platform.wiki.create.wizard.step.cleaningup.error', ["<strong>$wikiId</strong>"]){{/html}}
          {{/error}}
          
        #end
        {{html clean="false"}}
      </div>
      </form>
    {{/html}}
  #end
#end
#macro (getExtensionURL $extensionId $extensionVersion $extraParams)
#set ($parameters = {})
##
#if ($extraParams)
  #set ($discard = $parameters.putAll($extraParams))
#end
##
#if ($extensionId)
#set ($discard = $parameters.put('extensionId', $extensionId))
#elseif ($request.extensionId)
#set ($discard = $parameters.put('extensionId', $request.extensionId))
#end
##
#if ($extensionVersion)
#set ($discard = $parameters.put('extensionVersion', $extensionVersion))
#elseif ($request.extensionVersion)
#set ($discard = $parameters.put('extensionVersion', $request.extensionVersion))
#end
##
#if ($request.extensionNamespace)
#set ($discard = $parameters.put('extensionNamespace', $request.extensionNamespace))
#end
##
#if ($xback)
#set ($discard = $parameters.put('xback', $xback))
#elseif ($request.xback)
#set ($discard = $parameters.put('xback', $request.xback))
#end
##
#if ($request.section)
#set ($discard = $parameters.put('section', $request.section))
#end
##
#set ($queryString = '')
#foreach ($entry in $parameters.entrySet())
#set ($queryString = "$queryString&$escapetool.url($entry.key)=$escapetool.url($entry.value)")
#end
$xwiki.getURL('XWiki.XWikiPreferences', 'admin', "editor=globaladmin&section=XWiki.AddExtensions&${queryString.substring(1)}")##
#end
{{/velocity}}
