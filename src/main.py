from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.responses import JSONResponse

from src.api.routes import debug, parcels
from src.core.config import settings
from src.core.events import startup_event
from src.resources import strings
from src.utils import utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield


def get_application() -> FastAPI:

    application = FastAPI(
        title="International Delivery Service",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def add_cookie_middleware(request: Request, call_next):
        response: Response = await call_next(request)
        if request.cookies.get(settings.SESSION_KEY) is None:
            response.set_cookie(
                key=settings.SESSION_KEY, value=utils.generate_uuid(), httponly=True
            )
        return response

    @application.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        errors = [
            {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={"detail": strings.ERR_VALIDATION, "errors": errors},
        )

    application.include_router(parcels.router, tags=["parcels"], prefix="/api/parcels")
    application.include_router(debug.router, tags=["debug"], prefix="/debug/events")

    return application


app = get_application()
