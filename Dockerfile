# Usar imagen base con Python y Chrome
FROM selenium/standalone-chrome:latest

USER root

# Instalar Python y dependencias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Variable de entorno para el puerto
ENV PORT=8080

# Exponer puerto
EXPOSE 8080

# Comando para iniciar la aplicación
CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
