"""
Tests for Medical Billing MCP handlers.

Run with: pytest tests/ -v
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from medical_billing_mcp import handlers

# Data directory
DATA_DIR = Path(__file__).parent.parent / "src" / "medical_billing_mcp" / "data"


class TestICD10Lookup:
    """Tests for ICD-10 code lookups."""
    
    def test_lookup_by_code(self):
        """Test direct code lookup."""
        result = handlers.lookup_icd10(DATA_DIR, code="E11.9")
        assert result.get("code") == "E11.9"
        assert "diabetes" in result.get("description", "").lower()
    
    def test_lookup_by_code_case_insensitive(self):
        """Test code lookup is case insensitive."""
        result = handlers.lookup_icd10(DATA_DIR, code="e11.9")
        assert result.get("code") == "E11.9"
    
    def test_lookup_not_found(self):
        """Test code not found returns error."""
        result = handlers.lookup_icd10(DATA_DIR, code="X99.99")
        assert "error" in result
    
    def test_search(self):
        """Test keyword search."""
        result = handlers.lookup_icd10(DATA_DIR, search="diabetes")
        assert "results" in result
        assert len(result["results"]) > 0
    
    def test_no_params_returns_error(self):
        """Test no parameters returns error."""
        result = handlers.lookup_icd10(DATA_DIR)
        assert "error" in result


class TestCPTLookup:
    """Tests for CPT code lookups."""
    
    def test_lookup_by_code(self):
        """Test direct code lookup."""
        result = handlers.lookup_cpt(DATA_DIR, code="99213")
        assert result.get("code") == "99213"
        assert "office visit" in result.get("description", "").lower()
    
    def test_lookup_not_found(self):
        """Test code not found."""
        result = handlers.lookup_cpt(DATA_DIR, code="00000")
        assert "error" in result
    
    def test_search(self):
        """Test keyword search."""
        result = handlers.lookup_cpt(DATA_DIR, search="office visit")
        assert "results" in result
        assert len(result["results"]) > 0


class TestModifierLookup:
    """Tests for modifier lookups."""
    
    def test_lookup_modifier_25(self):
        """Test modifier 25 lookup."""
        result = handlers.lookup_modifier(DATA_DIR, modifier="25")
        assert result.get("modifier") == "25"
        assert "documentation_required" in result
    
    def test_lookup_modifier_59(self):
        """Test modifier 59 lookup."""
        result = handlers.lookup_modifier(DATA_DIR, modifier="59")
        assert result.get("modifier") == "59"
    
    def test_modifier_not_found(self):
        """Test modifier not found returns error and available list."""
        result = handlers.lookup_modifier(DATA_DIR, modifier="XX")
        assert "error" in result
        assert "available" in result


class TestDenialLookup:
    """Tests for denial code lookups."""
    
    def test_lookup_denial_code(self):
        """Test denial code lookup."""
        result = handlers.lookup_denial(DATA_DIR, code="50")
        assert result.get("code") == "50"
        assert "resolution_steps" in result
    
    def test_lookup_denial_with_group(self):
        """Test denial code with group prefix."""
        result = handlers.lookup_denial(DATA_DIR, code="CO-50")
        assert result.get("code") == "50"
    
    def test_search_denials(self):
        """Test denial keyword search."""
        result = handlers.lookup_denial(DATA_DIR, search="medical necessity")
        assert "results" in result


class TestPayerLookup:
    """Tests for payer lookups."""
    
    def test_lookup_medicare(self):
        """Test Medicare lookup."""
        result = handlers.lookup_payer(DATA_DIR, payer="medicare")
        assert result.get("payer_id") == "medicare"
        assert "timely_filing_days" in result
    
    def test_lookup_not_found(self):
        """Test payer not found."""
        result = handlers.lookup_payer(DATA_DIR, payer="unknown_payer")
        assert "error" in result
        assert "available" in result


class TestBundlingLookup:
    """Tests for bundling lookups."""
    
    def test_bundled_codes(self):
        """Test bundled code pair."""
        result = handlers.lookup_bundling(DATA_DIR, codes=["45378", "45380"])
        assert result.get("any_bundled") is True
    
    def test_non_bundled_codes(self):
        """Test non-bundled code pair."""
        result = handlers.lookup_bundling(DATA_DIR, codes=["99213", "36415"])
        # Should not find a bundle in our sample data
        assert "pairs" in result
    
    def test_insufficient_codes(self):
        """Test error when less than 2 codes provided."""
        result = handlers.lookup_bundling(DATA_DIR, codes=["99213"])
        assert "error" in result


class TestDataLoading:
    """Tests for data file loading."""
    
    def test_data_files_exist(self):
        """Test all required data files exist."""
        required_files = [
            "icd10.json",
            "cpt.json",
            "modifiers.json",
            "denials.json",
            "payers.json",
            "bundling.json",
        ]
        for filename in required_files:
            path = DATA_DIR / filename
            assert path.exists(), f"Missing data file: {filename}"
    
    def test_data_files_valid_json(self):
        """Test all data files are valid JSON."""
        import json
        for path in DATA_DIR.glob("*.json"):
            try:
                json.loads(path.read_text())
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {path.name}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
