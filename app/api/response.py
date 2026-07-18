from fastapi.responses import JSONResponse


def success_response(data=None, message="Operación exitosa", code=200):
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "message": message,
            "response": data,
        },
    )
