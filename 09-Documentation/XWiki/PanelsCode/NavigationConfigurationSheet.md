---
id: xwiki-PanelsCode.NavigationConfigurationSheet
type: XWiki Page
space: "PanelsCode"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907256000
sync_date: 2026-08-25 21:14:11
tags:
  - xwiki/documentation
  - space/panelscode
---
# NavigationConfigurationSheet

- **Space:** PanelsCode
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907256000
- **Source:** [NavigationConfigurationSheet](https://wiki.systemaops.in/bin/view/PanelsCode/PanelsCode.NavigationConfigurationSheet)

---

{{velocity output="false"}}
#macro (displayView $configDoc $configObj)
  #foreach ($propertyName in $configObj.propertyNames)
    ; $configDoc.displayPrettyName($propertyName)
      (% class="xHint" %)$services.localization.render("PanelsCode.NavigationConfigurationClass_${propertyName}.hint")(%%)
    : $configDoc.display($propertyName)
  #end
#end

#macro (displayEdit $configObj)
  #set ($discard = $xwiki.ssx.use('PanelsCode.NavigationConfigurationSheet'))
  #set ($discard = $xwiki.jsx.use('PanelsCode.NavigationConfigurationSheet'))
  {{html clean="false"}}
  <div class="hidden">
    <input type="hidden" name="xhidden" value="1" />
    <input type="hidden" name="objectPolicy" value="updateOrCreate" />
    #set ($wikiPreferences = $xwiki.getDocument('XWiki.XWikiPreferences'))
    #set ($pinnedChildPagesObject = $wikiPreferences.getObject('XWiki.PinnedChildPagesClass'))
    #set ($pinnedTopLevelPages = $wikiPreferences.getValue('pinnedChildPages', $pinnedChildPagesObject))
    #if (!$pinnedTopLevelPages)
      #set ($pinnedTopLevelPages = [])
    #end
    <input type="hidden" name="pinnedTopLevelPages" value="$escapetool.xml($jsontool.serialize($pinnedTopLevelPages))" />
  </div>
  {{/html}}
  (% class="row" %)(((
    (% class="col-sm-6" %)(((
      #displayNavigationPanel
      {{info}}{{translation key="index.tree.pinnedChildPages.topLevelHint" /}}{{/info}}
    )))
    (% class="col-sm-6" %)(((
      #displayExcludedPages($configObj)
    )))
  )))
#end

#macro (displayNavigationPanel)
  #set ($navigationPanel = $xwiki.getDocument('Panels.Navigation'))
  $navigationPanel.display('content', 'view').replace('data-dragAndDrop = "false"', 'data-dragAndDrop = "true"'
    ).replace('class = "xtree"', 'class = "xtree jstree-no-links jstree-xwiki-large"')
#end

#macro (displayExcludedPages $configObj)
  {{html clean="false"}}
  <div class="panel panel-info">
    <div class="panel-heading">
      <div class="panel-title">
        $escapetool.xml($services.localization.render('platform.panels.navigation.configuration.excludedPages'))
      </div>
    </div>
    <div class="panel-body">
      <p class="xHint">
        $escapetool.xml($services.localization.render('platform.panels.navigation.configuration.excludedPages.hint'))
      </p>
      #set ($inclusions = {})
      #foreach ($inclusion in $configObj.getValue('inclusions'))
        #set ($discard = $inclusions.put($services.model.resolveDocument($inclusion), $inclusion))
      #end
      #set ($defaultDocumentName = $services.model.getEntityReference('DOCUMENT', 'default').name)
      #topLevelExtensionPagesFilter($configObj $inclusions)
      #topLevelApplicationPagesFilter($configObj $inclusions)
      <div class="exclusion-filter otherPages">
        <p class="exclusion-filter-label">
          $escapetool.xml($services.localization.render('platform.panels.navigation.configuration.otherPages'))
        </p>
        <ul class="exclusion-filter-pages">
          #foreach ($exclusion in $configObj.getValue('exclusions'))
            #set ($documentReference = $services.model.resolveDocument($exclusion))
            #set ($excludedDoc = $xwiki.getDocument($documentReference))
            <li class="page" data-reference="$escapetool.xml($services.model.serialize($documentReference, 'default'))">
              <a href="$excludedDoc.getURL()">$escapetool.xml($excludedDoc.plainTitle)</a>
              <input type="hidden" name="PanelsCode.NavigationConfigurationClass_0_exclusions"
                value="$escapetool.xml($exclusion)" />
            </li>##
          #end
          <li class="empty">
            $escapetool.xml($services.localization.render('platform.panels.navigation.configuration.excludedPages.empty'))
            <input type="hidden" name="PanelsCode.NavigationConfigurationClass_0_exclusions" value="" />
          </li>
        </ul>
      </div>
    </div>
  </div>
  {{/html}}
#end

#macro (topLevelExtensionPagesFilter $configObj $inclusions)
  <div class="exclusion-filter exclusion-filter-dynamic topLevelExtensionPages">
    #exclusionFilterToggle($configObj 'excludeTopLevelExtensionPages')
    <ul class="exclusion-filter-pages#if (!$isFilterActive) hidden#end">
      #set ($query = $services.query.hql('select space.name from XWikiSpace space where space.parent is null'))
      #set ($discard = $query.addFilter('hidden/space'))
      #foreach ($result in $query.execute())
        #set ($documentReference = $services.model.createDocumentReference($NULL, $result, $defaultDocumentName))
        #set ($installedExtensions = $services.extension.xar.getInstalledExtensions($documentReference))
        #if ($installedExtensions && $installedExtensions.size() > 0
            && !$services.extension.xar.isEditAllowed($documentReference))
          #exclusionFilterPage($documentReference $inclusions)
        #end
      #end
      #exclusionFilterEmpty
    </ul>
  </div>
#end

#macro (topLevelApplicationPagesFilter $configObj $inclusions)
  <div class="exclusion-filter exclusion-filter-dynamic topLevelApplicationPages">
    #exclusionFilterToggle($configObj 'excludeTopLevelApplicationPages')
    <ul class="exclusion-filter-pages#if (!$isFilterActive) hidden#end">
      #set ($statement = 'select space.name '
        + 'from XWikiSpace as space, Document as doc, doc.object(AppWithinMinutes.LiveTableClass) as app '
        + 'where space.parent is null and doc.space = space.reference')
      #set ($query = $services.query.xwql($statement).addFilter('hidden/space'))
      #foreach ($result in $query.execute())
        #set ($documentReference = $services.model.createDocumentReference($NULL, $result, $defaultDocumentName))
        ## Don't list application pages that come from installed extensions because we have another filter for this.
        #set ($installedExtensions = $services.extension.xar.getInstalledExtensions($documentReference))
        #if (!$installedExtensions || $installedExtensions.isEmpty())
          #exclusionFilterPage($documentReference $inclusions)
        #end
      #end
      #exclusionFilterEmpty
    </ul>
  </div>
#end

#macro (exclusionFilterToggle $configObj $filterName)
  #set ($isFilterActive = $configObj.getValue($filterName) == 1)
  <p class="exclusion-filter-label">
    <label title="$escapetool.xml($services.localization.render("PanelsCode.NavigationConfigurationClass_${filterName}.hint"))">
      <input type="checkbox" name="PanelsCode.NavigationConfigurationClass_0_$filterName"
        value="1"#if ($isFilterActive) checked="checked"#end />
      <input type="hidden" name="PanelsCode.NavigationConfigurationClass_0_$filterName" value="0" />
      #set ($suffix = $stringtool.uncapitalize($stringtool.removeStart($filterName, 'exclude')))
      $escapetool.xml($services.localization.render("platform.panels.navigation.configuration.$suffix"))
    </label>
  </p>
#end

#macro (exclusionFilterPage $documentReference $inclusions)
  #set ($excludedDoc = $xwiki.getDocument($documentReference))
  #set ($included = $inclusions.containsKey($documentReference))
  <li class="page#if ($included) included#end"
      data-reference="$escapetool.xml($services.model.serialize($documentReference, 'default'))">
    <a href="$excludedDoc.getURL()">$escapetool.xml($excludedDoc.plainTitle)</a>
    #if ($included)
      <input type="hidden" name="PanelsCode.NavigationConfigurationClass_0_inclusions"
        value="$escapetool.xml($inclusions.get($documentReference))" />
    #end
  </li>##
#end

#macro (exclusionFilterEmpty)
  <li class="empty">
    $escapetool.xml($services.localization.render('platform.panels.navigation.configuration.excludedPages.empty'))
    <input type="hidden" name="PanelsCode.NavigationConfigurationClass_0_inclusions" value="" />
  </li>
#end
{{/velocity}}

{{velocity}}
#set ($configDoc = $doc)
#if ($doc.fullName == 'XWiki.XWikiPreferences')
  #set ($configDoc = $xwiki.getDocument('PanelsCode.NavigationConfiguration'))
#end
#set ($configObj = $configDoc.getObject('PanelsCode.NavigationConfigurationClass', true))
(% class="xform navigationPanelConfiguration" %)(((
  #if ($xcontext.action != 'edit' && $xcontext.action != 'admin')
    #displayView($configDoc $configObj)
  #else
    #displayEdit($configObj)
  #end
)))
{{/velocity}}
