# Final Integration Contract

## Module 2

Input:
RFQ PDF

Output:

{
  "rfq_id": "...",
  "project_info": {},
  "section_analysis": {
    "present_sections": [],
    "missing_sections": [],
    "completeness_score": 0
  }
}

## Module 3

Output:

{
  "feasibility_analysis": {
    "feasibility_score": 0,
    "risk_level": "",
    "insolvency_risk": false,
    "estimated_cost": 0,
    "required_resources": 0,
    "estimated_discussion_hours": 0,
    "estimated_documentation_hours": 0
  }
}

## Module 4

Output:

{
  "recommended_team": [],
  "skill_gap_report": {
    "missing_skills": [],
    "gap_percentage": 0
  },
  "overall_match_score": 0
}

## Module 5

Consumes:
- Module 2 Output
- Module 3 Output
- Module 4 Output

Produces:

{
  "score": 0,
  "verdict": "",
  "issues": []
}

## Module 6

Consumes:
- Module 2
- Module 3
- Module 4
- Module 5

Produces:
- JSON Report
- Human Readable Report