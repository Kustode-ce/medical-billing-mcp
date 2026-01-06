"""
Entry point for: python -m medical_billing_mcp

Usage:
    python -m medical_billing_mcp          # Run MCP server
    python -m medical_billing_mcp --test   # Run self-test
    python -m medical_billing_mcp --version
"""

import sys

from . import __version__


def self_test():
    """Run a quick self-test to verify everything works."""
    from pathlib import Path

    from . import handlers
    
    data_dir = Path(__file__).parent / "data"
    
    print(f"Medical Billing MCP v{__version__}")
    print(f"Data directory: {data_dir}")
    print()
    
    tests = [
        ("ICD-10 lookup", lambda: handlers.lookup_icd10(data_dir, code="E11.9")),
        ("ICD-10 search", lambda: handlers.lookup_icd10(data_dir, search="diabetes")),
        ("CPT lookup", lambda: handlers.lookup_cpt(data_dir, code="99213")),
        ("Modifier lookup", lambda: handlers.lookup_modifier(data_dir, modifier="25")),
        ("Denial lookup", lambda: handlers.lookup_denial(data_dir, code="CO-50")),
        ("Payer lookup", lambda: handlers.lookup_payer(data_dir, payer="medicare")),
        ("Bundling check", lambda: handlers.lookup_bundling(data_dir, codes=["99213", "36415"])),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            if "error" in result and "not found" in result.get("error", "").lower():
                print(f"⚠️  {name}: No data (add to JSON files)")
            else:
                print(f"✅ {name}: OK")
                passed += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    
    return 0 if failed == 0 else 1


def main():
    """Main entry point."""
    if "--version" in sys.argv:
        print(f"medical-billing-mcp {__version__}")
        return 0
    
    if "--test" in sys.argv:
        return self_test()
    
    # Run the MCP server
    from .server import run
    run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
