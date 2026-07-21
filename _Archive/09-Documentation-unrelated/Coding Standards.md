---
title: Coding Standards
date: 2026-07-10
type: documentation
tags: [documentation, coding-standards, best-practices]
---

# Coding Standards

## Overview

This document outlines the coding standards and best practices for the project.

## General Principles

- Write clear, readable code
- Follow the principle of least astonishment
- Write self-documenting code where possible
- Comment complex logic, not obvious code

## Language-Specific Standards

### [Programming Language - e.g., JavaScript/TypeScript]

#### Formatting
- Indentation: 2 spaces
- Line length: Maximum 100 characters
- Semicolons: Required
- Quotes: Single quotes for strings, except when avoiding escaping

#### Naming Conventions
- Variables: camelCase
- Functions: camelCase
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private members: _prefix (if applicable)

#### Best Practices
- Use strict equality (`===`) unless type coercion is specifically needed
- Handle promises properly with async/await or .then()
- Avoid deeply nested code (aim for flat structures)
- Use meaningful variable and function names

### [Add other languages as needed]

## Code Comments

### When to Comment
- Explain why something is done, not what is done
- Document complex algorithms or business rules
- Mark temporary solutions with TODO comments
- Document public APIs

### Comment Format
- Use complete sentences
- Keep comments updated when code changes
- Remove commented-out code

## Code Reviews

### What Reviewers Look For
- Correctness and completeness
- Adherence to coding standards
- Test coverage
- Performance considerations
- Security implications

### Review Process
1. Submit pull request with clear description
2. Address reviewer comments promptly
3. Maintainers approve and merge
4. Delete feature branch after merge

## Tools

### Linting
- Configured linter rules
- How to run linter locally
- CI integration

### Formatting
- Auto-formatting tools
- Pre-commit hooks

## Related Documentation

- [[Development Guide]]
- [[API Documentation]]