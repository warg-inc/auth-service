FROM python:3.14-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies with uv
RUN uv sync --frozen --no-dev

# Generate gRPC code from proto
RUN mkdir -p ./src/protos/generated && \
    touch ./src/protos/generated/__init__.py && \
    uv run python -m grpc_tools.protoc \
    -I./src/protos \
    --python_out=./src/protos/generated \
    --grpc_python_out=./src/protos/generated \
    ./src/protos/auth.proto \
    ./src/protos/user.proto && \
    sed -i 's/^import \(.*_pb2\) as/from src.protos.generated import \1 as/' \
    ./src/protos/generated/*_pb2_grpc.py

# Expose gRPC port
EXPOSE 50051

ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["python", "-m", "src.run"]
