from datetime import datetime, timezone
from fastapi import HTTPException, status


def _ts():
    return datetime.now(timezone.utc).isoformat() + "Z"


def conflict_response(codigo: str, mensaje: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"error": "Conflict", "codigoInterno": codigo,
                "mensaje": mensaje, "timestamp": _ts()},
    )


def not_found_response(codigo: str, mensaje: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": "Not Found", "codigoInterno": codigo,
                "mensaje": mensaje, "timestamp": _ts()},
    )


def bad_request_response(codigo: str, mensaje: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "Bad Request", "codigoInterno": codigo,
                "mensaje": mensaje, "timestamp": _ts()},
    )


def unauthorized_response(codigo: str, mensaje: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "Unauthorized", "codigoInterno": codigo,
                "mensaje": mensaje, "timestamp": _ts()},
        headers={"WWW-Authenticate": "Bearer"},
    )