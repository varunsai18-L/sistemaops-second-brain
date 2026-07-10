---
name: system-health
description: Guidelines for monitoring, troubleshooting, and maintaining the health of the Obsidian vault system
metadata:
  type: reference
  date: 2026-07-10
---

# System Health

## Overview
This document provides guidelines for monitoring, troubleshooting, and maintaining the health and
---

# System Health

## Overview
This document provides guidelines for monitoring the health of the Obsidian vault system, identifying issues, and performing troubleshooting to maintain optimal performance and usability.

## Purpose
To establish procedures for monitoring system health, detecting problems before they impact usability.

## Health

1. Performance**
     Opening time (startup)**
-    
  - **Search response time** (should be under 1 second for most queries)
  - **plugin performance** (monitor for slow or
  - **Sync status** (if
  - **Mobile app performance** (if applicable)

### 2. Content
INote sizes** (individual notes should generally be under 100KB unless
  - **Broken links** (should be 0, or have a clear plan for resolution)
  - **Orphaned notes** (notes with no incoming links - should be minimized)
  - **Duplicate notes** (should be identified and merged)
  - **Tag bloat** (excessive NON from in

### 3. Organizational Health
  - **Folder structure compliance** (notes should be in correct folders per [[Folder]])
  - **Naming convention adherence** (notes should follow [[Naming]])
  - **Tag usage consistency** (tags should be used consistently per [[Naming]])
  - **MOC accuracy** (Maps of Content should reflect current structure)
  - **Template usage** (appropriate use of templates for consistency)

### 4. Metadata and
  - **Frontmatter completeness** (notes using front
}

## Monitoring Tools and Techniques

### Built-in Obsidian Features

#### 1. **Graph View**
- Use to identify orphaned notes (notes with no connections)
- Use to see clusters of related content
- Identify overly connected notes that might be too broad
- Monitor health of knowledge connections over time

#### 2. **Tags Pane**
- Monitor tag usage and distribution
- Identify unused or rarely used tags
- Spot inconsistent tag usage (case variations, similar meanings)
- Monitor tag growth over time

#### 3. **File Explorer**
- Monitor folder sizes and item counts
- Identify folders that are disproportionately large
- Check for misplaced items
- Monitor archive growth

#### 4. **Search Functionality**
- Test search performance regularly
- Monitor for slow searches that might indicate indexing issues
- Test complex queries to ensure boolean logic works
- Monitor search relevance over time

### Advanced Monitoring Queries

#### Finding Orphaned Notes
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
  AND length(incoming(file.link)) = 0
  AND !contains(tags, "#template")
  AND !contains(tags, "#daily")
SORT file.name
LIMIT 100
```

#### Finding Broken Links
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
  AND file.outgoing(file.link)
  AND ANY(outgoing(file.link), (link) => !file.exists(link))
```

#### Finding Large Notes
```dataview
LIST length(file.name) as "Name Length", file.size as "Size (bytes)"
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
  AND file.size > 100000
SORT file.size DESC
LIMIT 50
```

#### Finding Duplicate Titles
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
GROUP BY file.name
HAVING COUNT(file.name) > 1
SORT COUNT(file.name) DESC
```

## Health Indicators and Thresholds

### Green (Healthy)
- Startup time: < 3 seconds
- Search response: < 1 second for simple queries
- Orphaned notes: < 1% of total notes
- Broken links: 0
- Average note size: < 50KB
- Tag usage consistency: > 95% compliance
- Folder structure compliance: > 98% compliance

### Yellow (Needs Attention)
- Startup time: 3-5 seconds
- Search response: 1-3 seconds
- Orphaned notes: 1-3% of total notes
- Broken links: 1-10
- Average note size: 50-100KB
- Tag usage consistency: 85-95% compliance
- Folder structure compliance: 90-98% compliance

### Red (Requires Immediate Attention)
- Startup time: > 5 seconds
- Search response: > 3 seconds
- Orphaned notes: > 3% of total notes
- Broken links: > 10
- Average note size: > 100KB
- Tag usage consistency: < 85% compliance
- Folder structure compliance: < 90% compliance

## Regular Health Checks

### Daily Checks
- [ ] Verify Vault opens bond
 (Quick)
- [ ] Vault opens without errors
- [ ] No sync conflicts visible
- [ ] Today's notes accessible
- [ ] Daily notes template working

### Weekly Checks
- [ ] Run orphaned notes report
- [ ] Check for broken links (use built-in sidebar)
- [ ] Review plugin updates and compatibility
- [ ] Check mobile sync (if applicable)
- [ ] Review inbox processing

### Monthly Checks
- [ ] Run comprehensive health check using [[mcp__gbrain__run_doctor]]
- [ ] Run orphaned notes report and broken links reports
- [ ] Check folder structure compliance
- [ ] Review naming convention adherence
- [ ] Analyze tag usage and consistency
- [ ] Check template usage rates
- [ ] Review archive growth
- [ ] Monitor vault size growth

### Quarterly Checks
- [ ] Deep dive into specific content areas
- [ ] Review MOC accuracy and completeness
- [ ] Evaluate folder structure for optimization
- [ ] Review naming conventions for updates
- [ ] Assess tag hierarchy for optimization
- [ ] Review template effectiveness
- [ ] Check for knowledge gaps
- [ ] Evaluate linking practices

### Annual Checks
- [ ] Complete vault health assessment
- [ ] Evaluate overall knowledge management effectiveness
- [ ] Review backup and disaster recovery procedures
- [ ] Assess user satisfaction and effectiveness
- [ ] Plan for major structural changes if needed
- [ ] Review long-term goals and adjust accordingly

## Troubleshooting Common Issues

### Performance Issues

#### Slow Startup
**Symptoms**: Vault takes more than 5 seconds to open
**Possible Causes**:
- Too many plugins enabled
- Large number of notes (>10,000)
- Corrupted cache
- Hardware limitations
**Solutions**:
- Disable unnecessary plugins
- Check for and remove corrupted cache files
- Consider splitting vault if excessively large
- Verify hardware meets minimum requirements

#### Slow Search
**Symptoms**: Search takes more than 2 seconds to return results
**Possible Causes**:
- Indexing issues
- Complex queries with boolean logic
- Large attachments indexed
- Plugin interference
**Solutions**:
- Rebuild index (Settings → Files & Links → "Rebuild index")
- Simplify complex search queries
- Check attachment settings in Files & Links
- Disable plugins one by one to identify culprit

#### Lag During Editing
**Symptoms**: Noticeable lag when typing or navigating large notes
**Possible Causes**:
- Extremely large notes (>500KB)
- Too many embeds or transclusions
- Resource-intensive plugins
- Inline CSS or HTML causing rendering issues
**Solutions**:
- Split large notes into smaller, connected notes
- Reduce number of embeds in single notes
- Disable plugins to identify performance issues
- Simplify note formatting

### Content Issues

#### Broken Links
**Symptoms**: Links showing as broken or missing in graph view
**Possible Causes**:
- Target note renamed without updating links
- Target note deleted or moved
- Typo in link
- Case sensitivity issues (less common)
**Solutions**:
- Use "Broken links" in sidebar to identify
- Search for similar note names to find moved content
- Restore from archive if accidentally deleted
- Update links to correct targets
- Use aliases for renamed content when appropriate

#### Orphaned Notes
**Symptoms**: Notes with no incoming links appearing in orphan reports
**Possible Causes**:
- Recently created notes not yet linked
- Notes that were never properly integrated
- Content that should be deleted or merged
- Notes that belong in MOCs but aren't linked
**Solutions**:
- Review each orphan and determine appropriate action
- Link to relevant MOCs or related content
- Merge with existing content if duplicate
- Delete if no longer relevant
- Create intentional MOCs for groups of related orphans

#### Tag Inconsistencies
**Symptoms**: Similar concepts tagged differently, hard to find related content
**Possible Cases**:
- Case variations (`#project` vs `#Project`)
- Similar meanings (`#initiative` vs `#project`)
- Plural vs singular (`#tag` vs `#tags`)
- Hyphenation inconsistencies (`#tag-name` vs `#t
**Solutions**:
- Standardize on one form
- Use tag aliasing or planned migration
- Review and update inconsistent usage
- Document standards in [[Naming Conventions]]
- Run regular tag audit reports

### Organizational Issues

#### Misplaced Content
**Symptoms**: Notes found in incorrect folders per [[Folder Structure]]
**Possible Causes**:
- Incorrect filing during processing
- Lack of awareness of structure
- Ambiguous content that could fit multiple categories
- Changes in structure not communicated
**Solutions**:
- Review [[Folder Structure]] for correct placement
- Move content to correct location
- Improve processing procedures
- Communicate structure changes clearly
- Create decision guidelines for ambiguous content

#### Naming Convention Violations
**Symptoms**: Notes not following [[Naming Conventions]]
**Possible Causes**:
- Lack of awareness of conventions
- Inconsistent application
- Legacy content from before conventions
- Edge cases not covered in documentation
**Solutions**:
- Review [[Naming Conventions]] for correct naming
- Rename notes to follow conventions
- Improve template usage to enforce conventions
- Update documentation for uncovered edge cases
- Run regular compliance checks

### Technical Issues

#### Sync Conflicts
**Symptoms**: Conflict notifications when using sync service
**Possible Causes**:
- Simultaneous editing on multiple devices
- Network interruptions during save
- Sync service issues
**Solutions**:
- Review conflicts in sync interface
- Choose correct version or manually merge
- Ensure adequate network connectivity
- Consider adjusting sync settings if conflicts frequent
- Educate users on avoiding simultaneous editing

#### Plugin Issues
**Symptoms**: Unexpected behavior, errors, or performance issues after plugin updates
**Possible Causes**:
- Incompatible plugin versions
- Plugin conflicts
- Bugs in plugin updates
**Solutions**:
- Disable recently updated plugins to identify culprit
- Check plugin compatibility with current Obsidian version
- Look for alternative plugins with similar functionality
- Report issues to plugin developers
- Consider waiting for plugin updates before upgrading

#### Cache Corruption
**Symptoms**: Strange behavior, missing content, or errors that persist after restart
**Possible Causes**:
- Improper shutdown
- Disk errors
- Software bugs
**Solutions**:
- Restart Obsidian
- Clear cache (Settings → About → "Restart without community plugins" then disable/reenable)
- Check disk health
- Consider reinstalling if persistent

## Maintenance Procedures for System Health

### Regular Maintenance Tasks
See [[Maintenance Checklist]] for detailed schedule, but key health-related tasks include:

#### Weekly
- [ ] Check for and resolve broken links
- [ ] Review orphaned notes and take appropriate action
- [ ] Monitor plugin performance and update as needed
- [ ] Verify sync status and resolve conflicts

#### Monthly
- [ ] Run [[mcp__gbrain__run_doctor]] for comprehensive health check
- [ ] Analyze startup and search performance
- [ ] Review folder structure compliance (>98% target)
- [ ] Check naming convention adherence (>95% target)
- [ ] Analyze tag usage for consistency and bloat
- [ ] Check average note size and identify outliers

#### Quarterly
- [ ] Deep dive health assessment of specific areas
- [ ] Evaluate MOC effectiveness and accuracy
- [ ] Review template usage and effectiveness
- [ ] Check knowledge gap analysis
- [ ] Assess overall structure optimization opportunities

#### Annual
- [ ] Complete system health evaluation
- [ ] Evaluate backup and disaster recovery procedures
- [ ] Assess long-term structural needs
- [ ] Plan for major upgrades or changes
- [ ] Review user satisfaction and effectiveness

## Health Reporting and Documentation

### Reporting Issues
When encountering system health issues:
1. Document symptoms clearly
2. Note when issue occurs and under what conditions
3. Record any error messages
4. Identify recent changes that might have caused issue
5. Try basic troubleshooting (restart, disable plugins)
6. Escalate if unresolved after basic steps

### Health Log
Consider maintaining a simple health log:
```
## System Health Log

### 2026-07-10 - Performance Check
- Startup time: 2.3 seconds (Green)
- Search response: 0.8 seconds (Green)
- Orphaned notes: 12 (0.1% - Green)
- Broken links: 0 (Green)
- Average note size: 34KB (Green)
- Actions: None needed
```

### Communication
For significant health issues:
- Notify relevant stakeholders
- Document issue and resolution
- Update procedures if needed to prevent recurrence
- Consider adding to [[Changelog]] if systemic issue

## Tools for Health Monitoring

### Built-in Obsidian Tools
- **Graph View** - for visualizing connections and finding orphans
- **Tags Pane** - for monitoring tag usage
- **File Explorer** - for monitoring folder structure and sizes
- **Search** - for testing performance and finding specific issues
- **Sidebar** - includes broken links indicator
- **About** - shows version info and has debugging tools

### Advanced Monitoring
- **Dataview queries** - for custom health reports (examples above)
- **Templater** - for automated health check templates
- **QuickAdd** - for quick health logging
- **Periodic Notes** - for regular health reporting templates

### External Tools (if applicable)
- **System monitoring tools** - for checking resource usage
- **Backup verification tools** - for ensuring backups are good
- **Network monitoring tools** - for sync-related issues
- **Disk health tools** - for checking storage integrity

## Escalation Procedures

### Level 1: Self-Service
- Basic troubleshooting (restart, check for obvious issues)
- Consult this document and [[Maintenance Checklist]]
- Try disabling plugins to isolate issues
- Search Obsidian help and forums

### Level 2: Community Support
- Consult Obsidian community forums
- Check plugin documentation and issue trackers
- Search for similar issues reported by others
- Consider reaching out to plugin developers

### Level 3: Expert Support
- Consult with knowledge management team
- Consider professional Obsidian consulting if available
- Evaluate whether issues indicate need for structural changes
- Consider whether migration to different system might be warranted

## Related Documents
- [[Vault Guide]] - Comprehensive usage guide
- [[Folder Structure]] - Detailed folder structure explanation
- [[Naming Conventions]] - Naming standards and conventions
- [[Maintenance Checklist]] - Regular maintenance tasks
- [[Changelog]] - Record of changes made to the system
- [[Version History]] - History of vault versions and releases

## Maintenance
Review this document quarterly and update as monitoring procedures and tools evolve.
Last reviewed: 2026-07-10
Next review: 2026-10-10