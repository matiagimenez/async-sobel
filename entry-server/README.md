# Entry web server

Este servidor web es el encargado de recibir la imagen original del usuario y enviarla al split-service para iniciar el procesamiento sobel asincrónico.

Además, posee un endpoint para recibir los resultados sobel desde el join-service, almacenandolos hasta que, en algun momento, el usuario que inicio el proceso solicite el resultado del procesamiento utilizando el TASK_ID que recibio al iniciar el proceso.
