# Medical Billing MCP - Docker Image
#
# Build: docker build -t medical-billing-mcp .
# Run:   docker run -it medical-billing-mcp

FROM python:3.11-slim

# Labels
LABEL org.opencontainers.image.title="Medical Billing MCP"
LABEL org.opencontainers.image.description="Open-source medical billing knowledge for AI assistants"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.licenses="MIT"

# Set working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir build && \
    pip install --no-cache-dir mcp httpx

# Copy source code
COPY src/ src/

# Install the package
RUN pip install --no-cache-dir -e .

# Default command - run the MCP server
CMD ["python", "-m", "medical_billing_mcp"]

# Health check - verify the module loads
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import medical_billing_mcp; print('OK')" || exit 1
