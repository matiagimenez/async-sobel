FROM python:3.9.19-slim-bullseye

# Crear un usuario no root
RUN useradd -m -d /home/nonroot -s /bin/bash nonroot

WORKDIR /sobel

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copiar archivos y directorios
COPY ./requirements.txt requirements.txt
COPY ./src/server.py server.py
COPY ./src/utils utils
COPY ./src/plugins plugins

# Cambiar la propiedad de los archivos al usuario no root
RUN chown -R nonroot:nonroot /sobel

# Cambiar al usuario no root
USER nonroot

# Instalar las dependencias de Python
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "server", "run", "--host", "0.0.0.0"]