from typing import Any
from fastapi.responses import JSONResponse


class ApiResponse:
    @staticmethod
    def _json(message: str | None, status: int) -> JSONResponse:
        return JSONResponse(content={"message": message}, status_code=status)

    @staticmethod
    def ok(content: Any) -> JSONResponse:
        return JSONResponse(content=content)

    @staticmethod
    def ok_with_message(message: str) -> JSONResponse:
        return ApiResponse._json(message, 200)

    @staticmethod
    def bad_request(message: str) -> JSONResponse:
        return ApiResponse._json(message, 400)

    @staticmethod
    def error(message: str) -> JSONResponse:
        return ApiResponse._json(message, 500)

    @staticmethod
    def not_found(message: str | None = None) -> JSONResponse:
        return ApiResponse._json(message or "Not found", 404)

    @staticmethod
    def unauthorized() -> JSONResponse:
        return ApiResponse._json("Unauthorized", 401)

    @staticmethod
    def forbidden() -> JSONResponse:
        return ApiResponse._json("Forbidden", 403)
