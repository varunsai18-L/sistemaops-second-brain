# Template Standards

## Overview
This document establishes standards for creating and using templates in the Obsidian vault to ensure consistency, efficiency, and maintainability of knowledge assets.

## Purpose
To provide standardized templates that:
- Ensure consistent structure and formatting across similar note types
- Reduce cognitive load when creating new notes
- Capture essential metadata and structure automatically
- Facilitate processing, searching, and knowledge synthesis
- Maintain quality standards across the knowledge base

## Template Philosophy

### 1. Purpose-Driven Design
- Each template should serve a specific, well-defined purpose
- Templates should capture the essential structure for their use case
- Avoid over-engineering; simplicity often yields better adoption

### 2. Consistency Over Flexibility
- Standardized structure enables better processing and querying
- Consistent templates make knowledge more predictable and usable
- Allow controlled flexibility where genuinely needed

### 3. Metadata-First Approach
- Capture essential metadata at creation time
- Use frontmatter for structured data that enables querying and processing
- Design templates for work

### 4. Progressive Disclosure
- Templates should provide the note content
- Use templates to capture immediate needs without overwhelming users
 allowing for progressive elaboration as needed
### 5. Evolving Standards
- Templates should evolve based on usage and feedback
- Regular reviews ensure templates remain relevant and effective
- Deprecate templates that no longer serve their intended purpose

## Template Categories

### 1. Core Templates
Templates for fundamental note types that form the backbone of the knowledge system

### 2. Domain-Specific Templates
Templates tailored to specific areas of knowledge or activity

### 3. Process Templates
Templates for capturing processes, procedures, and workflows

### 4. Reference Templates
Templates for source materials, references, and external resources

### 5. Meeting and Communication Templates
Templates for meetings, calls, interviews, and other interactions

### 6. Creative and Brainstorming Templates
Templates for ideation, brainstorming, and creative work

## Template Structure Standards

### 1. Frontmatter Standards
All templates should include standardized frontmatter fields where applicable:

```yaml
---
# Essential Identifiers
id: unique-identifier  # Optional: for explicit referencing
alias: [Alternative Name, Another Alias]
tags: [primary-tag, secondary-tag]

# Temporal Metadata
created: 2024-01-15
modified: 2024-01-15
date: 2024-01-15  # For time-specific notes

# Source and Attribution
source: "Source Name or URL"
author: "Author Name"
reference: "Full citation reference"

# Classification and Status
type: note-type  # e.g., meeting-note, literature-note, project-plan
status: draft|review|published|archived
priority: low|medium|high
confidence: low|medium|high  # For factual claims

# Project and Context
project: project-name-or-id
context: context-description
related: [[Related Note 1]], [[Related Note 2]]

# Custom Fields (domain-specific as needed)
# Example for literature notes:
#   author: "Author Name"
#   publication: "Journal Name"
#   year: 2024
#   doi: "10.1234/example.doi"
#   url: "https://example.com"
#   tags: [literature-note, topic-specific-tag]

---
```

### 2. Content Structure
Templates should follow a logical flow:

1. **Optional YAML Frontmatter** (as defined above)
2. **Header with Note Title** (usually matching the filename)
3. **Optional Summary/Abstract** (1-2 sentence overview)
4. **Main Content Sections** (specific to template type)
5. **Optional Sections** (as needed for the specific use case)
6. **References and Sources** (if applicable)
7. **Tags** (if not fully covered in frontmatter, or for additional context tags)

### 3. Section Naming Conventions
Use consistent, descriptive section headers:

- `## Summary` or `## Abstract` - Brief overview
- `## Key Points` or `## Main Ideas` - Core takeaways
- `## Details` or `## Content` - Main body content
- `## Analysis` or `## Reflection` - Personal interpretation or analysis
- `## Questions` or `## Open Issues` - Unanswered questions or concerns
- `## Action Items` or `## Next Steps` - Concrete actions to take
- `## Related` or `## See Also` - Related notes or resources
- `## References` or `## Sources` - Source citations
- `## Metadata` - Additional metadata not in frontmatter

## Specific Template Standards

### 1. Meeting Notes Template
```markdown
---
title: "{{title}}"
date: {{date}}
meeting-time: "{{meeting-time}}"
attendees: [{attendees}]
absentees: [{absentees}]
project: "{{project}}"
tags: [meeting-note, project-{{project-slug}}]
meeting-type: "{{meeting-type}}"  # e.g., standup, planning, review, retrospective
---

# {{title}}

**Date:** {{date}}
**Time:** {{meeting-time}}
**Project:** {{project}}
**Attendees:** {{attendees}}
**Absentees:** {{absentees}}
**Meeting Type:** {{meeting-type}}

## Agenda
- [ ] Agenda item 1
- [ ] Agenda item 2
- [ ] Agenda item 3

## Discussion Summary
### Topic 1
- Key points discussed
- Decisions made
- Open questions

### Topic 2
- Key points discussed
- Decisions made
- Open questions

## Decisions Made
- Decision 1: [Description]
- Decision 2: [Description]

## Action Items
- [ ] Action 1: Assignee :: Due Date
- [ ] Action 2: Assignee :: Due Date
- [ ] Action 3: Assignee :: Due Date

## Next Steps
- Next meeting: {{next-meeting-date}}
- Topics for next meeting:
 
 
```

### 2. Literature Notes Template
```markdown
---
title: "{{title}}"
author: "{{author}}"
publication: "{{publication}}"
year: {{year}}
doi: "{{doi}}"
url: "{{url}}"
tags: [literature-note, topic-{{topic-tag}}, type-{{source- Author: {{author}}
- **Publication:** {{publication}}
- **Year:** {{year}}
- **DOI:** {{doi}}
- **URL:** {{url}}
- **Date Accessed:** {{date}}

## Abstract:** {{abstract}}

## Key Takeaways
- Main argument or findings: 
- Key evidence or data:
- Theoretical framework:
- Limitations noted by authors:

## Personal Notes and Reflections
- How this relates to my work/interests:
- Questions this raises:
- Ideas for application or experimentation:
- Connections to other works:
- Critiques or considerations:

## Quotes and Excerpts
> "Quote text here" (p. ##)

> Another relevant quote (p. ##)

## References and Related Works
- [[Related Paper/Book Title]]
- [[Concept or Theory Referenced]]

```

### 3. Project Plan Template
```markdown
---
title: "{{title}}"
project: "{{project}}"
status: planning|active|on-hold|completed|cancelled
priority: low|medium|high
start-date: "{{start-date}}"
target-end-date: "{{target-end-date}}"
actual-end-date: "{{actual-end-date}}"
tags: [project-plan, project-{{project-slug}}, status-{{status}}]
---

# {{title}}

## Project Overview
- **Objective:** [Clear statement of what the project aims to achieve]
- **Scope:** [In-scope and out-of-scope items]
- **Stakeholders:** [List of key stakeholders and their roles]
- **Success Criteria:** [How project success will be measured]

## Timeline and Milestones
| Milestone | Target Date | Actual Date | Status |
|-----------|-------------|-------------|---------|
| Milestone 1 | {{date}} |  |  |
| Milestone 2 | {{date}} |  |  |
| Project Completion | {{target-end-date}} |  |  |

## Work Breakdown Structure
### Phase 1: [Phase Name]
- Task 1.1: [Description] :: Owner :: Due Date
- Task 1.2: [Description] :: Owner :: Due Date
- Task 1.3: [Description] :: Owner :: Due Date

### Phase 2: [Phase Name]
- Task 2.1: [Description] :: Owner :: Due Date
- Task 2.2: [Description] :: Owner :: Due Date

## Resources and Budget
### Personnel
- Role 1: [Name/allocation]
- Role 2: [Name/allocation]

### Budget
- Item 1: [Description] :: Cost
- Item 2: [Description] :: Cost
- **Total Estimated Cost:** [Amount]

## Risks and Mitigations
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|---------|---------------------|
| Risk 1 | Medium | High | [Mitigation approach] |
| Risk 2 | Low | Medium | [Mitigation approach] |

## Communication Plan
- **Regular Updates:** [Frequency and format]
- **Stakeholder Meetings:** [Schedule and attendees]
- **Reporting:** [What, to whom, and how often]

## Dependencies and Assumptions
### Dependencies
- [List of external dependencies]

### Assumptions
- [List of key assumptions underlying the plan]

## Approvals
- **Project Sponsor:** ___________________  Date: _________
- **Project Manager:** ___________________  Date: _________
- **Stakeholder Representative:** _________  Date: _________
```

### 4. Daily Notes Template
```markdown
---
date: {{date}}
day-of-week: "{{day}}"
tags: [daily-note, day-of-week-{{day-lower}}]
---

# {{date}} - {{day}}

## Schedule
- [ ] Time-blocked activity 1
- [ ] Time-blocked activity 2
- [ ] Meeting: [Topic] · [Time]

## Priorities
### Top 3 for Today
1. [ ] Priority 1
2. [ ] Priority 2
3. [ ] Priority 3

### Other Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Morning Pages / Brain Dump
[Free-form thinking, concerns, ideas]

## Meetings and Events
### [[Meeting Title]]
**Time:** [Time]
**Attendees:** [List]
**Notes:**
- Key discussion points
- Decisions made
- Action items

## Reflections and Lessons Learned
[End-of-day reflection on what went well, what could be improved, insights gained]

## Gratitude and Wins
- [ ] Gratitude item 1
- [ ] Gratitude item 2
- [ ] Win 1
- [ ] Win 2

## Tomorrow's Preparation
- [ ] Preparation task 1
- [ ] Preparation task 2

## Links and Resources Created Today
- [[New Note Created]]
- [[Another New Note]]
```

### 5. Atomic Note / Zettelkasten Template
```markdown
---
title: "{{title}}"
tags: [atomic-note, topic-{{topic-tag}},concept-{{concept-tag}}]
created: {{date}}
modified: {{date}}
---

# {{title}}

## Core Idea
[One-sentence summary of the core concept or idea]

## Elaboration
[Detailed explanation of the concept, including nuances and boundaries]

## Examples and Applications
- **Example 1:** [Concrete example illustrating the concept]
- **Application 1:** [How this concept can be applied in practice]
- **Counterexample:** [When the concept does not apply or its limitations]

## Connections and Relationships
- **Related Concept:** [[Related Concept Name]] - [Brief explanation of relationship]
- **Contrasts with:** [[Contrasting Concept]] - [How they differ]
- **Builds upon:** [[Foundational Concept]] - [How it extends or builds on prior knowledge]
- **Leads to:** [[Related Concept]] - [What this concept leads to or enables]

## Questions and Open Issues
- [Question 1 related to this concept]
- [Question 2 about applications or implications]
- [Consideration about edge cases or limitations]

## Sources and References
- [[Source or Reference Note]]
- [External Source Citation]

## Tags for Discovery
#concept #topic-[[topic-tag]] #related-[[related-concept]]
```

### Alternative Format
```markdown
---
title: "{{title}}"
tags: [atomic-note]
created: {{date}}
modified: {{date}}
type: atomic-note
status: evergreen
---

# {{title}}

> "Concise definition or key insight" (if applicable)

## Explanation
[Clear, concise explanation of the concept - aim for 3-5 sentences]

## Key Characteristics
- Characteristic 1
- Characteristic 2
- Characteristic 3

## Examples
- **Concrete Example 1:** [Brief description]
- **Concrete Example 2:** [Brief description]

## Related Notes
- See also: [[Related Concept 1]]
- See also: [[Related Concept 2]]
- Contrasts with: [[Contrasting Concept]]
- Builds upon: [[Foundational Concept]]

## Applications
- Application in context A
- Application in context B

## Sources
- [Source 1 citation]
- [Source 2 citation]
- Personal insight/experience

## Tags
#concept #topic-area #specific-subtopic
```

### 6. Book Notes Template
```markdown
---
title: "{{title}}"
author: "{{author}}"
publication-year: {{year}}
isbn: "{{isbn}}"
publisher: "{{publisher}}"
tags: [book-note,non-fiction,topic-{{topic-tag}}]
---

# {{title}} by {{author}}

## Bibliographic Information
- **Title:** {{title}}
- **Author:** {{author}}
- **Publication Year:** {{year}}
- **Publisher:** {{publisher}}
- **ISBN:** {{isbn}}
- **Format:** [Hardcover/Paperback/Ebook/Audiobook]
- **Date Started:** {{date-started}}
- **Date Completed:** {{date-completed}}

## Summary
[2-3 paragraph summary of the book's main argument, purpose, and coverage]

## Core Arguments and Takeaways
### Main Thesis
[Concise statement of the book's central argument]

### Key Parts/Sections
- **Part 1:** [Main focus and key points]
- **Part 2:** [Main focus and key points]
- **Part 3:** [Main focus and key points]

### Key Takeaways
1. **Takeaway 1:** [Detailed explanation]
2. **Takeaway 2:** [Detailed explanation]
3. **Takeaway 3:** [Detailed explanation]
4. **Takeaway 4:** [Detailed explanation]

## Chapter-by-Chapter Notes
### Chapter 1: [Chapter Title]
- Key point 1
- Key point 2
- Notable quote: "..." (p. ##)

### Chapter 2: [Chapter Title]
- Key point 1
- Key point 2
- Notable quote: "..." (p. ##)

[Continue for each chapter or major section]

## Notable Quotes and Passages
> "Quote that captures a key idea" (p. ##)
> 
> **Why this matters:** [Brief explanation of significance]

> "Another important quote" (p. ##)
> 
> **Context:** [Brief context]
> **Implication:** [Why this is significant]

## Critique and Evaluation
### Strengths
- What the book does particularly well
- Unique contributions or perspectives
- Quality of evidence and argumentation

### Weaknesses and Limitations
- Areas where the argument falls short
- Gaps in evidence or coverage
- Potential biases or blind spots
- Sections that could be improved

### Comparison to Related Works
- How this compares to [Similar Book 1]
- What this adds that [Similar Book 2] doesn't cover
- Alternative perspectives on the same topic

## Personal Application and Reflection
### Immediate Applications
- [Specific action I can take this week]
- [Practice I want to implement]
- [Conversation I want to have]

### Longer-Term Considerations
- [Idea to explore further]
- [Skill I want to develop based on this]
- [Perspective shift I'm considering]

### Questions Raised
- [Question 1 about implications or applications]
- [Question 2 about contradictions or unresolved issues]
- [Question 3 for further exploration]

## Connections to Other Knowledge
### Related Books
- [[Related Book Title]] - [How they relate/complement/contrast]
- [[Another Related Book]] - [Connection explanation]

### Related Concepts
- [[Concept from Another Domain]] - [Connection explanation]
- [Field or Discipline] concept: [How it connects]

## Action Plan
| Action | Timeline | Resources Needed | Status |
|--------|----------|------------------|---------|
| Action 1 | [Timeframe] | [What's needed] | ☐ |
| Action 2 | [Timeframe] | [What's needed] | ☐ |
| Action 3 | [Timeframe] | [What's needed] | ☐ |

```

## Template Usage Guidelines

### 1. Template Selection
- Choose the template that most closely matches your intended note type
- When in doubt, start with a simpler template and evolve it as needed
- Consider creating a hybrid template if no existing template fits perfectly

### 2. Customization Principles
- Customize templates to fit your specific needs, but maintain core structure
- Document any significant deviations from standard templates
- Share useful customizations with the team if in a collaborative vault

### 3. Template Maintenance
- Review templates quarterly for effectiveness
- Update templates based on usage patterns and feedback
- Deprecate templates that consistently fail to meet their intended purpose
- Version significant template changes when in collaborative environments

### 4. Creating New Templates
When creating a new template:
1. **Define the Purpose:** Clearly state what type of note this template is for
2. **Analyze Examples:** Look at existing good examples of this note type
3. **Identify Core Elements:** What elements consistently appear in effective notes of this type?
4. **Structure Logically:** Organize elements in a natural flow of thought or work
5. **Include Essential Metadata:** What structured data would enable better processing?
6. **Test and Refine:** Use the template for real notes and adjust based on experience
7. **Document Usage:** Add usage notes to the template itself if needed

### 5. Template Sources and Attribution
- When adapting templates from external sources, note the adaptation
- Create attribution notes for templates that significantly derive from others' work
- Consider publishing useful templates back to the community when appropriate

## Template Storage and Access

### 1. Template Location
Store templates in a dedicated folder:
```
00-Templates/
├── 01-Core/
│   ├── meeting-note.md
│   ├── literature-note.md
│   ├── project-plan.md
│   ├── daily-note.md
│   ├── atomic-note.md
│   └── book-note.md
├── 02-Domain-Specific/
│   ├── research-note.md
│   ├── design-note.md
│   └── meeting-note-client.md
├── 03-Process-Templates/
│   ├── retrospective-template.md
│   ├── retrospective-type.md
│   └── [
├── 0 inder
├── 02-Dom
├── 03-Proce
├── 04-Refe
├── 05-Meet
```
.

### 2. Template Access Methods
- Use the built-in Templates core plugin with the template folder configured
- Use templater or similar plugins for more complex template needs
- Consider using folder templates for automatic template application
- Create template notes with clear naming and documentation

### 3. Template Naming Convention
Use clear, descriptive names:
- `[type]-[purpose].md` (e.g., `meeting-note-standard.md`)
- `[domain]-[type].md` (e.g., `research-literature-note.md`)
- `[purpose]-template.md` (e.g., `project-retrospective-template.md`)

## Special Template Features

### 1. Date and Time Placeholders
- Use `{{date}}` for current date (YYYY-MM-DD)
- Use `{{time}}` for current time (HH:mm)
- Use `{{day}}` for day of week (Monday, etc.)
- Use `{{month}}` for month name
- Use `{{year}}` for four-digit year

### 2. Interactive Prompts
When using Templater or similar:
- `tp.user.prompt("Enter meeting title:")` for user input
- `tp.date.now("YYYY-MM-DD")` for formatted dates
- `tp.file.title()` for current filename
- `tp.webpage.get_url()` for clipboard URL capture

### 3. Conditional Sections
For advanced templating:
- Show/hide sections based on template variables
- Include different sections based on note type or purpose
- Create modular templates that can be combined

## Related Documents
- [[01-System Architecture]]
- [[02-Naming Conventions]]
- [[03-Linking Guidelines]]
- [[05-Maintenance Procedures]]
- [[06-Backup Procedures]]
- [[07-Glossary]]
-appendix]]
- [[08-Change Log]]

## Maintenance
This document should be reviewed semi-annually to ensure template standards remain effective and relevant.

## Change Log
See [[08-Change Log]] for detailed version history.