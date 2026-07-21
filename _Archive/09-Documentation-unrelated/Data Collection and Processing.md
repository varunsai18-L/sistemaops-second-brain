---
title: Data Collection and Processing
type: Documentation
status: Active
domain: Healthcare Data Management
created: 2026-07-16
updated: 2026-07-16
tags: [data-collection, data-processing, healthcare, methodologies]
related: [[Healthcare Data Categories and Database Design]], [[Data Governance in Healthcare]], [[Medical AI Training Data]]
---

# Data Collection and Processing

## Overview
This document outlines the main data categories used in the healthcare system and describes how each category is stored across different database technologies including vector databases, knowledge graphs, and PostgreSQL.

## Purpose
To provide a clear mapping of healthcare data categories to appropriate storage technologies, ensuring optimal performance, scalability, and functionality for each data type while maintaining data integrity and accessibility.

## Architecture
The healthcare data architecture employs a multi-model database approach utilizing three primary storage technologies:
- **Vector Database**: For storing embeddings and enabling similarity searches
- **Knowledge Graph**: For representing relationships and connections between entities
- **PostgreSQL**: For structured data storage with strong consistency and ACID properties

This hybrid approach allows each data type to be stored in the most appropriate technology based on its access patterns, query requirements, and relationship characteristics.

## Data Categories
The system manages nine main categories of healthcare data:

1. Clinical guidelines and recommendations
2. Symptoms, conditions and triage relationships
3. Medical terminology and coding systems
4. Medication and safety information
5. Patient-record structure
6. Synthetic patient cases
7. Public-health and epidemiological data
8. Evaluation and golden-test cases
9. Operational and feedback data

## Database Design
The following table shows where each data category is stored across the different database technologies:

| Data Category                | Vector Database                | Knowledge Graph                     | PostgreSQL         |
| ---------------------------- | ------------------------------ | ----------------------------------- | ------------------ |
| Guideline paragraphs         | Yes                            | References to find related articles | Metadata           |
| Clinical recommendations     | Yes                            | Yes                                 | Version metadata   |
| Conditions and symptoms      | Descriptions/synonyms          | Yes                                 | IDs and releases   |
| SNOMED concepts              | Optional embeddings            | Yes                                 | Terminology tables |
| ICD (disease codes) mappings | No                             | Yes                                 | Yes                |
| Medication product documents | Yes                            | Yes                                 | Product metadata   |
| Drug interactions            | Supporting text                | Yes                                 | Yes                |
| FHIR patient records         | No (but consider in future)    | Temporary/context graph only        | Yes/FHIR store     |
| Synthetic patient data       | Only synthetic notes if needed | Test graph                          | Test database      |
| Public-health statistics     | Reports only                   | Selected relationships              | Yes                |
| Golden tests                 | Expected evidence              | Expected paths                      | Test repository    |
| Source licences              | No                             | No                                  | Yes                |

## References
- [[Healthcare Data Standards]]
- [[Medical Coding Systems]]
- [[FHIR Specification]]
- [[SNOMED CT]]
- [[ICD-10 Coding]]
- [[Vector Database Applications in Healthcare]]
- [[Knowledge Graphs for Medical Data]]
- [[PostgreSQL for Healthcare Applications]]

## Related Notes
- [[Medical Terminology Management]] - Details on handling medical coding systems
- [[Patient Data Modeling]] - Structure and relationships of patient records
- [[Clinical Decision Support Systems]] - How guidelines and recommendations are used
- [[Public Health Surveillance]] - Epidemiological data collection and analysis
- [[Healthcare Data Integration]] - Strategies for combining data from multiple sources
- [[Data Governance in Healthcare]] - Policies and procedures for healthcare data management
- [[Medical AI Training Data]] - Synthetic patient data generation and usage
- [[Healthcare Analytics Platform]] - Evaluation and testing frameworks

## Source
Source: XWiki page - Main data categories and database design