from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import engine, Base
from app.routers import dashboard, countries, employees, payroll
from app.seed import seed_data

# Create tables and seed if empty
Base.metadata.create_all(bind=engine)

# Check if data exists, seed if not
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Country

db = SessionLocal()
if db.query(Country).count() == 0:
    print("No data found. Seeding database...")
    seed_data()
else:
    print("Database already seeded.")
db.close()

app = FastAPI(
    title="GlobalPayroll Dashboard API",
    description="Multi-country payroll management API with realistic compliance data",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(dashboard.router, prefix="/api")
app.include_router(countries.router, prefix="/api")
app.include_router(employees.router, prefix="/api")
app.include_router(payroll.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "GlobalPayroll API"}


# Serve static frontend files in production
frontend_dist = os.path.join(os.path.dirname(__file__), "../../dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
    
    @app.get("/{path:path}")
    def catch_all(path: str):
        return FileResponse(os.path.join(frontend_dist, "index.html"))
