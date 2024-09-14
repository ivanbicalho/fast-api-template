from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

from api.routes.v1 import users_route as users_route_v1
from api.routes.v1 import todo_route as todo_route_v1
from api.routes.v2 import users_route as users_route_v2

logger = logging.getLogger(__name__)

# There are a couple os ways to version API's in Fast API.
# A FastAPI app can have only one Swagger UI and in this repo we will use it this way
# If you want to have multiple docs like:
# By version:
#   - /v1/docs
#   - /v2/docs
# By resource:
#   /users/docs
#   /todo/docs
# You can have multiple FastAPI instances and use app.mount to add them to the a main app
# You can find more info here: https://github.com/tiangolo/fastapi/issues/381#issuecomment-584132553

app = FastAPI(
    title="Architectural API in Python",
    description="Architectural API in Python",
    terms_of_service="",
    contact={
        "name": "Ivan Bicalho",
        "email": "ivanribeirob@gmail.com",
        "url": "https://github.com/ivanbicalho/fast-api-template",
    },
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.exception_handler(Exception)
async def custom_http_exception_handler(request, exc) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    headers = getattr(exc, "headers", None)
    return JSONResponse({"detail": "Internal server error"}, headers=headers)


# CORS example:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8080"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=["*"],
# )

app.include_router(users_route_v1.router)
app.include_router(todo_route_v1.router)
app.include_router(users_route_v2.router)
