from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager
from src.core import cache
from src.api.routes.parcels import router as parcels_router

import asyncio

from src.resources import strings
from src.utils import utils


async def startup_event():
    try:
        asyncio.create_task(cache.schedule_currency_update())
    except Exception as e:
        print(f"Startup failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield


def get_application() -> FastAPI:

    application = FastAPI(
        title="International Delivery Service",
        # docs_url="/docs",
        # openapi_url="/openapi.json",
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
        if request.cookies.get(strings.SESSION_KEY) is None:
            response.set_cookie(key=strings.SESSION_KEY, value=utils.generate_uuid(), httponly=True)
        return response

    # application.add_event_handler(
    #     "startup", lambda: asyncio.create_task(tasks.schedule_currency_update())
    # )

    application.include_router(parcels_router, tags=["parcels"], prefix="/parcels")

    return application


app = get_application()

# settings = get_app_settings()
# settings.configure_logging()
# application = FastAPI(**settings.fastapi_kwargs)
# app = FastAPI()

# Base.metadata.create_all(bind=engine)


# @app.on_event("startup")
# async def startup_event():
#     """Starts Redis and schedules the shipping cost calculation task."""
#     redis = get_redis()
#     await schedule_shipping_cost_calculation(redis)


# @app.get("/health", tags=["Health Check"])
# async def health_check():
#     """Health check endpoint."""
#     return {"status": "ok"}


# @app.post("/currency", response_model=CurrencyResponse, tags=["Currency"])
# async def get_exchange_rate(db: Session = Depends(get_db)):
#     """Retrieves the dollar to ruble exchange rate."""
#     currency = db.query(Currency).first()
#     if not currency:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     return {"rate": currency.rate}


# def custom_openapi():
#     """Custom OpenAPI schema generation."""
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="International Delivery Service",
#         version="1.0.0",
#         description="API for managing parcels and calculating shipping costs",
#         routes=app.routes,
#     )
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi


# application.add_event_handler(
#     "startup",
#     create_start_app_handler(
#         application,
#         # settings,
#     ),
# )
# application.add_event_handler(
#     "shutdown",
#     create_stop_app_handler(application),
# )

# application.add_exception_handler(HTTPException, http_error_handler)
# application.add_exception_handler(RequestValidationError, http422_error_handler)
