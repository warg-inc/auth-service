FROM python:3.14-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies with uv
RUN uv sync --frozen

# Generate gRPC code from proto
RUN uv run python -m grpc_tools.protoc \
    -I./src/protos \
    --python_out=./src/protos/generated \
    --grpc_python_out=./src/protos/generated \
    ./src/protos/user.proto

# Expose gRPC port
EXPOSE 50051

# Run the application
CMD ["uv", "run", "python", "-m", "src.run"]