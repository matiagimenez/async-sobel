FROM python:3.9.19-slim-bullseye

# Crear un usuario no root
RUN useradd -m -d /home/nonroot -s /bin/bash nonroot

WORKDIR /entry-server

# Instalar dependencias del sistema
# RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
# RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copiar archivos y directorios
COPY ./requirements.txt requirements.txt
COPY server.py server.py
COPY storage_client.py storage_client.py

# Cambiar la propiedad de los archivos al usuario no root
RUN chown -R nonroot:nonroot /entry-server

# Cambiar al usuario no root.
USER nonroot

RUN pip install -r requirements.txt
    
EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "server", "run", "--host", "0.0.0.0"]