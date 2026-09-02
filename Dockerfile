# =========================
# Stage 1: Builder
# =========================
FROM python:3.13-slim AS builder

WORKDIR /app

# Create isolated virtual environment
RUN python -m venv /opt/venv

# Use venv Python/pip
ENV PATH="/opt/venv/bin:$PATH"

# Install application dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip


# =========================
# Stage 2: Runtime
# =========================
FROM python:3.13-slim AS runtime

WORKDIR /app

# Remove pip from runtime base image
RUN python -m pip uninstall -y pip

# Create non-root user
RUN useradd --create-home --uid 10001 appuser

# Copy only installed application dependencies from builder
COPY --from=builder /opt/venv /opt/venv

# Use venv Python at runtime
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser app.py .

# Run container as non-root
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]