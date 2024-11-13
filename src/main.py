from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
import uuid

# from src.redis import Redis
# from sqlalchemy.orm import Session

# from src.parcels.schemas import (
#     ParcelCreate,
#     Parcel,
#     ParcelType,
#     ParcelUpdate,
#     ParcelFilter,
#     ParcelList,
#     ParcelResponse,
#     Currency,
#     CurrencyResponse,
# )

# from src.utils import get_db, get_redis, calculate_shipping_cost, get_exchange_rate
# from src.tasks import schedule_shipping_cost_calculation
# from fastapi import APIRouter
from src.parcels.router import router as parcels_router

# from src.core.events import create_start_app_handler


def get_application() -> FastAPI:
    # settings = get_app_settings()
    # settings.configure_logging()
    # application = FastAPI(**settings.fastapi_kwargs)
    # app = FastAPI(title="International Delivery Service", docs_url="/docs", openapi_url="/openapi.json")

    application = FastAPI()

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
        if request.cookies.get("sessionKey") is None:
            response.set_cookie(key="sessionKey", value=str(uuid.uuid4()), httponly=True)
        return response

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

    application.include_router(parcels_router, tags=["parcels"], prefix="/parcels")

    return application


app = get_application()


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


# api_router = APIRouter()
# api_router.include_router(users.router, tags=["users"], prefix="/user")
# api_router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
# api_router.include_router(articles.router, tags=["articles"])
# api_router.include_router(
#     comments.router,
#     tags=["comments"],
#     prefix="/articles/{slug}/comments",
# )
# api_router.include_router(tags.router, tags=["tags"], prefix="/tags")
# application.include_router(api_router, prefix=settings.api_prefix)
