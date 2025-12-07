FROM python:3.11-slim

WORKDIR /app

# Дополнительно устанавливаем grpcurl для health checks (указано в условиях ДЗ)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && wget https://github.com/fullstorydev/grpcurl/releases/download/v1.9.1/grpcurl_1.9.1_linux_x86_64.tar.gz \
    && tar -xzf grpcurl_1.9.1_linux_x86_64.tar.gz -C /usr/local/bin \
    && rm grpcurl_1.9.1_linux_x86_64.tar.gz \
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY ml_grpc_service/ ./ml_grpc_service/

# Устанавливаем зависимости
RUN uv sync --frozen

# Environment variables defaults
ENV MODEL_PATH=ml_grpc_service/models/wine_quality_model.pkl
ENV SCALER_PATH=ml_grpc_service/models/wine_scaler.pkl
ENV MODEL_VERSION=v1.0.0
ENV PORT=50051
ENV MAX_WORKERS=4

EXPOSE 50051

# Запускаем gRPC сервер
CMD ["uv", "run", "python", "-m", "ml_grpc_service.server.server"]
