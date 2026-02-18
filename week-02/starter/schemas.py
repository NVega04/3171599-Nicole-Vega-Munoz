"""
Schemas Pydantic para la API de Contactos
=========================================

TODO: Implementar los schemas según las especificaciones del proyecto.

Schemas requeridos:
- ContactBase: Campos comunes
- ContactCreate: Para POST (con validadores)
- ContactUpdate: Para PATCH (todos opcionales)
- ContactResponse: Para respuestas
- ContactList: Lista paginada
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from datetime import datetime
import re


# ============================================
# TODO 1: ContactBase
# Campos comunes para todos los schemas de contacto
# ============================================

class ContactBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="El nombre del contacto"
    )
    last_name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="El apellido del contacto"
    )
    email: EmailStr = Field(
        ..., 
        description="Correo electrónico"
    )
    phone: str = Field(
        ..., 
        description="Número de teléfono de contacto"
    )
    company: str | None = Field(
        None, 
        description="Empresa donde trabaja el contacto"
    )
    tags: list[str] = Field(
        default=[], 
        max_length=5, 
        description="Etiquetas de categorización (máximo 5)"
    )
    is_favorite: bool = Field(
        default=False, 
        description="Marca si el contacto es favorito"
    )

    model_config = ConfigDict(from_attributes=True)


# ============================================
# TODO 2: ContactCreate
# Schema para crear contactos (POST)
# Incluye validadores para normalizar datos
# ============================================

class ContactCreate(ContactBase):
    """
    Schema para crear contactos con normalización específica.
    """
    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_names(cls, v: str) -> str:
        # 1. Capitalizar nombres (Ej: "juan" -> "Juan")
        return v.strip().title()

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        # 2. Extraer dígitos y formatear a +57
        nums = re.sub(r"\D", "", v)[-10:]
        return f"+57 {nums[:3]} {nums[3:6]} {nums[6:]}"

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        # 3. Minúsculas, sin duplicados (set), máximo 5
        clean_tags = list({tag.strip().lower() for tag in v})
        return clean_tags[:5]

# ============================================
# TODO 3: ContactUpdate
# Schema para actualizar contactos (PATCH)
# Todos los campos son opcionales
# ============================================

class ContactUpdate(BaseModel):
    # Definimos todo como opcional
    first_name: str | None = Field(None, min_length=2, max_length=50)
    last_name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    tags: list[str] | None = None
    is_favorite: bool | None = None

    # Reutilizamos los validadores pero con una protección simple: "if v"
    @field_validator("first_name", "last_name", "phone", "tags")
    @classmethod
    def validate_if_present(cls, v, info):
        # Si el valor es None (no se envió), no validamos nada, solo lo devolvemos
        if v is None:
            return v
            
        # Si hay valor, aplicamos la lógica según el campo
        if info.field_name in ["first_name", "last_name"]:
            return v.strip().title()
            
        if info.field_name == "phone":
            nums = re.sub(r"\D", "", v)[-10:]
            return f"+52 {nums[:3]} {nums[3:6]} {nums[6:]}"
            
        if info.field_name == "tags":
            return list({tag.strip().lower() for tag in v})[:5]
            
        return v


# ============================================
# TODO 4: ContactResponse
# Schema para respuestas (incluye id y timestamps)
# ============================================

class ContactResponse(ContactBase):
    """
    Schema para devolver los datos del contacto al cliente.
    """
    id: int = Field(..., description="ID único del contacto en la base de datos")
    created_at: datetime = Field(..., description="Fecha y hora de creación")
    updated_at: datetime | None = Field(None, description="Fecha y hora de última actualización")

    model_config = ConfigDict(from_attributes=True)

# ============================================
# TODO 5: ContactList
# Schema para lista paginada
# ============================================

class ContactList(BaseModel):
    """
    Schema para manejar la respuesta de múltiples contactos con paginación.
    """
    items: list[ContactResponse] = Field(..., description="Lista de contactos de la página actual")
    total: int = Field(..., description="Número total de contactos en la base de datos")
    page: int = Field(..., description="Número de la página actual")
    per_page: int = Field(..., description="Cantidad de elementos por página")

    model_config = ConfigDict(from_attributes=True)
