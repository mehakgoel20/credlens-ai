from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI , Response
from app.api.routes_risk import router as risk_router
from app.api.routes_docs import router as docs_router
from app.api.routes_decision import router as decision_router
from app.api.routes_retrieve import router as retrieve_router
from app.api.routes_debug import router as debug_router
from app.api.routes_audit import router as audit_router
from app.db.session import create_db_and_tables
from app.api.routes_report import router as report_router
from app.api.routes_dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="CredLens AI", version="1.0")
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(risk_router, prefix="/risk", tags=["Risk Scoring"])
app.include_router(docs_router, prefix="/docs", tags=["Document Ingestion"])
app.include_router(decision_router, prefix="/decision", tags=["Decision Engine"])
app.include_router(retrieve_router, prefix="/retrieve", tags=["Policy Retrieval"])
app.include_router(debug_router, prefix="/debug", tags=["Debug"])
app.include_router(audit_router, prefix="/audit", tags=["Audit Logs"])
app.include_router(report_router, prefix="/report", tags=["Reports"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

app.mount(
    "/dashboard",
    StaticFiles(directory=os.path.join(BASE_DIR, "dashboard"), html=True),
    name="dashboard",
)


@app.get("/")
def root():
    return {"status": "CredLens AI running ✅"}
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)
