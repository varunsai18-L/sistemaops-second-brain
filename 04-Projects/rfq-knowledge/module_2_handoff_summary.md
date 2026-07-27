# Module 1 and Module 2 Handoff Summary

Prepared by: Palak Nagar

## Scope

This work covers:

- Module 1: PDF Processing and structured RFQ extraction.
- Module 2: RFQ section analysis and completeness checking.

The implementation does not perform financial analysis, skill matching, decision making, or final GO / NO-GO recommendation.

## Module 1: PDF Processing and RFQ Extraction

### What Module 1 Does

1. User uploads an RFQ document through the Streamlit app.
2. The existing parser extracts text from the uploaded file.
3. The extracted text is cleaned.
4. A new RFQ ID is generated.
5. Ollama is asked to extract structured RFQ information as JSON.
6. The extracted JSON is validated before being saved.

### Technology Used

- Streamlit handles file upload.
- PyMuPDF extracts PDF text through the existing `PdfParser`.
- Python regex cleans the extracted text.
- Ollama extracts structured RFQ information.
- Pydantic validates the structured output.

### Module 1 Output Format

```json
{
  "rfq_id": "RFQ_YYYYMMDD_HHMMSS",
  "project_info": {
    "title": "",
    "scope": "",
    "budget": 0,
    "timeline": "",
    "technical_requirements": [],
    "required_skills": []
  }
}
```

### Module 1 Mandatory Fields

- `rfq_id`
- `project_info`
- `project_info.title`
- `project_info.scope`
- `project_info.budget`
- `project_info.timeline`
- `project_info.technical_requirements`
- `project_info.required_skills`

### Missing Value Handling

- Missing text fields use an empty string: `""`
- Missing budget uses `0`
- Missing list fields use an empty list: `[]`

## Module 2: Section Analysis

### What Module 2 Does

Module 2 checks whether the RFQ contains the required sections and calculates a completeness score.

Required sections currently checked:

- Project Overview / Scope
- Technical Requirements
- Deliverables
- Timeline / Schedule
- Budget / Commercial Details
- Evaluation Criteria
- Terms & Conditions
- Contact Information

The section list is configurable in code so it can be updated later.

### Completeness Score Formula

```text
completeness_score = (present required sections / total required sections) * 100
```

Example:

```text
7 sections present out of 8 = 87.5, rounded to 88
```

### Module 2 Output Format

```json
{
  "section_analysis": {
    "present_sections": [],
    "missing_sections": [],
    "completeness_score": 0
  }
}
```

### Module 2 Mandatory Fields

- `section_analysis`
- `section_analysis.present_sections`
- `section_analysis.missing_sections`
- `section_analysis.completeness_score`

## Final Saved Output

The final saved JSON combines Module 1 and Module 2 output:

```json
{
  "rfq_id": "RFQ_YYYYMMDD_HHMMSS",
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
  }
}
```

## Output Storage

Parsed text is saved in:

```text
data/parsed/
```

Final Module 1 + Module 2 JSON is saved in:

```text
data/outputs/
```

Example output file:

```text
data/outputs/RFQ_20260615_101500_Corporate_Website.json
```

The Streamlit UI does not display the full JSON body now. It shows the saved output file path.

## Error Handling

If RFQ processing fails, the system saves an error JSON file in:

```text
data/outputs/
```

Example error output:

```json
{
  "status": "error",
  "document": "file.pdf",
  "module": "module_1_structured_extraction",
  "message": "Could not connect to Ollama. Please check if Ollama is running.",
  "parsed_path": "data/parsed/file.txt",
  "created_at": "2026-06-15T10:15:00"
}
```

### Error Fields

- `status`: always `"error"` for failed processing.
- `document`: uploaded document name.
- `module`: module/stage where the error happened.
- `message`: readable error message.
- `parsed_path`: parsed text path if text extraction completed.
- `created_at`: timestamp when the error file was created.

### Current Error Module Values

- `module_1_pdf_processing`
- `module_1_structured_extraction`

## Notes

- OCR is not implemented in this phase.
- The previous summary generation flow has been replaced by structured JSON extraction.
- Successful outputs and error outputs are both saved under `data/outputs/` so downstream modules can consume them from a consistent location.
