# Quick Start Guide

Get up and running in 5 minutes.

## Option 1: pip install (Simplest)

```bash
# Clone
git clone https://github.com/YOUR_ORG/medical-billing-mcp.git
cd medical-billing-mcp

# Install
pip install -e .

# Test it works
python -m medical_billing_mcp --test
```

## Option 2: Docker

```bash
# Clone
git clone https://github.com/YOUR_ORG/medical-billing-mcp.git
cd medical-billing-mcp

# Build and run
docker build -t medical-billing-mcp -f docker/Dockerfile .
docker run --rm medical-billing-mcp python -m medical_billing_mcp --test
```

## Configure Claude Desktop

1. Find your config file:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. Add the server:

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

3. Restart Claude Desktop

## Test It!

Ask Claude:

> "What does denial code CO-50 mean and how do I fix it?"

> "When should I use modifier 25?"

> "What's Medicare's timely filing limit?"

## Expected Output

```
$ python -m medical_billing_mcp --test

Medical Billing MCP v0.1.0
Data directory: .../medical_billing_mcp/data

✅ ICD-10 lookup: OK
✅ ICD-10 search: OK
✅ CPT lookup: OK
✅ Modifier lookup: OK
✅ Denial lookup: OK
✅ Payer lookup: OK
✅ Bundling check: OK

Results: 7 passed, 0 failed
```

## Next Steps

- See [docs/examples/conversations.md](docs/examples/conversations.md) for usage examples
- See [docs/api/tools.md](docs/api/tools.md) for API reference
- See [CONTRIBUTING.md](CONTRIBUTING.md) to add payer rules or denial resolution steps
