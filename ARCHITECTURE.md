# Medical Billing MCP - Architecture

## Overview

An open-source MCP server that gives AI assistants medical billing **knowledge**.
This is a reference layer - users already have their own payer connections (Stedi, Availity, etc.).

---

## What This Is (and Isn't)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THIS TOOL IS:                                     │
│                                                                         │
│  A KNOWLEDGE LAYER                                                      │
│                                                                         │
│  • "What does denial code CO-50 mean?"                                 │
│  • "What modifier do I need for E/M with procedure?"                   │
│  • "What's Medicare's timely filing limit?"                            │
│  • "Are these two codes bundled?"                                      │
│  • "What documentation do I need for 99214?"                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        THIS TOOL IS NOT:                                 │
│                                                                         │
│  • NOT a clearinghouse                                                  │
│  • NOT submitting claims                                                │
│  • NOT checking eligibility                                             │
│  • NOT connecting to payers                                             │
│                                                                         │
│  Users already have: Stedi, Availity, Change Healthcare, direct APIs   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The Problem We're Solving

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CURRENT STATE                                     │
│                                                                         │
│  Staff gets denial → Opens Google → Searches "CO-50 denial" →          │
│  Reads 5 articles → Still confused → Calls payer → Hold 45 min →       │
│  Maybe gets answer                                                      │
│                                                                         │
│  Cost: 30-60 min per denial just to UNDERSTAND it                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        WITH THIS TOOL                                    │
│                                                                         │
│  Staff asks AI → Instant answer with resolution steps →                │
│  Fix claim → Resubmit via Stedi/Availity/etc.                          │
│                                                                         │
│  Cost: 2 minutes                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Design Principles

1. **PHI-Free by Design**
   - Only billing codes and rules
   - No patient data ever touches this system
   - Safe to run locally, safe to contribute to

2. **Data-Driven**
   - All billing knowledge in JSON files
   - Easy for community to add/update
   - No code changes needed to add a payer or code

3. **Simple > Clever**
   - Readable code over clever code
   - One file per concept
   - Comments explain the "why"

4. **Community-First**
   - MIT license
   - Easy contribution workflow
   - Clear data formats

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP CLIENT (Claude, etc.)                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ MCP Protocol (stdio)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP SERVER                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        server.py                                  │   │
│  │  - Lists available tools                                         │   │
│  │  - Routes tool calls to handlers                                 │   │
│  │  - Returns results                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                    ┌───────────────┼───────────────┐                    │
│                    ▼               ▼               ▼                    │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐        │
│  │  codes.py        │ │  denials.py      │ │  payers.py       │        │
│  │                  │ │                  │ │                  │        │
│  │  - ICD-10 lookup │ │  - CARC/RARC     │ │  - Timely filing │        │
│  │  - CPT lookup    │ │  - Resolution    │ │  - Auth rules    │        │
│  │  - Modifiers     │ │    steps         │ │  - Contacts      │        │
│  └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘        │
│           │                    │                    │                   │
│           ▼                    ▼                    ▼                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         data/                                    │   │
│  │                                                                  │   │
│  │  icd10.json    - Diagnosis codes                                │   │
│  │  cpt.json      - Procedure codes                                │   │
│  │  modifiers.json - Modifier reference                            │   │
│  │  denials.json  - CARC/RARC codes + resolution steps             │   │
│  │  payers.json   - Payer-specific rules                           │   │
│  │  bundling.json - CCI edit pairs                                 │   │
│  │                                                                  │   │
│  │  [Community contributes here]                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
medical-billing-mcp/
│
├── src/medical_billing_mcp/
│   ├── __init__.py              # Version, exports
│   ├── __main__.py              # python -m medical_billing_mcp
│   ├── server.py                # MCP server (tools + routing)
│   ├── handlers.py              # All lookup functions (simple, one file)
│   │
│   └── data/                    # JSON knowledge base
│       ├── icd10.json           # Diagnosis codes
│       ├── cpt.json             # Procedure codes  
│       ├── modifiers.json       # Modifier reference
│       ├── denials.json         # CARC/RARC + resolution
│       ├── payers.json          # Payer rules
│       └── bundling.json        # Common bundled pairs
│
├── tests/
│   └── test_handlers.py         # Test the lookups work
│
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

~10 files total. Anyone can understand it in 5 minutes.

---

## Data Schema Design

### Why JSON?
- Human-readable
- Easy to edit
- Easy to diff/review in PRs
- No database needed

### icd10.json
```json
{
  "_meta": {
    "description": "ICD-10-CM diagnosis codes",
    "source": "CMS",
    "version": "2026"
  },
  "codes": {
    "E11.9": {
      "description": "Type 2 diabetes mellitus without complications",
      "billable": true,
      "hcc": true,
      "hcc_category": 19,
      "chapter": "E00-E89",
      "common_procedures": ["99213", "99214", "82947"]
    }
  }
}
```

### cpt.json
```json
{
  "_meta": {
    "description": "CPT codes - descriptions only (AMA copyright)",
    "note": "Full CPT requires AMA license"
  },
  "codes": {
    "99213": {
      "description": "Office visit, established patient, low complexity",
      "category": "E/M",
      "time_range": "20-29 minutes",
      "documentation": {
        "requires": ["chief_complaint", "history", "assessment", "plan"],
        "mdm_level": "low"
      },
      "common_modifiers": ["25"],
      "common_denials": ["upcoding", "bundled_with_procedure"]
    }
  }
}
```

### modifiers.json
```json
{
  "25": {
    "description": "Significant, separately identifiable E/M service",
    "use_with": ["E/M codes"],
    "use_when": "E/M is separate from procedure on same day",
    "documentation_required": [
      "Separate chief complaint",
      "Separate history/exam",
      "Separate medical decision making"
    ],
    "common_mistakes": [
      "Using for routine pre-op eval",
      "No separate documentation"
    ],
    "audit_risk": "HIGH"
  }
}
```

### denials.json
```json
{
  "_meta": {
    "description": "CARC/RARC denial codes with resolution steps",
    "source": "X12 / Washington Publishing Company"
  },
  "codes": {
    "CO-50": {
      "description": "Not deemed medically necessary",
      "group": "CO",
      "category": "medical_necessity",
      "resolution_steps": [
        "Review diagnosis codes - use most specific",
        "Check LCD/NCD coverage criteria",
        "Gather supporting documentation",
        "Submit appeal with letter of medical necessity"
      ],
      "appeal_documentation": [
        "Physician letter explaining necessity",
        "Relevant clinical notes",
        "Test results supporting need"
      ],
      "prevention_tips": [
        "Use most specific ICD-10 code",
        "Include supporting secondary diagnoses",
        "Document why service was needed"
      ]
    }
  },
  "groups": {
    "CO": {
      "name": "Contractual Obligation",
      "patient_billable": false
    },
    "PR": {
      "name": "Patient Responsibility", 
      "patient_billable": true
    }
  }
}
```

### payers.json
```json
{
  "_meta": {
    "description": "Payer-specific billing rules",
    "note": "Rules vary by plan - always verify"
  },
  "payers": {
    "medicare": {
      "name": "Medicare",
      "type": "federal",
      "timely_filing_days": 365,
      "appeal_deadline_days": 120,
      "telehealth": {
        "modifier": "95",
        "pos_codes": ["02", "10"]
      },
      "contacts": {
        "provider_services": "1-800-MEDICARE"
      }
    },
    "bcbs_ma": {
      "name": "Blue Cross Blue Shield Massachusetts",
      "type": "commercial",
      "state": "MA",
      "timely_filing_days": 90,
      "known_issues": [
        "Inconsistent processing across plans",
        "May process same service differently on same EOB"
      ]
    }
  }
}
```

---

## Tool Design

### Community Edition Tools

Pure knowledge lookups - no validation logic that could be wrong.

| Tool | Question it answers |
|------|---------------------|
| `lookup_icd10` | "What is diagnosis code E11.9?" |
| `lookup_cpt` | "What is procedure code 99213?" |
| `lookup_modifier` | "When do I use modifier 25?" |
| `lookup_denial` | "What does CO-50 mean and how do I fix it?" |
| `lookup_payer` | "What's Medicare's timely filing limit?" |
| `lookup_bundling` | "Are 99213 and 36415 bundled?" |

### Tool Behavior

Each tool does ONE thing:
- Takes a code or search term
- Returns structured information from JSON
- No business logic, no validation, no "smart" features

**Why no validation tools?**
- Validation logic can be wrong
- Payer rules change constantly  
- Better to give knowledge, let user decide
- Enterprise version can add validated rules

---

## Handler Design

Keep it simple - just load JSON and search.

```python
# handlers/codes.py

import json
from pathlib import Path

_cache = {}

def load_data(data_dir: Path, filename: str) -> dict:
    """Load JSON file with caching."""
    if filename not in _cache:
        path = data_dir / filename
        _cache[filename] = json.loads(path.read_text())
    return _cache[filename]


def lookup_icd10(data_dir: Path, code: str = None, search: str = None) -> dict:
    """
    Look up ICD-10 diagnosis code.
    
    Examples:
        lookup_icd10(data_dir, code="E11.9")
        lookup_icd10(data_dir, search="diabetes")
    """
    data = load_data(data_dir, "icd10.json")
    
    if code:
        code = code.upper().strip()
        if code in data["codes"]:
            return {"code": code, **data["codes"][code]}
        return {"error": f"Code {code} not found"}
    
    if search:
        search = search.lower()
        matches = [
            {"code": k, **v}
            for k, v in data["codes"].items()
            if search in v["description"].lower()
        ]
        return {"results": matches[:20], "total": len(matches)}
    
    return {"error": "Provide 'code' or 'search'"}
```

That's it. No classes, no inheritance, no framework. Just functions.

---

## Contribution Workflow

### Adding a New Payer

1. Fork repo
2. Edit `data/payers.json`
3. Add payer entry with timely filing, contacts, known issues
4. Submit PR with source documentation

### Adding Denial Resolution Steps

1. Fork repo
2. Edit `data/denials.json`
3. Add resolution steps based on real-world experience
4. Submit PR describing what worked

### Adding Codes

1. Fork repo
2. Edit appropriate JSON file
3. Include source (CMS, etc.)
4. Submit PR

---

## Enterprise Extension Points

Community edition provides core knowledge. Enterprise expands depth:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMMUNITY vs ENTERPRISE                               │
│                                                                         │
│  COMMUNITY (This Repo - Free)              ENTERPRISE (Private - Paid)  │
│  ─────────────────────────────             ───────────────────────────  │
│  • Common ICD-10 codes                     • Full ICD-10 database       │
│  • Common CPT codes                        • Full CPT with RVUs         │
│  • Top 50 denial codes                     • All CARC/RARC codes        │
│  • Major payer rules                       • All payer rules + contracts│
│  • Basic bundling pairs                    • Full CCI edit database     │
│  • Manual data updates                     • Auto-updated from CMS      │
│                                            • LCD/NCD coverage rules     │
│                                            • Specialty-specific guides  │
│                                            • Custom denial analytics    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

The enterprise version imports community as a dependency and extends it.

---

## What's NOT in Scope (By Design)

This is a **knowledge layer**. Users bring their own payer connectivity.

| NOT in scope | Why | User already has |
|--------------|-----|------------------|
| Claim submission | Not our job | Stedi, Availity, Change HC |
| Eligibility checks | Real-time payer data | Stedi, payer portals |
| Prior auth submission | Payer integration | Stedi, Cohere, eviCore |
| EOB/ERA parsing | Clearinghouse function | Stedi, clearinghouse |
| PHI storage | Security/compliance | User's EHR/PMS |

We provide the **knowledge** to interpret and act on what those systems return.

---

## Next Steps

1. **Build server.py** - 6 tools, ~200 lines
2. **Build handlers.py** - 6 lookup functions, ~150 lines  
3. **Seed data files** - Common codes, top denials, major payers
4. **Test locally** - Verify MCP protocol works with Claude Desktop
5. **Push to GitHub** - MIT license, open for contributions
6. **Announce** - LinkedIn, healthcare tech communities

Total code: ~400 lines. Ship in one session.

---

## Confirmed Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Scope | Knowledge layer only | Users have Stedi/Availity for connectivity |
| Tools | 6 pure lookups | No validation logic that could be wrong |
| Data | JSON files | Easy to contribute, review, update |
| Handlers | Simple functions | No classes, no framework overhead |
| File count | ~10 files | Anyone can understand in 5 minutes |

---

Ready to code.

