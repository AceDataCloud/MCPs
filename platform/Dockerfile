FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir ".[http]"

CMD ["mcp-acedata-platform", "--transport", "http", "--port", "8000"]
