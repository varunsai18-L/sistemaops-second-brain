---
name: maintenance-checklist
description: Regular maintenance tasks and schedule for keeping the vault organized and healthy
metadata:
  type: reference
  date: 2026-07-10
---

# Maintenance Checklist

## Overview
This document outlines regular maintenance tasks to keep the Obsidian vault organized, efficient, and useful. Regular maintenance ensures the knowledge base remains valuable over time.

## Purpose
To establish a regular maintenance schedule and procedures that prevent knowledge decay, ensure findability, and maintain system performance.

## Maintenance Schedule

### Daily Tasks
- [ ] Process inbox (`00-Inbox/`) - file new notes appropriately
- [ ] Review and process any flagged items for follow-up
- [ ] Quick glance at today's notes for immediate actions
- [ ] Review today's meetings and create/action items

### Weekly Tasks (Every Friday)
- [ ] Review weekly notes and extract actionable items
- [ ] Process weekly meeting notes
- [ ] Review and update project status notes
- [ ] Check for and resolve any linking issues (broken links)
- broken links report via [[mD
]]
- [ Weekly review of inbox and processing

### Monthly Tasks (First Monday of Month)
- [ ] Run [[mcp__gbrain__find_orphans]] to find orphaned notes
- [ ] Review and tag orphaned notes appropriately
- [ ] Check for duplicate notes and merge if necessary
- [ ] Review [[MOCs (Maps of Content)]] for accuracy and completeness
- [ ] Update any outdated MOCs
- [ ] Run [[mcp__gbrain__get_recent_salience]] to see what's been active
- [ ] Review tagged items from the past month
- [ ] Check tag usage and consolidate redundant tags
- [ ] Review and update [[Naming Conventions]] if needed
- [ ] Check folder structure for misplaced items
- [ ] Review [[Maintenance Checklist]] itself for improvements

### Quarterly Tasks (First Day of Quarter)
- [ ] Deep review of folder structure ([[Folder Structure]])
- [ ] Archive inactive projects to `05-Archive/`
- [ ] Review and update [[Naming Conventions]]
- [ ] Review and update [[Folder Structure]] if needed
- [ ] Run comprehensive orphan report
- [ ] Check vault performance issues
- [ ] Review trace|duration average loading times
- [ ] Backup verification (ensure backups are current and restorable)
- [ ] Review and update [[Vault Guide]] if needed
- [ ] Tag audit: review tag usage and merge/split as needed
- [ ] Review [[MOCs (Maps of Content)]] for major restructuring needs

### Bi-Annual Tasks (January and July)
- [ ] Comprehensive tag review and standardization
- [ ] Review and update all system documentation in 10-System/ and 17-System/
- [ ] Evaluate plugin usage and performance impact
- [ ] Review backup strategy and test restoration
- [ ] Conduct user satisfaction survey (if applicable)
- [ ] Review long-term goals and adjust organization accordingly
- [ ] Archive completed projects older than 2 years
- [ ] Review and update [[Changelog]] and [[Version History]]

### Annual Tasks (January)
- [ ] Full vault health check using [[mcp__gbrain__run_doctor]]
- [ ] Review and update all template notes
- [ ] Archive inactive content (>2 years old unless specifically preserved)
- [ ] Review and update [[Naming Conventions]] and [[Folder Structure]]
- [ ] Evaluate overall vault structure for major reorganization
- [ ] Review backup systems and disaster recovery plan
- [ ] Set goals for the coming year
- [ ] Review and update all system documentation
- [ ] Perform complete tag audit and standardization
- [ ] Check and update all MOCs for accuracy

## Detailed Procedures

### Inbox Management
1. Process all new notes from `00-Inbox/`
2. Apply appropriate naming conventions ([[Naming Conventions]])
3. File in correct folder according to [[Folder Structure]]
4. Add appropriate initial tags
5. Create necessary for new [[
- Mark as processed

### Orphan Management
1. Run orphan detection: [[mcp__gbrain__find_orphans]]
2. Review each orphan:
   - Determine if it should be kept, deleted, or merged
   - If keeping, apply proper naming and filing
   - Add appropriate tags and links
   - Consider if it belongs in an MOC
3. Take action on each item
4. Verify no new orphans remain

### Duplicate Detection and Resolution
1. Search for potential duplicates by title/content
2. Review suspected duplicates:
   - Determine if they are true duplicates
   - If yes, merge content into single note
   - Redirect links from duplicate to master note
   - Delete or archive duplicate
3. Update all links to point to the canonical version

### Tag Maintenance
1. Review tag usage: [[mcp__gbrain__get_tags]]
2. Identify:
   - Rarely used tags (<5 uses) - consider merging or removing
   - Similar tags that could be consolidated (e.g., "#meeting" and "#meetings")
   - Misspelled tags
   - Inconsistent casing or formatting
3. Standardize tag usage:
   - Rename tags for consistency
   - Merge similar tags
   - Remove obsolete tags
   - Apply correct tags to mis-tagged content

### Link Health
1. Run link check to find broken links
2. For each broken link:
   - Determine if target exists elsewhere
   - If yes, update link to correct target
   - If target deleted, remove link or replace with appropriate alternative
   - If target should exist, recreate or restore from archive
3. Verify intentional external links still work
4. Update outdated external links

### MOC (Map of Content) Maintenance
1. Review all MOCs for accuracy and completeness
2. Update MOCs to reflect current structure and content
3. Ensure MOCs follow naming conventions
4. Verify all important content is linked from appropriate MOCs
5. Create new MOCs for growing topics
6. Archive or merge obsolete MOCs

### Archive Management
1. Review `05-Archive/` for content that can be permanently deleted
2. Check archive for items that should be restored to active use
3. Verify archive organization is logical
4. Ensure archived items are properly named and tagged
5. Check for any sensitive information that should be further secured

## Automation Opportunities
Consider implementing these automations (where supported by plugins or scripts):
- Automatic tagging based on content patterns
- Regular orphan reports via automation
- Duplicate detection scripts
- Link validation scheduled reports
- Automated filing of inbox items based on heuristics
- Regular backups with verification
- Template application for common note types

## Tools and Reports
Use these built-in queries and reports for maintenance:

### Finding Orphans
```
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
SORT file.name
```
### Finding Duplicates (by similar names)
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
GROUP BY file.name
HAVING Count(file.name) > 1
```
### Finding Untagged Notes
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
  AND length(tags) = 0
SORT file.name
```
### Finding Old Unmodified Notes
```dataview
LIST
FROM ""
WHERE !contains(file.path, "10-System")
  AND !contains(file.path, "11-Meta")
  AND !contains(file.path, "17-System")
  AND !contains(file.path, "00-Inbox")
  AND !contains(file.path, "06-Templates")
  AND file.modified < date(today) - dur(6 months)
SORT file.modified
```

## Troubleshooting Common Issues

### Performance Issues
- Check for excessively large notes (>100KB)
- Review plugin usage and disable unnecessary ones
- Check for problematic community plugins
- Verify hardware acceleration settings
- Consider splitting very large notes

### Link Issues
- Use "Broken links" in the sidebar
- Check for renamed files that broke links
- Verify aliases are correctly set
- Check for case sensitivity issues in links

### Tag Inconsistencies
- Use tag pane to review tag usage
- Search for similar tag variations
- Check for inconsistent casing
- Verify hierarchical tag usage

### Organization Drift
- Refer to [[Folder Structure]] for correct placement
- Check [[Naming Conventions]] for proper naming
- Review recent changes for misfiled items
- Use graph view to identify disconnected clusters

## Recording Maintenance
After completing maintenance:
1. Update this checklist with completion dates
2. Add entry to [[Changelog]] if significant changes made
3. Note any issues discovered and actions taken
4. Update [[Vault Guide]] if procedures changed
5. Consider adding to [[Monthly Review]] or [[Quarterly Review]] notes

## Related Documents
- [[Vault Guide]] - Comprehensive usage guide
- [[Folder Structure]] - Detailed folder structure explanation
- [[Naming Conventions]] - Naming standards and conventions
- [[Changelog]] - System change history
- [[Version History]] - Version release details
- [[System Health]] - Monitoring and health guidelines
- [[MOCs (Maps of Content)]] - Guidelines for creating and maintaining MOCs

## Maintenance
Review this checklist quarterly and update as procedures evolve.
Last reviewed: 2026-07-10
Next review: 2026-10-10