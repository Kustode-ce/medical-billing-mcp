"""
Medical Billing MCP

Open-source medical billing knowledge for AI assistants.

License: MIT
Repository: https://github.com/YOUR_ORG/medical-billing-mcp
"""

__version__ = "0.1.0"

from . import handlers
from .server import main, run, server

__all__ = ["main", "run", "server", "handlers", "__version__"]
