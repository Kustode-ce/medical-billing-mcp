# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-05

### Added

- Initial release
- **6 MCP Tools:**
  - `lookup_icd10` - ICD-10 diagnosis code lookup
  - `lookup_cpt` - CPT procedure code lookup
  - `lookup_modifier` - Billing modifier guidance
  - `lookup_denial` - CARC/RARC denial codes with resolution steps
  - `lookup_payer` - Payer-specific billing rules
  - `lookup_bundling` - CCI bundling edit check
- **Seed Data:**
  - Common ICD-10 codes with HCC indicators
  - Common CPT E/M and procedure codes
  - Top modifiers (25, 59, TC, 26, etc.)
  - Common denial codes with resolution steps
  - Major payer rules (Medicare, BCBS, UHC, Aetna, Cigna, Humana)
  - Common bundling pairs
- **Documentation:**
  - Architecture diagrams (Mermaid)
  - API documentation
  - Usage examples with sample conversations
  - Sample tool outputs
- **Infrastructure:**
  - Docker support
  - GitHub Actions CI
  - pytest test suite (21 tests)
  - Self-test command (`--test`)

### Notes

- This is a **knowledge layer** - users bring their own payer connectivity (Stedi, Availity, etc.)
- 100% PHI-free - works with codes and rules only
- Seed data is a starting point - community contributions welcome!
