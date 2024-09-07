from typing import Mapping
from fastapi.responses import JSONResponse


class ApiResponse:
    @staticmethod
    def _json(message: str, status: int, headers: Mapping[str, str] = None) -> JSONResponse:
        return JSONResponse(content={"message": message}, status_code=status, headers=headers)

    @staticmethod
    def ok(message: str) -> JSONResponse:
        return ApiResponse._json(message, 200)

    @staticmethod
    def bad_request(message: str) -> JSONResponse:
        return ApiResponse._json(message, 400)

    @staticmethod
    def error(message: str, headers) -> JSONResponse:
        return ApiResponse._json(message, 500, headers=headers)

    @staticmethod
    def not_found(message: str | None = None) -> JSONResponse:
        return ApiResponse._json(message or "Not found", 404)

    @staticmethod
    def unauthorized() -> JSONResponse:
        return ApiResponse._json("Unauthorized", 401)

    @staticmethod
    def forbidden() -> JSONResponse:
        return ApiResponse._json("Forbidden", 403)
