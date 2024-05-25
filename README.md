# Sobel contenerizado asincrónico y escalable

El operador de Sobel es una máscara que, aplicada a una imagen, permite detectar (resaltar) bordes. Este operador es una operación matemática que, aplicada a cada pixel y teniendo en cuenta los píxeles que lo rodean, obtiene un nuevo valor (color) para ese pixel. Aplicando la operación a cada píxel, se obtiene una nueva imagen que resalta los bordes.

La idea es que construya una infraestructura basada en la nube pero ahora con un enfoque diferente

Para ello, será necesario desplegar con terraform un cluster de Kubernetes (GKE). Este será el manejador de todos los recursos que vayamos a desplegar. Es decir, va a alojar tanto los servicios de infraestructura (rabbitMQ y Redis) como los componentes de las aplicaciones que vamos a correr (frontend, backend, split, joiner, etc). Este clúster tiene que tener la siguiente configuración mínima:

-   Un nodegroup para alojar los servicios de infraestructura (rabbitmq, redis, otros)
-   Un nodegroup compartido para las aplicaciones del sistema (front, back, split, joiner)
-   Máquinas virtuales (fuera del cluster) que se encarguen de las tareas de procesamiento / cómputo intensivo

![Diagramas-# HIT 3 (TP 4)](https://github.com/Fedesin/sdypp-2024/assets/117539520/660a280b-d904-4bf5-b8dc-57966502dfa0)
