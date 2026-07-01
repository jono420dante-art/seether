FROM python:3.12-slim

WORKDIR /app

COPY packages/shared /app/packages/shared
COPY apps/worker /app/apps/worker
COPY services/dieter_core /app/services/dieter_core
COPY services/neural_hub /app/services/neural_hub

RUN pip install cryptography requests pydantic

ENV PYTHONPATH="/app"

CMD ["python", "apps/worker/director_poc.py"]
