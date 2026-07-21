---
title: Medication data
type: Documentation
status: Active
created: 2026-07-16
updated: 2026-07-16
---

Medication data

Data structure:
- Active ingredient
- Brand names
- Strength
- Dosage form
- Indications
- Contraindications
- Warnings
- Interactions
- Adverse effects
- Pregnancy and breastfeeding information
- Age restrictions
- Renal and hepatic considerations
- Emergency overdose information
- Regulatory safety updates
- Authorisation status

Sources:
- Germany: BfArM AMIce
- European Union: EMA

Graph structure
- (Medication)-[:HAS_INGREDIENT]->(Substance)
- (Medication)-[:CONTRAINDICATED_FOR]->(Condition)
- (Medication)-[:INTERACTS_WITH]->(Medication)
- (Medication)-[:REQUIRES_CAUTION_IN]->(Population)
- (Medication)-[:MAY_CAUSE]->(AdverseEffect)
- (Medication)-[:SUPPORTED_BY]->(ProductInformation)
- (SafetyCommunication)-[:UPDATES]->(Medication)