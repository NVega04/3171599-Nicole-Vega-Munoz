from fastapi import FastAPI

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

# Diccionario de servicios
TRANSLATION_SERVICES: dict[str, str] = {
    "es": "Bienvenido al servicio profesional de traducción, {name}.",
    "en": "Welcome to the professional translation service, {name}.",
    "fr": "Bienvenue au service de traduction professionnelle, {name}.",
    "de": "Willkommen beim professionellen Übersetzungsservice, {name}.",
    "it": "Benvenuti al servizio de traduzione professionale, {name}.",
    "pt": "Bem-vindo ao serviço de tradução profissional, {name}.",
}

# Servicios soportados (para documentación)
SUPPORTED_LANGUAGES = list(TRANSLATION_SERVICES.keys())


# ============================================
# TODO1: CREAR LA INSTANCIA DE FASTAPI
# ============================================

app = FastAPI(title="Servicios de traducción", description="API de servicios", version="1.0.0")


# ============================================
# TODO2: ENDPOINT RAÍZ
# ============================================

@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información de la API."""
    return {
        "name": "Servicios de traducción",
        "version": "1.0.0",
        "docs": "/docs",
        "languages": ["es", "en", "fr", "de", "it", "pt"]
    }

# ============================================
# TODO3: SALUDO PERSONALIZADO
# ============================================

@app.get("/greet/{name}")
async def greet(name: str, language: str = "es",) -> dict[str, str]:
    """
    Saluda a una persona en el idioma especificado.
    
    Args:
        name: Nombre de la persona
        language: Código de idioma (es, en, fr, de, it, pt)
    
    Returns:
        dict: Saludo personalizado
    """
    # Si el idioma no existe, usar español por defecto.
    template = TRANSLATION_SERVICES.get(language, TRANSLATION_SERVICES["es"])
    
    greeting_message = template.format(name=name)
    
    return {
        "greeting": greeting_message,
        "language": language if language in TRANSLATION_SERVICES else "es",
        "name": name
    }


# ============================================
# TODO4: SALUDO FORMAL
# ============================================

@app.get("/greet/{name}/formal")
async def greet_formal(name: str, title: str = "Sr./Sra.",) -> dict[str, str]:
    """
    Genera un saludo formal con título.
    
    Args:
        name: Nombre o apellido de la persona
        title: Título formal (Dr., Ing., Prof., Lic., etc.)
    
    Returns:
        dict: Saludo formal
    """
    # 1. Construir el saludo formal usando f-strings para mayor claridad
    formal_greeting = f"Estimado/a {title} {name}, es un placer saludarle."
    
    # 2. Retornar el diccionario con la estructura solicitada
    return {
        "greeting": formal_greeting,
        "title": title,
        "name": name
    }


# ============================================
# TODO5: SALUDO SEGÚN LA HORA
# ============================================

def get_day_period(hour: int) -> tuple[str, str]:
    """
    Determina el saludo y período según la hora.
    """
    # Implementamos la lógica de rangos
    if 5 <= hour < 12:
        return "Buenos días", "morning"
    elif 12 <= hour < 18:
        return "Buenas tardes", "afternoon"
    else:
        return "Buenas noches", "night"


@app.get("/greet/{name}/time-based")
async def greet_time_based(
    name: str,
    hour: int,
) -> dict[str, str | int]:
    """
    Saluda según la hora del día.
    """
    # 1. Validar que hour esté entre 0-23
    # Si la hora es inválida, podríamos lanzar un error, 
    # pero para este nivel base, vamos a limitarla o manejarla:
    if not (0 <= hour <= 23):
        return {"error": "La hora debe estar entre 0 y 23"}

    # 2. Usar get_day_period() para obtener el saludo y el período
    saludo_base, period = get_day_period(hour)
    
    # 3. Retornar el diccionario con el formato solicitado
    return {
        "greeting": f"{saludo_base}, {name}!",
        "hour": hour,
        "period": period
    }

# ============================================
# TODO6: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Verifica el estado de la API.
    Utilizado por Docker/Kubernetes para monitoreo.
    """
    return {
        "status": "healthy",
        "service": "greeting-api",
        "version": "1.0.0"
    }

# ============================================
# VERIFICACIÓN
# ============================================
# Una vez completados todos los TODOs:
#
# 1. Ejecutar:
#    docker compose up --build
#
# 2. Probar en el navegador:
#    http://localhost:8000/docs
#
# 3. Verificar cada endpoint:
#    - GET /
#    - GET /greet/Carlos
#    - GET /greet/Carlos?language=en
#    - GET /greet/García/formal?title=Dr.
#    - GET /greet/Ana/time-based?hour=10
#    - GET /health
# ============================================