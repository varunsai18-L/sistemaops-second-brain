---
name: folder-structure
description: Detailed explanation of the vault's organizational hierarchy and folder structure
metadata:
  type: reference
  date: 2026-07-10
---

# Folder Structure

## Overview
This document describes the organizational structure of the Obsidian vault, explaining the purpose and usage of each top-level folder and subfolder structure.

## Top-Level Structure

```
second brain/
├── 00-Inbox/                 # Incoming items requiring processing
├── 01-People/                # People and relationships
├── 02-Companies/             # Companies and organizations
├── 03-Projects/              # Active projects and initiatives
├── 04-Resources/             # Reference materials and resources
├── 05-Archive/               # Archived and inactive items
├── 06-Templates/             # Reusable note templates
├── 10-System/                # System documentation and maintenance (THIS FOLDER)
├── 11-Meta/                  # Metadata and system-level notes
└── 17-System/                # System documentation (current location)
```

## Detailed Folder Descriptions

### 00-Inbox
- **Purpose**: Temporary holding area for new items requiring processing
- **Usage**: 
  - New ideas, notes, and items go here initially
  - Processed items are moved to appropriate permanent locations
  - Reviewed daily as part of inbox zero practice
- **Contents**: 
  - Fleeting notes
  - Meeting notes awaiting processing
  - Ideas requiring clarification
  - Items awaiting categorization

### 01-People
- **Purpose**: Information about individuals and relationships
- **Structure**:
  - `01-People/Contacts/` - Contact information
  - `01-People/Relationships/` - Relationship maps and connection notes
  - `01-People/Profiles/` - Detailed person profiles
  - `01-People/Teams/` - Team and group information
- **Naming**: `First Last` or `Role - Name` for disambiguation
- **Tagging**: `#person`, `#contact`, relationship-specific tags

### 02-Companies
- **Purpose**: Information about organizations and companies
- **Structure**:
  - `02-Companies/Profiles/` - Company profiles and information
  - `02-Companies/Relationships/` - Business relationships and partnerships
  - `02-Companies/Financials/` - Financial information (where applicable)
  - `02-Companies/Teams/` - Organizational structures
- **Naming**: `Company Name` format
- **Tagging**: `#company`, `#organization`, industry-specific tags

### 03-Projects
- **Purpose**: Active projects and initiatives
- **Structure**:
  - `03-Projects/Active/` - Currently active projects
  - `03-Projects/Planning/` - Projects in planning phase
  - `03-Projects/On Hold/` - Temporarily paused projects
  - `03-Projects/Completed/` - Recently completed (before archiving)
- **Naming**: `[STATUS] Project Name` or `Project Name - [TIMEFRAME]`
- **Tagging**: `#project`, status tags (`#active`, `#planning`, `#on-hold`), domain tags

### 04-Resources
- **Purpose**: Reference materials, resources, and knowledge base
- **Structure**:
  - `04-Resources/References/` - General reference materials
  - `04-Resources/Reading/` - Books, articles, papers
  - `04-Resources/Courses/` - Educational materials and courses
  - `04-Resources/Templates/` - Additional templates (beyond 06-Templates)
  - `04-Resources/Tools/` - Information about tools and software
- **Naming**: Descriptive titles following [[Naming Conventions]]
- **Tagging**: `#resource`, topic-specific tags, format tags (`#book`, `#article`, `#course`)

### 05-Archive
- **Purpose**: Long-term storage for inactive items
- **Structure**:
  - `05-Archive/People/` - Archived people profiles
  - `05-Archive/Companies/` - Archived company information
  - `05-Archive/Projects/` - Completed and archived projects
  - `05-Archive/Resources/` -Archive/Resources/` - Archived resources
- **Naming**: Same as source folders with optional archive date
- **Tagging**: Inherits original tags plus `#archived`

### 06-Templates
- **Purpose**: Reusable note templates for consistent formatting
- **Structure**:
  - `06-Templates/Meeting Notes/` - Meeting note templates
  - `06-Templates/Project Plans/` - Project planning templates
  - `06-Templates/Person Profiles/` - Person profile templates
  - `06-Templates/Company Profiles/` - Company profile templates
  - `06-Templates/Resources/` - Resource note templates
- **Naming**: Descriptive template names
- **Usage**: Access via Ctrl+P → "Insert template" or template hotkeys

### 10-System
- **Purpose**: Core system documentation and maintenance files
- **Structure**:
  - `10-System/README.md` - System overview
  - `10-System/Vault Guide.md` - Comprehensive usage guide
  - `10-System/Folder Structure.md` - This document
  - `10-System/Naming Conventions.md` - Naming standards
  - `10-System/Maintenance Checklist.md` - Maintenance procedures
  - `10-System/Changelog.md` - System change history
  - `10-System/Version History.md` - Version release details
  - `10-System/System Health.md` - Monitoring and health guidelines
- **Tagging**: `#system`, `#documentation`

### 11-Meta
- **Purpose**: Metadata and system-level notes about the vault itself
- **Structure**:
  - `11-Meta/Statistics/` - Vault statistics and metrics
  - `11-Meta/Analytics/` - Usage analytics and insights
  - `11-Meta/Backups/` - Backup records and logs
  - `11-Meta/Settings/` - Obsidian configuration notes
- **Tagging**: `#meta`, `#system-info`

### 17-System (Current Location)
- **Purpose**: Additional system documentation (legacy/organizational)
- **Note**: This folder exists for historical/organizational reasons and mirrors some 10-System content
- **Structure**: Same as 10-System
- **Tagging**: `#system`, `#documentation`

## Folder Naming Conventions
- All folders use two-digit prefixes for consistent ordering
- Prefixes indicate sequence and category:
  - `00-`: Processing/Inbox
  - `01-`: People
  - `02-`: Companies
  - `03-`: Projects
  - `04-`: Resources
  - `05-`: Archive
  - `06-`: Templates
  - `10-`: Core System
  - `11-`: Meta
  - `17-`: Additional System (historical)

## Cross-Folder Relationships
- People ↔ Companies (works_at, founded_by, invested_in)
- Companies ↔ Projects (sponsors, clients, partners)
- Projects → Resources (references, research)
- Resources ↔ People (authors, experts)
- All folders can link to any other as needed

## Maintenance Guidelines
- Review folder structure quarterly via [[Maintenance Checklist]]
- Archive inactive content regularly (see [[05-Archive/]])
- Maintain consistent naming within folders
- Update folder descriptions as structure evolves
- Archive folders older than 2 years (configurable)

## Related Documents
- [[Vault Guide]] - Comprehensive usage guide
- [[Naming Conventions]] - Naming standards and conventions
- [[Maintenance Checklist]] - Regular maintenance tasks
- [[Changelog]] - System change history
- [[Version History]] - Version release details
- [[System Health]] - Monitoring and health guidelines

## Maintenance
Review this document quarterly and update as folder structure evolves.
Last reviewed: 2026-07-10