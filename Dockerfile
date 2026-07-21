# ─────────────────────────────────────────────────────────────────
#  Dockerfile – 2048 Game with AI Solver
#  Deployable on Render
# ─────────────────────────────────────────────────────────────────

# ---- Build stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and install
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage ----
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed Python packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy the application source code (located inside the 2048-game/ subdirectory)
COPY 2048-game/src/ src/
COPY 2048-game/web_app.py .
COPY 2048-game/templates/ templates/
COPY 2048-game/static/ static/

# Ensure the high-score file exists
RUN echo "0" > src/scores.txt

# Expose the port Render expects
EXPOSE 5000

# Health check so Render knows the app is ready
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/state')" || exit 1

# Run the Flask web application
CMD ["python", "web_app.py"]