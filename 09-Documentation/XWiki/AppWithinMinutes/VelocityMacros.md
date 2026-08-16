---
id: xwiki-AppWithinMinutes.VelocityMacros
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906769000
sync_date: 2026-08-16 19:45:26
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# VelocityMacros

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906769000
- **Source:** [VelocityMacros](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.VelocityMacros)

---

{{velocity output="false"}}
#macro (getAppReference)
  #set ($appLocalRef = $doc.getValue('dataSpaceName'))
  #if ("$!appLocalRef" != '')
    ## Between 6.3M2 (XWIKI-11249) and 7.3RC1 (XWIKI-12741).
    #set ($appReference = $services.model.resolveSpace($appLocalRef))
  #else
    ## Possible locations:
    ## 1. same space (<6.2M1, XWIKI-8757)
    ## 2. sibling space (between 6.2M1 and 6.3M2)
    ## 3. grand parent space (7.3RC1+)
    #set ($appReferences = [
      $doc.documentReference.parent,
      $services.model.createSpaceReference($stringtool.removeEnd($doc.documentReference.name, 'TemplateProvider'),
        $doc.documentReference.parent.parent),
      $doc.documentReference.parent.parent
    ])
    #foreach ($item in $appReferences)
      #set ($appReference = $item)
      #if ($xwiki.getDocument($appReference).getObject($appDescriptorClassName))
        #break
      #end
    #end
  #end
#end

#macro (getAppTitle)
  #getAppReference
  #set ($appTitle = $xwiki.getDocument($appReference).plainTitle)
#end

#macro (getExpectedAppClassReference $appName $appReference)
  #set ($expectedClassName = "$!{appName}Class")
  #set ($expectedClassLocations = [
    $services.model.createSpaceReference('Code', $appReference),
    $services.model.createSpaceReference("${appReference.name}Code", $appReference.parent),
    $appReference
  ])
  #set ($found = false)
  #foreach ($expectedClassLocation in $expectedClassLocations)
    #set ($expectedClassReference = $services.model.createDocumentReference($expectedClassName,
      $expectedClassLocation))
    #if ($xwiki.exists($expectedClassReference))
      #set ($found = true)
      #break
    #end
  #end
  #if (!$found)
    #set ($expectedClassReference = $NULL)
  #end
#end

#macro (getAppClassReference $appHomePage)
  #set ($appName = $appHomePage.pageReference.name)
  #set ($appReference = $appHomePage.documentReference.parent)
  ## Look for the application class in the expected location.
  #getExpectedAppClassReference($appName $appReference)
  #if ($expectedClassReference)
    #set ($classReference = $expectedClassReference)
  #else
    ## The application was probably moved or renamed.
    ## The configured class reference is relative to the application home page (holding the application descriptor).
    #set ($configuredClassReference = $services.model.resolveDocument("$!appHomePage.getValue('class')",
      $appHomePage.documentReference))
    #set ($previousAppName = $stringtool.removeEnd($configuredClassReference.name, 'Class'))
    ## Look for a class with the previous name in the current location.
    #getExpectedAppClassReference($previousAppName $appReference)
    #if ($expectedClassReference)
      #set ($classReference = $expectedClassReference)
    #else
      ## Use the configured class.
      #set ($classReference = $configuredClassReference)
    #end
  #end
#end
{{/velocity}}
