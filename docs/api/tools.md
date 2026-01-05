# API Documentation

## Overview

Medical Billing MCP exposes 6 tools via the Model Context Protocol (MCP).

Each tool:
- Takes simple input parameters
- Returns structured JSON
- Is read-only (no side effects)
- Is PHI-free (codes and rules only)

---

## Tools

### `lookup_icd10`

Look up ICD-10 diagnosis codes.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "description": "ICD-10 code (e.g., 'E11.9', 'I50.9')"
    },
    "search": {
      "type": "string", 
      "description": "Search term (e.g., 'diabetes', 'heart failure')"
    }
  }
}
```

**Example - Direct Lookup:**
```json
// Input
{"code": "E11.9"}

// Output
{
  "code": "E11.9",
  "description": "Type 2 diabetes mellitus without complications",
  "billable": true,
  "chapter": "E00-E89",
  "hcc": true,
  "hcc_category": 19
}
```

**Example - Search:**
```json
// Input
{"search": "diabetes"}

// Output
{
  "results": [
    {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
    {"code": "E11.65", "description": "Type 2 diabetes mellitus with hyperglycemia"},
    {"code": "E10.9", "description": "Type 1 diabetes mellitus without complications"}
  ],
  "total": 3
}
```

---

### `lookup_cpt`

Look up CPT procedure codes.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "description": "CPT code (e.g., '99213', '45378')"
    },
    "search": {
      "type": "string",
      "description": "Search term (e.g., 'office visit', 'colonoscopy')"
    }
  }
}
```

**Example:**
```json
// Input
{"code": "99213"}

// Output
{
  "code": "99213",
  "description": "Office visit, established patient, low complexity",
  "category": "E/M",
  "time_range": "20-29 minutes",
  "documentation": {
    "requires": ["chief_complaint", "history", "assessment", "plan"],
    "mdm_level": "low",
    "time_based_alternative": true
  },
  "common_modifiers": ["25"],
  "rvu_work": 1.30
}
```

---

### `lookup_modifier`

Look up CPT/HCPCS modifiers with usage guidance.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "modifier": {
      "type": "string",
      "description": "Modifier code (e.g., '25', '59', 'TC')"
    }
  },
  "required": ["modifier"]
}
```

**Example:**
```json
// Input
{"modifier": "25"}

// Output
{
  "modifier": "25",
  "description": "Significant, separately identifiable E/M service",
  "use_with": ["E/M codes"],
  "use_when": "E/M is above and beyond the usual pre/post work for a procedure",
  "documentation_required": [
    "Separate chief complaint from procedure",
    "Separate history and/or exam elements",
    "Separate medical decision making"
  ],
  "common_mistakes": [
    "Using for routine pre-op evaluation",
    "No separate documentation in chart"
  ],
  "audit_risk": "HIGH",
  "denial_rate": "Frequently audited"
}
```

---

### `lookup_denial`

Look up CARC/RARC denial codes with resolution steps.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "description": "Denial code (e.g., 'CO-50', '50', 'PR-1')"
    },
    "search": {
      "type": "string",
      "description": "Search description (e.g., 'medical necessity')"
    }
  }
}
```

**Example:**
```json
// Input
{"code": "CO-50"}

// Output
{
  "code": "50",
  "group": "CO",
  "group_name": "Contractual Obligation",
  "description": "These are non-covered services because this is not deemed a 'medical necessity' by the payer",
  "patient_billable": false,
  "resolution_steps": [
    "Review diagnosis codes - use most specific ICD-10 available",
    "Check LCD/NCD coverage criteria for the procedure",
    "Add supporting secondary diagnoses",
    "Gather clinical documentation supporting medical necessity",
    "Submit appeal with letter of medical necessity"
  ],
  "appeal_documentation": [
    "Physician letter explaining why service was needed",
    "Relevant clinical notes and test results",
    "LCD/NCD criteria crosswalk showing patient meets requirements"
  ],
  "prevention_tips": [
    "Use most specific diagnosis code",
    "Include all relevant secondary diagnoses",
    "Document medical necessity in clinical notes"
  ]
}
```

---

### `lookup_payer`

Look up payer-specific billing rules.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "payer": {
      "type": "string",
      "description": "Payer name (e.g., 'medicare', 'bcbs_ma', 'aetna')"
    }
  },
  "required": ["payer"]
}
```

**Example:**
```json
// Input
{"payer": "medicare"}

// Output
{
  "payer": "medicare",
  "name": "Medicare",
  "type": "federal",
  "timely_filing_days": 365,
  "timely_filing_from": "date_of_service",
  "appeal_deadline_days": 120,
  "appeal_deadline_from": "remittance_date",
  "telehealth": {
    "modifier": "95",
    "pos_codes": ["02", "10"],
    "audio_only_codes": ["99441", "99442", "99443"]
  },
  "contacts": {
    "provider_services": "1-800-MEDICARE"
  }
}
```

---

### `lookup_bundling`

Check if procedure codes are bundled (CCI edits).

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "codes": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of CPT codes to check"
    }
  },
  "required": ["codes"]
}
```

**Example:**
```json
// Input
{"codes": ["99213", "36415"]}

// Output
{
  "codes_checked": ["99213", "36415"],
  "bundled": false,
  "can_bill_together": true,
  "notes": "Venipuncture (36415) can be billed separately from E/M"
}
```

**Example - Bundled:**
```json
// Input
{"codes": ["45378", "45380"]}

// Output
{
  "codes_checked": ["45378", "45380"],
  "bundled": true,
  "can_bill_together": false,
  "column_1_code": "45380",
  "column_2_code": "45378",
  "modifier_allowed": false,
  "explanation": "Diagnostic colonoscopy (45378) is included in colonoscopy with biopsy (45380)",
  "resolution": "Bill only 45380 when biopsy is performed"
}
```

---

## Error Responses

All tools return errors in a consistent format:

```json
{
  "error": "Description of what went wrong"
}
```

**Common errors:**
- `"Code X not found"` - The requested code doesn't exist in our database
- `"Provide 'code' or 'search'"` - No input parameters provided
- `"Payer X not found"` - Payer not in our database

---

## Response Codes

The MCP protocol doesn't use HTTP status codes. All responses are successful at the protocol level. Check for `error` key in response to detect issues.

---

## Rate Limits

None. This is a local server reading JSON files.

---

## Data Freshness

Data files are updated manually. Check `_meta.last_updated` in each JSON file for currency.

For production use with current data, consider the enterprise version or contribute updates via pull requests.
