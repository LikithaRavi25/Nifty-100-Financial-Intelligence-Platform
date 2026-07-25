from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.middleware import log_requests
from src.api.routes.companies import router as companies_router
from src.api.routes.screener import router as screener_router
from src.api.routes.sectors import router as sectors_router
from src.api.routes.peers import router as peers_router
from src.api.routes.valuation import router as valuation_router
from src.api.routes.portfolio import router as portfolio_router
from src.api.routes.documents import router as documents_router
from src.api.routes.health import router as health_router

app = FastAPI(

    title="NIFTY 100 Financial Intelligence API",

    version="1.0.0",

    description="REST API for Financial Intelligence Platform"

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)
app.middleware("http")(log_requests)
app.include_router(
    companies_router,
    prefix="/api/v1"
)

app.include_router(
    screener_router,
    prefix="/api/v1"
)

app.include_router(
    sectors_router,
    prefix="/api/v1"
)

app.include_router(
    peers_router,
    prefix="/api/v1"
)

app.include_router(
    valuation_router,
    prefix="/api/v1"
)

app.include_router(
    portfolio_router,
    prefix="/api/v1"
)

app.include_router(
    documents_router,
    prefix="/api/v1"
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

@app.get("/")

def root():

    return {

        "message":

        "NIFTY 100 Financial Intelligence API"

    }