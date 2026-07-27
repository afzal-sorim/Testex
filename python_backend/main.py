import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api
from app.routers import api_keys
from app.routers import technical_documents

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Assistant API")

@app.middleware("http")
async def add_ngrok_header_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Configure CORS origins dynamically to support local development and deployed frontend (Render)
cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
if cors_origins_str:
    origins = [o.strip().rstrip("/") for o in cors_origins_str.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

# Default to allow all Render subdomains to prevent CORS issues on Render deployment
cors_origins_regex = os.getenv("CORS_ALLOWED_ORIGINS_REGEX", r"https://.*\.onrender\.com") or None

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=cors_origins_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "error": "Validation Error"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detail": "Internal Server Error"}
    )

from app.routers import intelligence_api
from app.routers import report_api
from app.routers import export_api

app.include_router(api.router, prefix="/api")
app.include_router(api_keys.router)
app.include_router(technical_documents.router)
app.include_router(intelligence_api.router)
app.include_router(report_api.router)
app.include_router(export_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

