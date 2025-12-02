# S1NGULARITY Dockerfile
# Multi-stage build for optimized production image

# ==============================================
# Stage 1: Builder
# ==============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==============================================
# Stage 2: Runtime
# ==============================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Add virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create logs directory and make start script executable
RUN mkdir -p logs && \
    chmod +x start.sh

# Non-root user for security
RUN useradd -m -u 1000 s1ngularity && \
    chown -R s1ngularity:s1ngularity /app

USER s1ngularity

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application with initialization
CMD ["./start.sh"]
