from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError


from app.db.database import engine, Base
from app.api.erros import sqlalchemy_integrity_exception_handler, global_exception_handler
from app.api.routes import auth_route, users_route, records_route, dashboard_route
from app.db.init_db import bootstrap_system




def create_tables():
    Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI(title = "Finance Dashboard API", version = "1.0.0")
    
    load_dotenv()
    create_tables()
    bootstrap_system()
    

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(IntegrityError, sqlalchemy_integrity_exception_handler)
    application.add_exception_handler(Exception, global_exception_handler)

    application.include_router(auth_route.router)
    application.include_router(users_route.router)
    application.include_router(records_route.router)
    application.include_router(dashboard_route.router)

    return application

app = get_application()