# Servicios de traducción profesional 

Este proyecto es una **API de saludo** desarrollada con **FastAPI** y **Docker**. Está diseñada para funcionar como bienvenida y gestión de identidad dew una página de servicios de traducción.

## Objetivo del proyecto
Proporcionar una interfaz para gestionar saludos corporativos en múltiples idiomas, asegurando que cada cliente reciba una atención personalizada según su idioma, título profesional y contexto temporal.

---

## Funcionalidades (Endpoints)

La API ha sido estructurada siguiendo los estándares **RESTful** y las necesidades del dominio de traducción:

* **`GET /` (Información de la API)**: Punto de entrada que detalla la versión actual y lista los códigos de idioma ISO 639-1 soportados por el motor de traducción.
* **`GET /greet/{name}` (Traducción Dinámica)**: Genera un saludo basado en el idioma del cliente. Implementa una lógica de *fallback* automático al español si el idioma solicitado no está en el catálogo.
* **`GET /greet/{name}/formal` (Localización Corporativa)**: Endpoint especializado para comunicaciones ejecutivas que permite la integración de títulos profesionales (`Dr.`, `Ing.`, `Lic.`, etc.).
* **`GET /greet/{name}/time-based` (Contexto Temporal)**: Servicio inteligente que adapta el mensaje según la hora del día (Mañana, Tarde, Noche) para mejorar la experiencia del usuario.
* **`GET /health` (Estado del Servicio)**: Endpoint de monitoreo vital para entornos de **DevOps** y orquestación de contenedores.



---

## Arquitectura y decisiones Técnicas

* **FastAPI**: Elegido por su alto rendimiento, validación automática de datos con Pydantic y generación nativa de documentación **OpenAPI (Swagger)**.
* **Modularidad**: Se separó la lógica de negocio (como el cálculo del período del día) en funciones auxiliares para facilitar el mantenimiento y las futuras pruebas unitarias.
* **Gestión de Dependencias con `uv`**: Se utiliza `uv` por su velocidad superior en la resolución de paquetes y la creación de entornos deterministas.
* **Contenerización con Docker**: El proyecto está completamente dockerizado para garantizar la paridad entre los entornos de desarrollo y producción, eliminando el problema de "en mi máquina sí funciona".



---

## Instalación y despliegue

1.  **Construir y levantar el contenedor:**
    ```bash
    docker compose up --build
    ```

2.  **Acceder a la API:**
    * API Base: `http://localhost:8000`
    * Documentación Interactiva: `http://localhost:8000/docs`

---

## Especificaciones de dominio
* **Estándar de Idiomas**: Los códigos de idioma siguen el estándar internacional (es, en, fr, de, it, pt).
* **Configuración de Entorno**: El servicio está optimizado para Docker evitando la generación de archivos `.pyc` y forzando el volcado de logs en tiempo real para un monitoreo efectivo.