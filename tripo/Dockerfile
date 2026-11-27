FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

CMD ["mcp-tripo", "--transport", "http", "--port", "8000"]
