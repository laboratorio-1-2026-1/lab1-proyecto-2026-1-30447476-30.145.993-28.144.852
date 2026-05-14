from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime

def bad_request_response(message: str, codigo_interno: str = "ERR_VALIDACION"):
    """Respuesta para error 400 Bad Request"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "codigoInterno": codigo_interno,
            "mensaje": message,
            "timestamp": datetime.now().isoformat()
        }
    )

def conflict_response(message: str, codigo_interno: str = "ERR_CONFLICTO"):
    """Respuesta para error 409 Conflict - Reglas de negocio"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "codigoInterno": codigo_interno,
            "mensaje": message,
            "timestamp": datetime.now().isoformat()
        }
    )

def created_response(mensaje: str, data: dict):
    """Respuesta para 201 Created - Éxito en creación"""
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "success",
            "mensaje": mensaje,
            "data": data
        }
    )