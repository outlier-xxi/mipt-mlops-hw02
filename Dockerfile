# Wine Quality Prediction gRPC Service
FROM python:3.11-slim

WORKDIR /app

# Install uv for package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY ml_grpc_service/ ./ml_grpc_service/

# Install dependencies
RUN uv sync --frozen

# Environment variables with defaults for wine quality model
ENV MODEL_PATH=ml_grpc_service/models/wine_quality_model.pkl
ENV SCALER_PATH=ml_grpc_service/models/wine_scaler.pkl
ENV MODEL_VERSION=v1.0.0
ENV PORT=50051
ENV MAX_WORKERS=4

# Expose gRPC port
EXPOSE 50051

# Run the gRPC server
CMD ["uv", "run", "python", "-m", "ml_grpc_service.server.server"]
