---
name: naming-conventions
description: Standards and conventions for naming files, folders, tags, and links within the vault
metadata:
  type: reference
  date: 2026-07-10
---

# Naming Conventions

## Overview
This document establishes naming conventions for files, folders, tags, and links within the Obsidian vault to ensure consistency, discoverability, and maintainability.

## Purpose
To establish clear, consistent naming standards that improve searchability, linking, and overall organization of the knowledge vault.

## File Naming Conventions

### General Principles
- Use clear, descriptive names that indicate content
- Avoid special characters except hyphens and underscores
- Use consistent date formats where applicable
- Keep names concise but meaningful
- Use title case for proper nouns, sentence case for descriptive titles

### Person Notes
- Format: `First Last` (e.g., `John Smith`)
- For disambiguation: `First Last - Role/Company` (e.g., `John Smith - Engineer at Acme`)
- Always include full name for discoverability
- Include middle initial if commonly used: `John A. Smith`

### Company/Organization Notes
- Format: `Company Name` (e.g., `Acme Corporation`)
- For subsidiaries: `Parent Company - Subsidiary` (e.g., `Alphabet Inc. - Google`)
- Avoid legal suffixes unless necessary for disambiguation (Inc., Corp., Ltd.)
- Use commonly recognized names

### Project Notes
- Format: `[STATUS] Project Name` or `Project Name - [TIMEFRAME]`
- Status indicators: `[PLANNING]`, `[ACTIVE]`, `[ON HOLD]`, `[COMPLETED]`
- Timeframe format: `YYYY` or `YYYY-Q#` or `YYYY-MM`
- Examples: 
  - `[ACTIVE] Website Redesign`
  - `AI Research Project - 2024`
  - `[ON HOLD] Mobile App - Q1 2024`

### Resource Notes
- Books: `Book Title - Author Name` (e.g., `Atomic Habits - James Clear`)
- Articles: `Article Title - Source/Publication` (e.g., `The Future of AI - MIT Technology Review`)
- Courses: `Course Title - Platform/Instructor` (e.g., `Machine Learning - Coursera/Andrew Ng`)
- Tools: `Tool Name - Version/Version` (e.g., `Obsidian - v1.5.0`)

### Meeting Notes
- Format: `YYYY-MM-DD Meeting - [Topic/Attendees]`
- Examples:
  - `2024-01-15 Meeting - Project Kickoff`
  - `2024-01-20 Meeting - Leadership Team`
  - `2024-01-10 1:1 - Manager Name`

### Daily Notes
- Format: `YYYY-MM-DD` (e.g., `2024-01-15`)
- Optional suffix for special days: `YYYY-MM-DD - [Description]` (e.g., `2024-01-15 - Conference`)

### Template Notes
- Format: `[Template Type] - Description` (e.g., `[Meeting Notes] - Team Standup`)
- Alternative: `Template: Description` (e.g., `Template: Project Proposal`)

## Folder Naming Conventions
See [[Folder Structure]] for detailed folder structure, but general principles:
- Use two-digit prefixes for ordering: `00-`, `01-`, `02-`, etc.
- Use clear, descriptive names after prefix
- Avoid special characters except hyphens
- Use plural nouns for collections (e.g., `01-People`, `02-Companies`)

## Tagging Conventions

### General Principles
- Use lowercase for all tags
- Use hyphens for multi-word tags
- Be specific but not overly granular
- Use hierarchical tags for related concepts
- Apply multiple relevant tags when appropriate

### Person Tags
- `#person` - Base tag for all people
- `#contact` - For business contacts
- `#expert` - For subject matter experts
- `#team-[name]` - For team members (e.g., `#team-marketing`)
- `#role-[title]` - For role-based tagging (e.g., `#role-manager`)

### Company/Organization Tags
- `#company` - Base tag for all companies
- `#organization` - For non-corporate organizations
- `#client` - For client organizations
- `#partner` - For partner organizations
- `#competitor` - For competitors
- `#industry-[sector]` - For industry classification (e.g., `#industry-tech`)

### Project Tags
- `#project` - Base tag for all projects
- `#active` - For active projects
- `#planning` - For projects in planning phase
- `#on-hold` - For paused projects
- `#completed` - For completed projects (before archiving)
- `#type-[category]` - For project types (e.g., `#type-research`, `#type-development`)

### Resource Tags
- `#resource` - Base tag for all resources
- `#book` - For books
- `#article` - For articles and papers
- `#course` - For educational courses
- `#tool` - For software and tools
- `#template` - For templates
- `#format-[type]` - For format specification (e.g., `#format-video`, `#format-podcast`)

### Status and Metadata Tags
- `#status-[status]` - For status tracking (e.g., `#status-in-progress`, `#status-review`)
- `#priority-[level]` - For priority levels (e.g., `#priority-high`, `#priority-low`)
- `#review-[date]` - For review scheduling (e.g., `#review-2024-06-01`)
- `#review-quarterly`, `#review-monthly` - For recurring reviews
- `#verified` - For fact-checked information
- `#todo` - For action items

### Geographic Tags
- `#location-[place]` - For geographic locations (e.g., `#location-new-york`, `#location-remote`)
- `#region-[region]` - For remote work regions (e.g., `#region-apac`, `#region-emea`)

### Time-Based Tags
- `#year-[year]` - For year-specific content (e.g., `#year-2024`)
- `#quarter-[q#]` - For quarter-specific content (e.g., `#quarter-q1`)
- `#month-[month]` - For month-specific content (e.g., `#month-january`)
- `#recurring` - For recurring events or tasks

## Linking Conventions

### WikiLinks
- Use double brackets for internal links: `[[Note Title]]`
- Use aliases for different display text: `[[Actual Note Title|Display Text]]`
- Link to specific blocks using `^block-id`: `[[Note Title^block-id]]`
- Link to headers: `[[Note Title#Header Name]]`

### External Links
- Use standard markdown: `[Display Text](URL)`
- Always include descriptive text
- Consider adding metadata in comments for tracked links

### Embedded Content
- Use `![[Note Title]]` for note embeds
- Use `![[Note Title^block-id]]` for block embeds
- Use `![[image.jpg]]` for images

## Special Naming Cases

### Measurements and Data
- Use standard units: `10kg`, `5mb`, `2tb`
- Format dates consistently: `YYYY-MM-DD`
- UseISO 8601 for timestamps: `YYYY-MM-DDTHH:mm:ss`

### Version Numbers
- Use semantic versioning where applicable: `v1.2.3`
- For internal versions: `v1.2.3-internal`
- For drafts: `v1.2.3-draft`

### Language and Localization
- Primary language: English
- For non-English content: `[Language] Content Title` (e.g., `[Spanish] Título del Contenido`)
- Language tags: `#language-es`, `#language-fr`, etc.

## File-Specific Guidelines

### Markdown Files (.md)
- Primary format for notes
- Follow all above conventions
- Use appropriate frontmatter (see Template Guidelines)

### Image Files
- Format: `description-context.jpg/png` (e.g., `diagram-system-architecture.png`)
- Store in appropriate folder or same folder as referencing note
- Consider using `/_resources/` subfolder in note directory for multiple images

### PDF and Other Documents
- Format: `document-title-author-date.pdf` (e.g., `research-ai-trends-2024.pdf`)
- Store in `04-Resources/` or relevant project folder
- Consider linking rather than duplicating when possible

## Frontmatter Standards
For notes using frontmatter (YAML at top of file):

```yaml
---
name: note-name
description: Brief description of the note
metadata:
  type: person | company | project | resource | template | system
  status: active | inactive | archived | deprecated
  tags:
    - tag1
    - tag2
  created: YYYY-MM-DD
  modified: YYYY-MM-DD
  version: 1.0
---
```

Field Descriptions:
- `name`: Machine-readable identifier (kebab-case)
- `description`: Human-readable description
- `metadata.type`: Primary type classification
- `metadata.status`: Current status
- `metadata.tags`: Additional tags beyond frontmatter
- `created`: Creation date
- `modified`: Last modification date
- `version`: Version number for evolving documents

## Examples

### Person Note
```markdown
---
name: john-smith
description: Senior Software Engineer at TechCorp
metadata:
  type: person
  status: active
  tags:
    - engineer
    - techcorp
    - backend
  created: 2024-01-15
  modified: 2024-01-15
---

# John Smith

Senior Software Engineer at TechCorp specializing in backend systems.

## Contact
- Email: john.smith@techcorp.com
- LinkedIn: linkedin.com/in/johnsmith

## Expertise
- [[Backend Development]]
- [[Database Design]]
- [[API Development]]

## Projects
- [[API Gateway Redesign]]
- [[Microservices Migration]]
```

### Project Note
```markdown
---
name: website-redesign-2024
description: Complete redesign of company website
metadata:
  type: project
  status: active
  tags:
    - frontend
    - design
    - marketing
  created: 2024-01-10
  modified: 2024-01-15
  deadline: 2024-06-30
---

# [ACTIVE] Website Redesign

Project to redesign the company website for improved user experience and conversion.

## Timeline
- Start: 2024-01-10
- End: 2024-06-30
- Milestone 1: Wireframes complete - 2024-02-15
- Milestone 2: Design mockups - 2024-03-31
- Milestone 3: Development complete - 2024-05-30
- Milestone 4: Launch - 2024-06-30

## Team
- [[John Smith]] - Project Lead
- [[Jane Doe]] - UX Designer
- [[Bob Wilson]] - Developer

## Resources
- [[Brand Guidelines]]
- [[User Research 2023]]
- [[Competitor Analysis]]
```

## Maintenance
- Review naming conventions quarterly via [[Maintenance Checklist]]
- Update as new types of content are added
- Ensure team awareness and adherence
- Monitor for inconsistencies during regular vault maintenance
- Archive or rename legacy content that doesn't conform (during scheduled maintenance)

## Related Documents
- [[Vault Guide]] - Comprehensive usage guide
- [[Folder Structure]] - Detailed folder structure explanation
- [[Maintenance Checklist]] - Regular maintenance tasks
- [[Changelog]] - System change history
- [[Version History]] - Version release details
- [[System Health]] - Monitoring and health guidelines

## Maintenance
Review this document quarterly and update as naming conventions evolve.
Last reviewed: 2026-07-10