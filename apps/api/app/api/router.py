from fastapi import APIRouter

from app.api.routers import agents, auth, calls, clients, dashboard, knowledge, templates, tenants, wizard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tenants.router)
api_router.include_router(clients.router)
api_router.include_router(agents.router)
api_router.include_router(wizard.router)
api_router.include_router(calls.router)
api_router.include_router(dashboard.router)
api_router.include_router(templates.router)
api_router.include_router(knowledge.router)
