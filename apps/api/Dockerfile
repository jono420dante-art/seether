FROM python:3.12-slim

WORKDIR /app

COPY packages/shared /app/packages/shared
COPY apps/api /app/apps/api
COPY services/dieter_core /app/services/dieter_core
COPY services/neural_hub /app/services/neural_hub
COPY apps/worker /app/apps/worker

RUN pip install fastapi uvicorn cryptography requests pydantic

ENV PYTHONPATH="/app"

CMD ["uvicorn", "apps.api.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
