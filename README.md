# Sobel contenerizado asincrónico y escalable

El operador de Sobel es una máscara que, aplicada a una imagen, permite detectar (resaltar) bordes. Este operador es una operación matemática que, aplicada a cada pixel y teniendo en cuenta los píxeles que lo rodean, obtiene un nuevo valor (color) para ese pixel. Aplicando la operación a cada píxel, se obtiene una nueva imagen que resalta los bordes.

La idea es que construya una infraestructura basada en la nube pero ahora con un enfoque diferente.

Para ello, será necesario desplegar con terraform un cluster de Kubernetes (GKE). Este será el manejador de todos los recursos que vayamos a desplegar. Es decir, va a alojar tanto los servicios de infraestructura (rabbitMQ y Redis) como los componentes de las aplicaciones que vamos a correr (frontend, backend, split, joiner, etc). Este clúster tiene que tener la siguiente configuración mínima:

-   Un nodegroup para alojar los servicios de infraestructura (rabbitmq, redis, otros)
-   Un nodegroup compartido para las aplicaciones del sistema (front, back, split, joiner)
-   Máquinas virtuales (fuera del cluster) que se encarguen de las tareas de procesamiento / cómputo intensivo.

![Diagramas-# HIT 3 (TP 4)](https://github.com/Fedesin/sdypp-2024/assets/117539520/660a280b-d904-4bf5-b8dc-57966502dfa0)

# Instrucciones para ejecutar el servicio de manera local con docker

1. Clonar el archivo .env.example y renombrarlo a .env. Si desea, puede actualizar los valores por defecto.

```
# Endpoint para interactuar con el servicio de split de imágenes
SPLIT_SERVICE_URL=http://split-service:5000/api/split

# Definir la cantidad de partes en las que se dividirá la imagen
FRAGMENTS_COUNT=4

# Nombre del bucket GCP donde se subirán los fragmentos de imagen
BUCKET_NAME=sobel

# Host y puerto donde escucha el servidor redis
REDIS_PORT=6379
REDIS_HOST=redis

# Nombre de usuario y password para usar de credenciales en rabbitmq
RABBITMQ_USER=rabbituser
RABBITMQ_PASSWORD=rabbitpassword
# Host donde escucha el servidor rabbitmq
RABBITMQ_HOST=rabbit
```

2. Ejecutar el siguiente comando (debe modificar la linea de curl si desea utilizar otra imagen). Para este paso es necesario contar con el archivo con las keys (credentials.json) en el directorio raiz del proyecto. También deberá actualizar los valores de variables en el código terraform para adecuarlo a su proyecto GCP.

```bash
sh runner.sh
```

Copie el TASK_ID obtenido como respuesta.

3. Abra el navegador y pegue la siguiente URL `http://localhost:5001/api/results/<TASK_ID>`, reemplazando el valor de TASK_ID obtenido en el paso anterior. El JSON que muestra como respuesta indica el estado de la tarea. Cuando la tarea esté completa, le mostrará la URL que le permitirá obtener la imagen sobel final
