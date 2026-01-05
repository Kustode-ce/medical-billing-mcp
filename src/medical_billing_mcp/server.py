"""
Medical Billing MCP Server

An open-source MCP server providing medical billing knowledge.
https://github.com/Kustode-ce/medical-billing-mcp

License: MIT
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

from . import handlers

__version__ = "0.1.0"

# Initialize server
server = Server("medical-billing-mcp")

# Data directory
DATA_DIR = Path(__file__).parent / "data"


# =============================================================================
# Tool Definitions
# =============================================================================

TOOLS = [
    Tool(
        name="lookup_icd10",
        description="Look up ICD-10 diagnosis codes by code or search term",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "ICD-10 code (e.g., 'E11.9')"
                },
                "search": {
                    "type": "string",
                    "description": "Search term (e.g., 'diabetes')"
                }
            }
        }
    ),
    Tool(
        name="lookup_cpt",
        description="Look up CPT procedure codes by code or search term",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "CPT code (e.g., '99213')"
                },
                "search": {
                    "type": "string",
                    "description": "Search term (e.g., 'office visit')"
                }
            }
        }
    ),
    Tool(
        name="lookup_modifier",
        description="Look up billing modifier usage and documentation requirements",
        inputSchema={
            "type": "object",
            "properties": {
                "modifier": {
                    "type": "string",
                    "description": "Modifier code (e.g., '25', '59')"
                }
            },
            "required": ["modifier"]
        }
    ),
    Tool(
        name="lookup_denial",
        description="Look up denial codes (CARC/RARC) with resolution steps",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Denial code (e.g., 'CO-50', '50')"
                },
                "search": {
                    "type": "string",
                    "description": "Search term (e.g., 'medical necessity')"
                }
            }
        }
    ),
    Tool(
        name="lookup_payer",
        description="Look up payer-specific billing rules",
        inputSchema={
            "type": "object",
            "properties": {
                "payer": {
                    "type": "string",
                    "description": "Payer name (e.g., 'medicare', 'bcbs_ma')"
                }
            },
            "required": ["payer"]
        }
    ),
    Tool(
        name="lookup_bundling",
        description="Check if procedure codes are bundled together",
        inputSchema={
            "type": "object",
            "properties": {
                "codes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CPT codes to check (e.g., ['99213', '36415'])"
                }
            },
            "required": ["codes"]
        }
    )
]


@server.list_tools()
async def list_tools() -> List[Tool]:
    """Return list of available tools."""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Route tool calls to handlers."""
    
    try:
        # Route to appropriate handler
        if name == "lookup_icd10":
            result = handlers.lookup_icd10(
                DATA_DIR,
                code=arguments.get("code"),
                search=arguments.get("search")
            )
        
        elif name == "lookup_cpt":
            result = handlers.lookup_cpt(
                DATA_DIR,
                code=arguments.get("code"),
                search=arguments.get("search")
            )
        
        elif name == "lookup_modifier":
            result = handlers.lookup_modifier(
                DATA_DIR,
                modifier=arguments.get("modifier")
            )
        
        elif name == "lookup_denial":
            result = handlers.lookup_denial(
                DATA_DIR,
                code=arguments.get("code"),
                search=arguments.get("search")
            )
        
        elif name == "lookup_payer":
            result = handlers.lookup_payer(
                DATA_DIR,
                payer=arguments.get("payer")
            )
        
        elif name == "lookup_bundling":
            result = handlers.lookup_bundling(
                DATA_DIR,
                codes=arguments.get("codes", [])
            )
        
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        # Return result as JSON
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        )
    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]
        )


# =============================================================================
# Main Entry Point
# =============================================================================

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def run():
    """Entry point for console script."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
