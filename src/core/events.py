from typing import Callable

from fastapi import FastAPI, Response, Request

# from loguru import logger

# from app.core.settings.app import AppSettings
# from app.db.events import close_db_connection, connect_to_db


# @router.get("/set_cookie/")
# async def set_cookie(response: Response):
#     response.set_cookie(key="sessionKey", value=str(uuid.uuid4()), httponly=True)
#     return {"message": "Cookie has been set"}


# def create_start_app_handler(
#     app: FastAPI,
#     # settings: AppSettings,
# ) -> Callable:  # type: ignore
# async def start_app() -> None:
#     await connect_to_db(app, settings)

# return start_app


# def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
#     @logger.catch
#     async def stop_app() -> None:
#         await close_db_connection(app)

#     return stop_app
