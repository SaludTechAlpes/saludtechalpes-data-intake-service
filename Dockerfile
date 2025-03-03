# Usa una versión específica de Python (3.9-alpine3.16)
FROM python:3.9-alpine3.16

# Establece el directorio de trabajo
WORKDIR /app

# Asegurar que Python reconozca src como parte del entorno
ENV PYTHONPATH=/app/src

# Instala dependencias necesarias del sistema
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    libstdc++ \
    gcompat


COPY requirements.txt ./
RUN pip install --upgrade "pip<24.1"
RUN pip install -r requirements.txt

# Copia el resto del código después de instalar dependencias para mejorar cacheo
COPY . /app

# Expone el puerto 5000 (si usas Flask)
EXPOSE 5000

# Permisos y arranque del contenedor
COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh

# Iniciar la aplicación (asegúrate de que `make run-docker` existe)
CMD ["make", "run-docker"]
