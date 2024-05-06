1. Breve Descripción de la Actividad
Se desplegó un CMS, específicamente WordPress, con dominio propio y certificado SSL para el sitio reto3.sudominio.tld. Este despliegue incluyó la utilización de un balanceador de cargas Nginx en la capa de aplicación. Además, se configuraron dos servidores adicionales: uno para la base de datos, que puede ser Dockerizada o nativa, y otro como servidor de archivos implementando NFS, todo dentro de un clúster de Kubernetes diseñado para alta disponibilidad.

1.1 Aspectos Cumplidos
Se configuró correctamente un clúster en AWS EKS, implementando alta disponibilidad en el balanceador de cargas, la base de datos y la capa de almacenamiento. Se desplegó una base de datos dentro del clúster y se estableció el servicio de dominio, aunque solo en HTTP.

1.2 Aspectos No Cumplidos
No se logró implementar el servidor de archivos NFS ni se configuró el HTTPS para el dominio, quedando pendientes estas configuraciones para la seguridad y funcionalidad completa del sistema.

2. Información General de Diseño
A lo largo del curso, se han explorado diversos entornos de despliegue de aplicaciones, desde servidores propios hasta servidores en la nube administrados que ofrecen mejor disponibilidad y reducción de costos. El proyecto actual avanzó de una implementación dockerizada con un balanceador de cargas básico a una configuración más compleja y escalable utilizando Kubernetes en servicios de nube como AWS EKS o Google Cloud's Kubernetes.

3. Descripción del Ambiente de Desarrollo Técnico
Para el desarrollo se utilizó el laboratorio de AWS Academy específicamente para EKS. Las tecnologías y versiones incluyeron:

WordPress: última versión disponible
MySQL: versión 5.7
Kubernetes: versión 1.9
kubectl: herramienta de línea de comando para la gestión del clúster de Kubernetes
Estas herramientas y versiones proporcionan una base sólida para la gestión y el despliegue eficiente de aplicaciones dentro de un entorno de Kubernetes, aprovechando las ventajas de la escalabilidad y la gestión de infraestructura que ofrece AWS EKS.