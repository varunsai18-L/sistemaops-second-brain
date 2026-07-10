# Naming Conventions

## Overview
This document establishes standardized naming conventions for notes, tags, and other elements within the Obsidian vault to ensure consistency, discoverability, and maintainability.

## Purpose
To eliminate ambiguity in naming, improve searchability, and create a predictable structure that supports effective knowledge management.

## File Naming

### General Principles
- Use lowercase letters, numbers, and hyphens only
- Avoid spaces, special characters, and underscores
- Use descriptive, concise names that indicate content
- Use kebab-case (kebab-case) for multi-word names

### Specific Conventions
| Element Type | Convention | Example |
|--------------|------------|---------|
| Regular Notes | `descriptive-name.md` | `project-alpha-plan.md` |
| Template Notes | `template-<purpose>.md` | `template-meeting-notes.md` |
| Daily Notes | `YYYY-MM-DD.md` | `2024-01-15.md` |
| Templates | `template-<name>.md` | `template-project-proposal.md` |
| Index/MOCs | `moc-<topic>.md` | `moc-machine-learning.md` |
| Archives | `archive-<original-name>-YYYY-MM.md` | `archive-project-beta-2023-12.md` |
| Templates | `template-<name>.md` | `template-meeting-agenda.md` |

### Special Cases
- **People**: Use `firstname-lastname` format (e.g., `john-doe.md`)
- **Organizations**: Use `organization-name` format (e.g., `acme-corporation.md`)
- **Projects**: Use `project-name` or `initiative-name` format (e.g., `website-redesign.md`)
- **Events**: Use `event-name-YYYY-MM-DD` format (e.g., `annual-conference-2024-03.md`)
- **Books**: Use `book-title-author` format (e.g., `atomic-habits-james-clear.md`)
- **Movies**: Use `movie-title-year` format (e.g., `inception-2010.md`)

## Tag Naming

### General Principles
- Use lowercase letters, numbers, hyphens, and slashes only
- Use hierarchical structure with slashes for categorization
- Be specific but not overly granular
- Use consistent terminology across the vault

### Hierarchical Structure
```
#area/subarea
#project/project-name
#topic/subtopic
#type/document-type
#status/status-value
#priority/priority-level
```

### Common Tag Prefixes
- `#area/` - Areas of responsibility (e.g., `#area/health`, `#area/finance`)
- `#project/` - Active projects` (e.g., `#project/website-redesign`)
- `#area/` - Areas of responsibility (e.g., `#area/health`, `#area/finance`)
- `#topic/` - Subject areas (e.g., `#topic/machine-learning`, `#topic/productivity`)
- `#type/` - Content types (e.g., `#type/meeting-notes`, `#type/book-notes`)
- `#status/` - Workflow status (e.g., `#status/draft`, `#status/review`, `#status/published`)
- `#priority/` - Priority levels (e.g., `#priority/high`, `#priority/medium`, `#priority/low`)
- `#status/` - Status indicators (e.g., `#status/active`, `#status/archived`, `#status/archived`)

### Specific Examples
- `#area/health/fitness`
- `#project/website-redesign`
- `#topic/quantum-computing`
- `#type/meeting-notes`
- `#status/draft`
- `#priority/high`
- `#source/book`
- `#author/john-doe`

## Linking Conventions

### Wikilinks
- Use double brackets: `[[Note Title]]`
- For notes with specific naming, use the exact filename (without .md)
- Use aliases when needed: `[[Note Title|Alias]]`
- Link to specific blocks: `[[Note Title#^block-id]]`

### External Links
- Use standard markdown: `[Description](URL)`
- Prefer descriptive link text over raw URLs
- Use reference-style links for repeated URLs

### Embedding
- Use `![[Note Title]]` for transclusion
- Use `![[Note Title#^block-id]]` for specific block embedding
- For external media: `![Description](URL)`

## Naming Best Practices

### Clarity Over Brevity
- Prefer clear, descriptive names over cryptic abbreviations
- Example: `project-alpha-phase-plan.md` vs `pap.md`

### Consistency
- Apply the same naming rules consistently across similar content types
- Regularly audit and refine naming patterns

### Searchability
- Anticipate how you'll search for the note
- Include key terms that you're likely to search for
- Consider multiple potential search terms

### Avoid Redundancy
- Don't repeat information already captured in tags or folders
- Example: If using `#area/finance` tag, don't include "finance" in every finance-related note title

### Versioning
- For versioned documents, use: `document-name-v2.md` or `document-name-2024-01.md`
- Consider using date versioning for temporal documents

## Exceptions and Special Cases

### Legacy Notes
- Existing notes that don't conform should be gradually updated during regular maintenance
- Maintain redirects using aliases when renaming established notes

### External Standards
- When integrating with external systems (e.g., Zotero, GitHub), consider adopting their naming conventions for integration points
- Maintain internal consistency while respecting external constraints

### Personal Names
- For people with non-Western names, follow their preferred romanization
- Consider including honorifics or titles when relevant for disambiguation (e.g., `dr-jane-smith.md`)

## Maintenance
This document should be reviewed annually or when significant inconsistencies are observed in naming practices.

## Related Documents
- [[01-System Architecture]]
- [[03-Linking Guidelines]]
- [[04-Template Standards]]
- [[05-Maintenance Procedures]]
- [[06-Backup Procedures]]
- [[07-Glossary]]
- [[08-Change Log]]

## Change Log
See [[08-Change Log]] for detailed version history.