# 🏥 Medical Billing MCP

**Open-source billing knowledge for AI assistants**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-1.0-blue.svg)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](docker/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

> **The Problem:** A billing staff member gets a denial code. They Google it, read 5 articles, call the payer, wait on hold for 45 minutes, and maybe get an answer. Cost: 30-60 minutes per denial.
>
> **The Solution:** Ask an AI assistant. Get instant answers with resolution steps. Cost: 2 minutes.

---

## What Is This?

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that gives AI assistants like Claude access to medical billing knowledge:

| Tool | What It Does |
|------|--------------|
| `lookup_icd10` | Look up diagnosis codes |
| `lookup_cpt` | Look up procedure codes |
| `lookup_modifier` | Understand when to use modifiers (25, 59, etc.) |
| `lookup_denial` | Understand denial codes + how to fix them |
| `lookup_payer` | Get payer-specific rules (timely filing, etc.) |
| `lookup_bundling` | Check if codes are bundled together |

**This is a knowledge layer.** You bring your own payer connectivity (Stedi, Availity, Change Healthcare, etc.).

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/Kustode-ce/medical-billing-mcp.git
cd medical-billing-mcp

# Run with Docker
docker compose up -d

# Test it
docker compose exec mcp python -m medical_billing_mcp --test
```

### Option 2: Local Install

```bash
# Clone and install
git clone https://github.com/Kustode-ce/medical-billing-mcp.git
cd medical-billing-mcp
pip install -e .

# Run the server
python -m medical_billing_mcp
```

### Configure Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "medical-billing": {
      "command": "python",
      "args": ["-m", "medical_billing_mcp"]
    }
  }
}
```

**Config locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Restart Claude Desktop.

---

## Usage Examples

Once installed, ask Claude questions like:

### Understanding Codes

> "What does ICD-10 code E11.9 mean?"

> "What's CPT code 99214 and what documentation do I need?"

> "When should I use modifier 25?"

### Resolving Denials

> "I got denial code CO-50. What does it mean and how do I fix it?"

> "My claim was denied for 'not medically necessary'. What are the resolution steps?"

### Payer Rules

> "What's Medicare's timely filing limit?"

> "What are Blue Cross MA's known billing issues?"

### Bundling

> "Are CPT codes 99213 and 36415 bundled?"

See [docs/examples/](docs/examples/) for sample conversations.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI ASSISTANT (Claude)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MEDICAL BILLING MCP                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      server.py                            │  │
│  │            (Tool definitions + routing)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     handlers.py                           │  │
│  │              (Lookup functions)                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                       data/                               │  │
│  │                                                           │  │
│  │   icd10.json   cpt.json   modifiers.json                 │  │
│  │   denials.json   payers.json   bundling.json             │  │
│  │                                                           │  │
│  │            [Community contributes here]                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

---

## What This Is NOT

| Not In Scope | Why | You Already Have |
|--------------|-----|------------------|
| Claim submission | Not our job | Stedi, Availity |
| Eligibility checks | Real-time payer data | Stedi, payer portals |
| Prior auth submission | Payer integration | Cohere, eviCore |
| EOB/ERA parsing | Clearinghouse function | Stedi, clearinghouse |
| PHI storage | Security/compliance | Your EHR/PMS |

**We provide knowledge. You provide connectivity.**

---

## Data Sources

All data is from public sources:

| Data | Source |
|------|--------|
| ICD-10 codes | CMS |
| CPT descriptions | AMA (limited - full requires license) |
| HCPCS codes | CMS |
| Denial codes (CARC/RARC) | X12 / Washington Publishing |
| Payer rules | Public payer manuals |

---

## Contributing

We welcome contributions! The easiest way to help:

### Add Payer Rules

Know a payer's quirks? Edit `data/payers.json`:

```json
{
  "bcbs_tx": {
    "name": "Blue Cross Blue Shield Texas",
    "timely_filing_days": 95,
    "known_issues": ["Requires modifier 25 documentation"]
  }
}
```

### Add Denial Resolution Steps

Fixed a tricky denial? Share how in `data/denials.json`:

```json
{
  "CO-151": {
    "description": "Service not covered",
    "resolution_steps": [
      "Check if service requires prior auth",
      "Verify correct place of service code",
      "Appeal with medical necessity documentation"
    ]
  }
}
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Project Structure

```
medical-billing-mcp/
├── src/medical_billing_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py          # MCP server
│   ├── handlers.py        # Lookup functions
│   └── data/              # JSON knowledge base
│       ├── icd10.json
│       ├── cpt.json
│       ├── modifiers.json
│       ├── denials.json
│       ├── payers.json
│       └── bundling.json
├── tests/
├── docs/
│   ├── diagrams/          # Architecture diagrams
│   ├── api/               # API documentation
│   └── examples/          # Usage examples
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## License

MIT License - see [LICENSE](LICENSE)

**Note:** CPT codes are copyrighted by the AMA. This tool provides limited descriptions for educational purposes. For full CPT data, obtain an AMA license.

---

## Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/Kustode-ce/medical-billing-mcp/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Kustode-ce/medical-billing-mcp/discussions)

---

**Made for the healthcare community** ❤️

*Because providers should spend time with patients, not fighting insurance companies.*
