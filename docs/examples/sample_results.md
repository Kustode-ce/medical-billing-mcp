# Sample Results

Example outputs from the Medical Billing MCP tools.

---

## lookup_icd10

### Direct Code Lookup
```bash
Input: {"code": "E11.9"}
```

```json
{
  "code": "E11.9",
  "description": "Type 2 diabetes mellitus without complications",
  "billable": true,
  "chapter": "E00-E89",
  "category": "Endocrine, nutritional and metabolic diseases",
  "hcc": true,
  "hcc_category": 19,
  "common_procedures": ["99213", "99214", "82947", "83036"]
}
```

### Search
```bash
Input: {"search": "heart failure"}
```

```json
{
  "results": [
    {
      "code": "I50.9",
      "description": "Heart failure, unspecified",
      "billable": true,
      "hcc": true,
      "hcc_category": 85
    },
    {
      "code": "I50.22",
      "description": "Chronic systolic (congestive) heart failure",
      "billable": true,
      "hcc": true,
      "hcc_category": 85
    },
    {
      "code": "I50.32",
      "description": "Chronic diastolic (congestive) heart failure",
      "billable": true,
      "hcc": true,
      "hcc_category": 85
    }
  ],
  "total": 3
}
```

---

## lookup_cpt

### Direct Code Lookup
```bash
Input: {"code": "99214"}
```

```json
{
  "code": "99214",
  "description": "Office visit, established patient, moderate complexity",
  "category": "E/M",
  "time_range": "30-39 minutes",
  "documentation": {
    "mdm_level": "moderate",
    "requires": ["chief_complaint", "history", "exam", "assessment", "plan"],
    "mdm_elements": {
      "problems": "1+ chronic illness with severe exacerbation OR 2+ chronic illnesses with mild exacerbation",
      "data": "Moderate (order/review tests, obtain history, discuss with external)",
      "risk": "Moderate (prescription drug management)"
    }
  },
  "common_modifiers": ["25"],
  "common_denials": ["downcoded_to_99213", "documentation_insufficient"],
  "rvu_work": 1.92
}
```

---

## lookup_modifier

```bash
Input: {"modifier": "25"}
```

```json
{
  "modifier": "25",
  "description": "Significant, separately identifiable E/M service by the same physician on the same day of a procedure",
  "use_with": ["E/M codes (99202-99215, etc.)"],
  "use_when": "E/M service is above and beyond the usual pre/post work for a procedure",
  "documentation_required": [
    "Chief complaint separate from procedure indication",
    "History and/or exam elements for separate issue",
    "Separate medical decision making"
  ],
  "common_mistakes": [
    "Using for routine pre-op evaluation",
    "No separate documentation in chart",
    "E/M only addresses issue requiring procedure"
  ],
  "audit_risk": "HIGH",
  "examples": {
    "appropriate": "Patient comes for mole removal, also has new cough requiring evaluation",
    "inappropriate": "Patient comes for mole removal, provider examines only the mole"
  }
}
```

---

## lookup_denial

```bash
Input: {"code": "CO-50"}
```

```json
{
  "code": "50",
  "description": "Non-covered service - not deemed medically necessary by payer",
  "group": "CO",
  "category": "medical_necessity",
  "resolution_steps": [
    "Review diagnosis codes - use most specific ICD-10 available",
    "Check LCD/NCD coverage criteria for this procedure",
    "Add secondary diagnoses that support medical necessity",
    "Gather clinical documentation supporting need",
    "Submit appeal with letter of medical necessity"
  ],
  "appeal_documentation": [
    "Letter from physician explaining why service was needed",
    "Relevant clinical notes and test results",
    "LCD/NCD criteria showing patient qualifies",
    "Peer-reviewed literature if off-label/unusual"
  ],
  "prevention_tips": [
    "Use most specific diagnosis code",
    "Include all relevant secondary diagnoses",
    "Document medical necessity in clinical notes before service"
  ],
  "patient_billable": false,
  "note": "CO group - cannot bill patient. Must appeal or write off.",
  "group_info": {
    "name": "Contractual Obligation",
    "description": "Amount provider agreed to write off per contract",
    "patient_billable": false
  }
}
```

---

## lookup_payer

```bash
Input: {"payer": "medicare"}
```

```json
{
  "payer_id": "medicare",
  "name": "Medicare",
  "type": "federal",
  "timely_filing_days": 365,
  "timely_filing_from": "date_of_service",
  "appeal_deadline_days": 120,
  "appeal_deadline_from": "remittance_date",
  "appeal_levels": [
    "Redetermination (120 days)",
    "Reconsideration by QIC (180 days)",
    "ALJ Hearing (60 days)",
    "Medicare Appeals Council (60 days)",
    "Federal District Court (60 days)"
  ],
  "telehealth": {
    "modifier": "95",
    "pos_codes": ["02", "10"],
    "pos_02": "Patient not at home",
    "pos_10": "Patient at home",
    "audio_only_codes": ["99441", "99442", "99443", "G2012"]
  },
  "contacts": {
    "provider_services": "1-800-MEDICARE (1-800-633-4227)",
    "website": "cms.gov"
  },
  "tips": [
    "Use modifier 95 for telehealth, not GT",
    "ABN required for non-covered services",
    "Check LCD for coverage criteria"
  ]
}
```

---

## lookup_bundling

### Bundled Codes
```bash
Input: {"codes": ["45378", "45380"]}
```

```json
{
  "codes_checked": ["45378", "45380"],
  "any_bundled": true,
  "pairs": [
    {
      "code_pair": ["45378", "45380"],
      "bundled": true,
      "column_1": "45380",
      "column_2": "45378",
      "modifier_allowed": false,
      "description": "Colonoscopy with biopsy includes diagnostic colonoscopy",
      "explanation": "When biopsy is performed, the work of diagnostic colonoscopy is included",
      "resolution": "Bill only 45380 (colonoscopy with biopsy)"
    }
  ]
}
```

### Non-Bundled Codes
```bash
Input: {"codes": ["99213", "36415"]}
```

```json
{
  "codes_checked": ["99213", "36415"],
  "any_bundled": false,
  "pairs": [
    {
      "code_pair": ["99213", "36415"],
      "bundled": false,
      "can_bill_together": true,
      "note": "No bundling rule found - verify with current CCI edits"
    }
  ]
}
```

---

## Test Results

```
$ python -m medical_billing_mcp --test

Medical Billing MCP v0.1.0
Data directory: /path/to/medical_billing_mcp/data

✅ ICD-10 lookup: OK
✅ ICD-10 search: OK
✅ CPT lookup: OK
✅ Modifier lookup: OK
✅ Denial lookup: OK
✅ Payer lookup: OK
✅ Bundling check: OK

Results: 7 passed, 0 failed
```

```
$ pytest tests/ -v

======================== test session starts ========================
tests/test_handlers.py::TestICD10Lookup::test_lookup_by_code PASSED
tests/test_handlers.py::TestICD10Lookup::test_lookup_by_code_case_insensitive PASSED
tests/test_handlers.py::TestICD10Lookup::test_lookup_not_found PASSED
tests/test_handlers.py::TestICD10Lookup::test_search PASSED
tests/test_handlers.py::TestICD10Lookup::test_no_params_returns_error PASSED
tests/test_handlers.py::TestCPTLookup::test_lookup_by_code PASSED
tests/test_handlers.py::TestCPTLookup::test_lookup_not_found PASSED
tests/test_handlers.py::TestCPTLookup::test_search PASSED
tests/test_handlers.py::TestModifierLookup::test_lookup_modifier_25 PASSED
tests/test_handlers.py::TestModifierLookup::test_lookup_modifier_59 PASSED
tests/test_handlers.py::TestModifierLookup::test_modifier_not_found PASSED
tests/test_handlers.py::TestDenialLookup::test_lookup_denial_code PASSED
tests/test_handlers.py::TestDenialLookup::test_lookup_denial_with_group PASSED
tests/test_handlers.py::TestDenialLookup::test_search_denials PASSED
tests/test_handlers.py::TestPayerLookup::test_lookup_medicare PASSED
tests/test_handlers.py::TestPayerLookup::test_lookup_not_found PASSED
tests/test_handlers.py::TestBundlingLookup::test_bundled_codes PASSED
tests/test_handlers.py::TestBundlingLookup::test_non_bundled_codes PASSED
tests/test_handlers.py::TestBundlingLookup::test_insufficient_codes PASSED
tests/test_handlers.py::TestDataLoading::test_data_files_exist PASSED
tests/test_handlers.py::TestDataLoading::test_data_files_valid_json PASSED

======================== 21 passed in 1.02s ========================
```
