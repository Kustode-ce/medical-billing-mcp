# Contributing to Medical Billing MCP

Thank you for your interest in contributing! This project helps healthcare providers spend less time fighting insurance bureaucracy.

## Quick Start

The easiest way to contribute is to **add data** - no code required!

### Add Payer Rules

1. Fork the repo
2. Edit `src/medical_billing_mcp/data/payers.json`
3. Add your payer's rules:

```json
{
  "bcbs_tx": {
    "name": "Blue Cross Blue Shield Texas",
    "type": "commercial",
    "state": "TX",
    "timely_filing_days": 95,
    "known_issues": [
      "Requires detailed modifier 25 documentation"
    ],
    "tips": [
      "Submit authorization requests at least 5 days in advance"
    ]
  }
}
```

4. Submit a PR with source (payer manual, personal experience)

### Add Denial Resolution Steps

1. Fork the repo
2. Edit `src/medical_billing_mcp/data/denials.json`
3. Add or improve resolution steps:

```json
{
  "CO-151": {
    "description": "Payment adjusted - frequency of services",
    "group": "CO",
    "resolution_steps": [
      "Check payer's frequency limits for this code",
      "Document medical necessity for additional services",
      "Appeal with clinical justification"
    ]
  }
}
```

4. Submit a PR describing what worked for you

### Add Codes

Edit the appropriate file in `src/medical_billing_mcp/data/`:
- `icd10.json` - Diagnosis codes
- `cpt.json` - Procedure codes
- `modifiers.json` - Modifier reference
- `bundling.json` - Bundled code pairs

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/medical-billing-mcp.git
cd medical-billing-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run the self-test
python -m medical_billing_mcp --test
```

## Code Style

- **Format:** Run `black src tests` before committing
- **Lint:** Run `ruff check src tests`
- **Simple > Clever:** Write readable code
- **Comments:** Explain the "why", not the "what"

## Pull Request Process

1. Fork and create a feature branch
2. Make your changes
3. Run tests: `pytest tests/ -v`
4. Format code: `black src tests`
5. Submit PR with clear description

### PR Checklist

- [ ] Tests pass
- [ ] Code is formatted
- [ ] Data changes include source/reference
- [ ] Description explains what and why

## Data Quality Guidelines

When adding billing data:

1. **Cite your source** - Link to CMS, payer manual, regulation
2. **Date it** - Note when you verified the information
3. **Be specific** - Note if rule varies by plan type
4. **Note exceptions** - Billing rules often have edge cases

## What We Need Most

### High Priority

- [ ] More payer-specific rules (especially state BCBS plans)
- [ ] State Medicaid rules
- [ ] Denial resolution steps from real experience
- [ ] Common bundling pairs

### Medium Priority

- [ ] Additional ICD-10 codes with HCC info
- [ ] Specialty-specific billing tips
- [ ] Regional payer quirks

### Low Priority (Nice to Have)

- [ ] International billing codes (ICD-10-PCS, etc.)
- [ ] Historical code crosswalks

## Code of Conduct

Be respectful and constructive. We're all here to help healthcare work better.

## Questions?

- Open a [Discussion](https://github.com/YOUR_ORG/medical-billing-mcp/discussions)
- Tag maintainers in your PR

---

Thank you for helping make healthcare billing less painful! 🏥
