FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ETAPA 2: Final (Imagen liviana de ejecución)

FROM python:3.12-slim AS final

WORKDIR /app

# Instalar librerias de tiempo de ejecucion para PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar paquetes instalados desde la etapa anterior
COPY --from=builder /usr/local /usr/local
COPY . /app/

ENV PYTHONUNBUFFERED=1

# Buenas practicas de seguridad: Crear usuario no raiz (non-root)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]