FROM python:3.11-slim

WORKDIR /app

RUN set -ex \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        curl \
        apt-transport-https \
        ca-certificates \
        gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends google-cloud-sdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY credentials.json /app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
