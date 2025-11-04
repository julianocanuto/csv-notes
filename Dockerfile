FROM python:3.10-alpine

WORKDIR /app

COPY backend/requirements.txt .
RUN apk add --no-cache libffi libstdc++ \
    && apk add --no-cache --virtual .build-deps build-base musl-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY backend/app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
