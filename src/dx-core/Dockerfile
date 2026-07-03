# SPDX-License-Identifier: MIT
FROM python:3.12-slim

WORKDIR /app

# Copy khai báo dự án + mã nguồn rồi cài (setuptools cần thư mục app khi build)
COPY pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir .

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --retries=5 \
    CMD python -c "import httpx,sys; sys.exit(0 if httpx.get('http://localhost:8000/health').status_code==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
