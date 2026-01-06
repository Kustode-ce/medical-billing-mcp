"""
Medical Billing MCP - Handlers

Simple lookup functions for billing codes and rules.
Each function loads JSON data and searches/returns results.

No classes, no complexity - just functions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# =============================================================================
# Data Loading (with caching)
# =============================================================================

_cache: Dict[str, Any] = {}


def _load_data(data_dir: Path, filename: str) -> Dict:
    """Load JSON file with caching."""
    cache_key = str(data_dir / filename)

    if cache_key not in _cache:
        path = data_dir / filename
        if not path.exists():
            return {"codes": {}, "_meta": {"error": f"File not found: {filename}"}}
        _cache[cache_key] = json.loads(path.read_text())

    return _cache[cache_key]


# =============================================================================
# ICD-10 Lookup
# =============================================================================


def lookup_icd10(data_dir: Path, code: Optional[str] = None, search: Optional[str] = None) -> Dict:
    """
    Look up ICD-10 diagnosis codes.

    Args:
        data_dir: Path to data directory
        code: Direct code lookup (e.g., "E11.9")
        search: Keyword search (e.g., "diabetes")

    Returns:
        Code details or search results
    """
    data = _load_data(data_dir, "icd10.json")
    codes = data.get("codes", {})

    if code:
        code = code.upper().strip().replace(" ", "")
        if code in codes:
            return {"code": code, **codes[code]}

        # Try partial match
        matches = [(k, v) for k, v in codes.items() if k.startswith(code)]
        if matches:
            return {
                "exact_match": False,
                "suggestions": [{"code": k, **v} for k, v in matches[:10]],
            }

        return {"error": f"Code '{code}' not found"}

    if search:
        search_lower = search.lower()
        matches = [
            {"code": k, **v}
            for k, v in codes.items()
            if search_lower in v.get("description", "").lower()
        ]
        return {"results": matches[:20], "total": len(matches)}

    return {"error": "Provide 'code' or 'search' parameter"}


# =============================================================================
# CPT Lookup
# =============================================================================


def lookup_cpt(data_dir: Path, code: Optional[str] = None, search: Optional[str] = None) -> Dict:
    """
    Look up CPT procedure codes.

    Args:
        data_dir: Path to data directory
        code: Direct code lookup (e.g., "99213")
        search: Keyword search (e.g., "office visit")

    Returns:
        Code details or search results
    """
    data = _load_data(data_dir, "cpt.json")
    codes = data.get("codes", {})

    if code:
        code = code.strip()
        if code in codes:
            return {"code": code, **codes[code]}
        return {"error": f"Code '{code}' not found"}

    if search:
        search_lower = search.lower()
        matches = [
            {"code": k, **v}
            for k, v in codes.items()
            if search_lower in v.get("description", "").lower()
        ]
        return {"results": matches[:20], "total": len(matches)}

    return {"error": "Provide 'code' or 'search' parameter"}


# =============================================================================
# Modifier Lookup
# =============================================================================


def lookup_modifier(data_dir: Path, modifier: Optional[str] = None) -> Dict:
    """
    Look up billing modifiers.

    Args:
        data_dir: Path to data directory
        modifier: Modifier code (e.g., "25", "59")

    Returns:
        Modifier details with usage guidance
    """
    data = _load_data(data_dir, "modifiers.json")
    modifiers = data.get("modifiers", {})

    if not modifier:
        return {"error": "Provide 'modifier' parameter", "available": list(modifiers.keys())}

    modifier = modifier.upper().strip()

    if modifier in modifiers:
        return {"modifier": modifier, **modifiers[modifier]}

    return {"error": f"Modifier '{modifier}' not found", "available": list(modifiers.keys())}


# =============================================================================
# Denial Code Lookup
# =============================================================================


def lookup_denial(data_dir: Path, code: Optional[str] = None, search: Optional[str] = None) -> Dict:
    """
    Look up denial codes (CARC/RARC).

    Args:
        data_dir: Path to data directory
        code: Denial code (e.g., "CO-50", "50")
        search: Keyword search (e.g., "medical necessity")

    Returns:
        Denial details with resolution steps
    """
    data = _load_data(data_dir, "denials.json")
    codes = data.get("codes", {})
    groups = data.get("groups", {})

    if code:
        # Parse code - handle "CO-50" or just "50"
        code = code.upper().strip()

        group = None
        code_num = code

        if "-" in code:
            parts = code.split("-")
            group = parts[0]
            code_num = parts[1]

        if code_num in codes:
            result = {"code": code_num, **codes[code_num]}

            # Add group info if available
            result_group = result.get("group", group)
            if result_group and result_group in groups:
                result["group_info"] = groups[result_group]

            return result

        return {"error": f"Denial code '{code}' not found"}

    if search:
        search_lower = search.lower()
        matches = [
            {"code": k, **v}
            for k, v in codes.items()
            if search_lower in v.get("description", "").lower()
            or search_lower in str(v.get("resolution_steps", [])).lower()
        ]
        return {"results": matches[:20], "total": len(matches)}

    return {"error": "Provide 'code' or 'search' parameter"}


# =============================================================================
# Payer Lookup
# =============================================================================


def lookup_payer(data_dir: Path, payer: Optional[str] = None) -> Dict:
    """
    Look up payer-specific billing rules.

    Args:
        data_dir: Path to data directory
        payer: Payer identifier (e.g., "medicare", "bcbs_ma")

    Returns:
        Payer rules and information
    """
    data = _load_data(data_dir, "payers.json")
    payers = data.get("payers", {})

    if not payer:
        return {"error": "Provide 'payer' parameter", "available": list(payers.keys())}

    payer_key = payer.lower().strip().replace(" ", "_")

    if payer_key in payers:
        return {"payer_id": payer_key, **payers[payer_key]}

    # Try partial match
    matches = [k for k in payers.keys() if payer_key in k]
    if matches:
        return {"error": f"Payer '{payer}' not found exactly", "suggestions": matches}

    return {"error": f"Payer '{payer}' not found", "available": list(payers.keys())}


# =============================================================================
# Bundling Lookup
# =============================================================================


def lookup_bundling(data_dir: Path, codes: List[str] = None) -> Dict:
    """
    Check if procedure codes are bundled (CCI edits).

    Args:
        data_dir: Path to data directory
        codes: List of CPT codes to check

    Returns:
        Bundling status and details
    """
    if not codes or len(codes) < 2:
        return {"error": "Provide at least 2 codes to check bundling"}

    data = _load_data(data_dir, "bundling.json")
    bundles = data.get("bundles", {})

    codes = [c.strip() for c in codes]
    results = []

    # Check each pair
    for i, code1 in enumerate(codes):
        for code2 in codes[i + 1 :]:
            # Create key (sorted for consistent lookup)
            key = tuple(sorted([code1, code2]))
            key_str = f"{key[0]}|{key[1]}"
            alt_key_str = f"{key[1]}|{key[0]}"

            bundle_info = bundles.get(key_str) or bundles.get(alt_key_str)

            if bundle_info:
                results.append({"code_pair": [code1, code2], "bundled": True, **bundle_info})
            else:
                results.append(
                    {
                        "code_pair": [code1, code2],
                        "bundled": False,
                        "can_bill_together": True,
                        "note": "No bundling rule found - verify with current CCI edits",
                    }
                )

    # Summary
    any_bundled = any(r["bundled"] for r in results)

    return {"codes_checked": codes, "any_bundled": any_bundled, "pairs": results}
