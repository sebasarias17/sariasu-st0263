# info de la materia: ST0263 Topicos de telematica
#
# Estudiante(s): Sebastian Arias Usma, sariasu@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Reto 1 y 2 P2P - Comunicación entre procesos mediante API REST, RPC 
#
# 1. breve descripción de la actividad
Esta actividad implica diseñar e implementar un sistema peer-to-peer (P2P) para compartir archivos de manera distribuida y descentralizada. Cada nodo del sistema contiene microservicios que permiten la comunicación entre pares mediante API REST, gRPC. Se recomienda un esquema de red P2P no estructurada, donde cada nodo tiene un archivo de configuración con detalles como la dirección IP, el puerto de escucha y los nodos amigos.

Cada nodo puede buscar y compartir archivos utilizando consultas sobre los recursos disponibles en la red. La transferencia real de archivos se lleva a cabo entre los nodos que poseen el recurso, mientras que las consultas y la interacción con la red se realizan a través de otros nodos. Los microservicios deben ser concurrentes para permitir la comunicación simultánea entre procesos remotos.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
En el desarrollo de este proyecto, se ha logrado la creación exitosa del servidor central utilizando Express, un framework de Node.js ampliamente utilizado para la creación de servidores web.
Esto proporciona una base sólida y confiable para la gestión de la comunicación entre los nodos del sistema. Además, se han realizado pruebas de las peticiones a través de la API utilizando Postman, asegurando así la funcionalidad y fiabilidad de las interacciones 
entre los diferentes componentes del sistema. Por último, la comunicación entre los peer y el servidor central se ha implementado eficazmente utilizando Axios, una biblioteca HTTP basada en promesas, que permite realizar solicitudes tanto desde el servidor central como 
entre los nodos, garantizando así una conectividad fluida y eficiente en la red peer-to-peer.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
 hay aspectos que no se lograron cumplir o desarrollar completamente en este proyecto. En primer lugar, la comunicación utilizando gRPC y MOM no fue implementada según lo especificado.
 Estas tecnologías son importantes para la comunicación entre los nodos y podrían haber mejorado la eficiencia y escalabilidad del sistema. Además, el proyecto no fue desplegado en AWS, lo cual podría haber proporcionado acceso remoto y escalabilidad en la nube.
 Finalmente, el programa no fue dockerizado, lo que habría facilitado su despliegue y gestión en diferentes entornos. Estos aspectos representan áreas de mejora que podrían fortalecer la funcionalidad y la robustez del sistema.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
El diseño de alto nivel de este proyecto se basó en una arquitectura peer-to-peer (P2P), lo que significa que los nodos o pares del sistema interactúan directamente entre sí, sin depender de un servidor centralizado. 
Esta arquitectura descentralizada permite una mayor escalabilidad y resiliencia, ya que cada nodo puede actuar tanto como cliente como servidor.

En cuanto a las prácticas de API, se implementaron para facilitar la comunicación entre los nodos del sistema. 
Se utilizaron API REST para definir las interfaces de comunicación entre los nodos, lo que proporciona un enfoque estándar y flexible para el intercambio de datos. 
Además, el uso de Postman para realizar pruebas de API ayudó a garantizar la fiabilidad y funcionalidad de estas interfaces.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
- Lenguaje de programación: Node.js
- Framework web: Express.js
- Librería para hacer peticiones HTTP: Axios
- Herramienta para realizar pruebas de API: Postman
## como se compila y ejecuta.
- Para compilar y ejecutar este proyecto, primero se debe asegurar que Node.js esté instalado en el sistema. Luego, los pasos serían los siguientes:
   - Instalación de dependencias: Abrir una terminal en el directorio del proyecto y ejecutar el siguiente comando para instalar las dependencias necesarias: ```npm install```
   - Ejecución del servidor: Iniciar el servidor central ejecutando el siguiente comando en la terminal: ```node serverc.js```
   - Ejecución de los nodos/peers: Abrir una nueva terminal para cada nodo/peer y ejecutar el siguiente comando para cada uno: ```node peerc.js```
-  Una vez que el servidor y los peers estén en funcionamiento, se pueden realizar peticiones a través de Postman. Abra Postman y realice las solicitudes HTTP según la API definida en el servidor y los endpoints disponibles en los peers.
## detalles del desarrollo.
- Implementación de la Comunicación entre Nodos
  - Arquitectura P2P: Se estableció una arquitectura peer-to-peer (P2P) para la comunicación entre nodos, permitiendo la interacción directa entre pares sin necesidad de un servidor centralizado.
  - Express.js para el Servidor Central: Se desarrolló un servidor central utilizando Express.js, aprovechando su capacidad para manejar rutas, middleware y solicitudes HTTP.
  - Comunicación entre Nodos: Axios se utilizó para facilitar la comunicación entre los nodos del sistema. Esta biblioteca proporcionó una forma sencilla de realizar solicitudes HTTP tanto desde el servidor central como entre los nodos pares.
- Pruebas de la API con Postman
  - Pruebas de Funcionalidad: Se realizaron pruebas exhaustivas de la API utilizando Postman para garantizar su correcto funcionamiento. Se probaron diferentes endpoints y escenarios de uso para validar la funcionalidad del sistema.
  - Validación de Peticiones HTTP: Postman permitió enviar y recibir solicitudes HTTP, lo que facilitó la validación de la comunicación entre los nodos y la correcta interpretación de las respuestas.
## detalles técnicos
- Gestión de Dependencias y Versiones
  - npm: Se utilizó npm para gestionar las dependencias del proyecto. Las versiones de las bibliotecas y paquetes utilizados se especificaron en el archivo ```package.json```
- Configuración del Servidor Central
  - Express Middleware: Se configuraron middlewares de Express para manejar la lógica de las solicitudes HTTP entrantes, como el enrutamiento, la validación de datos y la gestión de errores.
  - Endpoints de API: Se definieron endpoints de API RESTful para permitir a los nodos realizar consultas y compartir información sobre los archivos disponibles en la red.
- Comunicación entre Nodos
  - Axios: La comunicación entre los nodos se realizó utilizando Axios, una biblioteca HTTP basada en promesas que facilita la realización de solicitudes HTTP tanto desde el servidor central como entre los nodos pares.
  - Protocolos de Comunicación: Se implementaron protocolos de comunicación estándar para garantizar la interoperabilidad entre los nodos, lo que facilitó la integración y la expansión del sistema en el futuro.
- Pruebas de Integración
  - Postman Collection: Se creó una colección de Postman que contiene todas las solicitudes necesarias para probar la funcionalidad del sistema, lo que facilitó la realización de pruebas de integración y la validación del comportamiento esperado de la API.
  - Ambientes de Prueba: Se configuraron ambientes de Postman para separar las pruebas realizadas en entornos de desarrollo, pruebas y producción, lo que permitió realizar pruebas de extremo a extremo en diferentes etapas del ciclo de vida del software.

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
- Lenguaje de Programación y Entorno de Ejecución
  - Node.js: La aplicación se ejecuta en un entorno de Node.js en producción. Se utiliza Node.js debido a su eficiencia y escalabilidad para aplicaciones basadas en JavaScript.
- Framework y Librerías
  - Express.js: El servidor web en producción sigue utilizando Express.js como su framework principal. Express.js proporciona una manera sencilla y flexible de manejar rutas, middleware y solicitudes HTTP.
  - Axios: La biblioteca Axios sigue siendo utilizada para realizar solicitudes HTTP entre los nodos en el entorno de producción. Se utiliza para facilitar la comunicación entre los distintos componentes del sistema.
- Gestión de Dependencias y Versiones
  - npm: La gestión de dependencias se realiza a través de npm, al igual que en el entorno de desarrollo. Se especifican las versiones exactas de las dependencias en el archivo ```package.json``` para garantizar la consistencia en el entorno de producción.

# referencias:
## [sitio1-url ](https://grpc.io/docs/languages/node/quickstart/)
## [sitio2-url](https://grpc.io/docs/languages/node/basics/)
## [sitio3-url](https://chat.openai.com/auth/login)
