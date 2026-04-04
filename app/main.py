from fastapi import FastAPI

def create_tables():
    ...

def get_application() -> FastAPI:
    application = FastAPI(title = "Finance Dashboard API", version = "1.0.0")

    return application

app = get_application()