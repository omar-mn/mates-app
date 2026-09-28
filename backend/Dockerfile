FROM python:3.11-alpine AS base

WORKDIR /app

COPY requirements/requirements.dev.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.dev.txt

FROM python:3.11-alpine

WORKDIR /app

COPY --from=base /app/wheels /wheels
COPY --from=base /app/requirements.dev.txt .

RUN pip install --no-cache /wheels/*

RUN pip install uvicorn[standard]

COPY ./src .

COPY build.sh .

RUN chmod +x build.sh

CMD ["sh", "build.sh"]