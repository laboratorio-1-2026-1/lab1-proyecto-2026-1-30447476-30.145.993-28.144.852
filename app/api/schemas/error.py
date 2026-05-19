from pydantic import BaseModel
from datetime import datetime

# Schema para errores (como pide el profesor)
class ErrorResponse(BaseModel):
    error: str
    codigoInterno: str
    mensaje: str
    timestamp: datetime