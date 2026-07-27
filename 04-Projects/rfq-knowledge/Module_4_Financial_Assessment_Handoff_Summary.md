# Module 4: Financial Assessment Engine

**Prepared by:** Diksha Ballav

---

# Scope

This work covers:

**Module 4: Financial Assessment Engine**

The implementation estimates:

* Total development hours
* Estimated project cost
* Estimated project timeline
* Financial feasibility decision
* Recommendation based on the financial decision

---

# Module 4: Financial Assessment

## What Module 4 Does

Module 4 receives the structured RFQ JSON and performs financial calculations.

The module:

* Reads the RFQ information.
* Reads the project title.
* Reads the project budget.
* Reads the technical requirements.
* Reads the recommended team.
* Generates required roles based on the technical requirements.
* Calculates the total development hours.
* Calculates the estimated development cost.
* Adds external project costs.
* Estimates the project timeline.
* Compares the estimated cost with the project budget.
* Generates a financial decision.
* Returns the financial assessment output.

---

# Technology Used

* Python
* Math Library (`math`)

---

# Input Structure

```json
{
  "rfq_id": "",
  "project_info": {
    "title": "",
    "scope": "",
    "budget": 0,
    "timeline": "",
    "technical_requirements": [],
    "required_skills": []
  },
  "section_analysis": {
    "present_sections": [],
    "missing_sections": [],
    "completeness_score": 0
  },
  "recommended_team": [
    {
      "employee": "",
      "match_score": 0,
      "matched_skills": []
    }
  ]
}
```

---

# Input Fields Used

The Financial Engine uses the following fields:

## Root Level

* rfq_id
* project_info
* recommended_team

## project_info

* title
* budget
* technical_requirements

## recommended_team

Each object contains:

* employee
* match_score
* matched_skills

The current implementation uses only the number of employees in the recommended team.

---

# Role Generation

The module generates required roles from the technical requirements.

The following effort values are assigned.

| Technology           | Hours per Person |
| -------------------- | ---------------: |
| React                |              100 |
| Next.js              |              100 |
| TypeScript           |              100 |
| Node.js              |              120 |
| Express.js           |              120 |
| AWS                  |               80 |
| Docker               |               80 |
| GitHub Actions       |               80 |
| Any other technology |               60 |

Each generated role has:

* count = 1
* hours_per_person = assigned value

---

# Total Development Hours

The total development hours are calculated as:

```
Total Hours =
Σ (count × hours_per_person)
```

---

# Estimated Development Cost

The Financial Engine uses a fixed hourly rate.

```
Hourly Rate = €50
```

The development cost is calculated as:

```
Development Cost =
Σ (count × hours_per_person × hourly rate)
```

---

# External Project Cost

External project cost is calculated as:

```
External Cost =
Budget × 5%
```

---

# Estimated Total Cost

```
Estimated Total Cost =
Development Cost + External Cost
```

---

# Timeline Estimation

The timeline is calculated using:

* Total development hours
* Number of recommended team members
* 40 working hours per week

Formula:

```
Weekly Capacity =
Available Resources × 40

Estimated Timeline =
Ceiling(Total Hours / Weekly Capacity)
```

If the weekly capacity is 0, the estimated timeline is returned as 0.

---

# Financial Decision

The estimated total cost is compared with the project budget.

| Condition                           | Decision        |
| ----------------------------------- | --------------- |
| Estimated Total Cost ≤ Budget       | GO              |
| Estimated Total Cost ≤ Budget × 1.2 | GO WITH CAUTION |
| Estimated Total Cost > Budget × 1.2 | NO GO           |

---

# Recommendation

The recommendation returned depends on the decision.

| Decision        | Recommendation                                                                                                               |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| GO              | Project is feasible with available resources, skills, and budget.                                                            |
| GO WITH CAUTION | Project is feasible but requires mitigation actions such as hiring, training, scope clarification, or resource reallocation. |
| NO GO           | Significant skill gaps, resource limitations, financial concerns, or delivery risks make successful execution unlikely.      |

---

# Output Structure

```json
{
  "rfq_id": "",
  "project_title": "",
  "team_size": 0,
  "total_tech_requirements": 0,
  "estimated_timeline_weeks": 0,
  "estimated_total_cost": 0,
  "budget": 0,
  "decision": "",
  "recommendation": ""
}
```

---

# Output Fields

* rfq_id
* project_title
* team_size
* total_tech_requirements
* estimated_timeline_weeks
* estimated_total_cost
* budget
* decision
* recommendation

---

# Default Values

If values are missing, the following defaults are used.

| Field                  | Default Value        |
| ---------------------- | -------------------- |
| rfq_id                 | `"UNKNOWN"`          |
| project_title          | `"Untitled Project"` |
| budget                 | `0`                  |
| technical_requirements | `[]`                 |
| recommended_team       | `[]`                 |

If no recommended team members are available, the estimated timeline returned is `0`.


