La version utilizada de python es Python 3.10.4
Se utilizo flask para levantar los servidores.
Para desplegar el programa se deben seguir estos pasos (windows):
- descromprimir e ingresar a la consola en la misma carpeta donde estan los scripts server.py y cliente.py
- escribir en la consola: python server.py y enter
- escribir python cliente.py seguido de la direccion del archivo de configuracion, en este caso se incluyen 3 archivos de ejemplo que se encuentran en la misma carpeta, por lo que quedara como python cliente.py config1.json por ejemplo.
- hacer estos con los otros archivos de configuracion o crear uno.
- el programa se ejecutara solo a partir de aqui, fijarse en la consola de los clientes y servidores para informacion adicional.


---- Log Server -----
Es necesario inicialiazr el servidor de logs con python logging_server.py para que se puedan guardar los datos.
Pre requisitos:
1. Instalar java y javac en ubuntu
2. Instalar pandas y maplotlib "pip install pandas matplotlib"


## Pasos para ejecutar
1. Iniciar: javac CentralLogServer.java LogClient.java
2. Ejecutar el servidor central: java CentralLogServer
3. Ejecutar el cliente RMI para enviar los logs:
    python3 LogClient config1.log && 
    python3 LogCLient config2.log && 
    python3 LogClient config3.log ...




