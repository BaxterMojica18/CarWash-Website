from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import create_tables
from app.routers import auth, settings, invoices, reports
import os

app = FastAPI(
    title="Car Wash Manager API",
    description="Backend API for dashboard, invoicing, and settings.",
    version="1.0.2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    create_tables()
    print("Database tables ensured.")
except Exception as e:
    print(f"Warning: Could not initialize database tables: {e}")
    print("Server will continue running. Check database connection.")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/{page}.html")
def read_page(page: str):
    file_path = f"frontend/{page}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Page not found"}

# Serve frontend static files
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
