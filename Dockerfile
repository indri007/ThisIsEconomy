FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python scripts/setup_data_access.py || true

EXPOSE 8080

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
