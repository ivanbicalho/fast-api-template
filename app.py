from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes import users_route
import logging

logger = logging.getLogger(__name__)

# Multiple versions: https://github.com/tiangolo/fastapi/issues/381#issuecomment-584132553

app = FastAPI(
    title="Architectural API in Python",
    description="Architectural API in Python",
    terms_of_service="",
    contact={
        "Developer name": "Ivan Bicalho",
        "email": "ivanribeirob@gmail.com",
        "Website Address": "https://www.ivanbicalho.com",
    },
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
)


@app.exception_handler(Exception)
async def custom_http_exception_handler(request, exc) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    headers = getattr(exc, "headers", None)
    return JSONResponse({"detail": "Internal server error"}, status_code=500, headers=headers)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8080"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=["*"],
# )

app.include_router(users_route.router)
