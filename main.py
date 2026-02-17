"""
FastAPI application with GET and PATCH endpoints for
organization datasource connections.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Test API — Organization Datasource Connections",
    version="0.1.0",
)


# ─── Models ───────────────────────────────────────────────────────────────────
class Credentials(BaseModel):
    AppName: str
    AppSecret: str
    AppKey: str
    BaseURL: str


class FoundryConfig(BaseModel):
    profiles_dataset_rid: str
    visits_dataset_rid: str


class ConnectionResponse(BaseModel):
    id: str
    credentials: Credentials
    foundryConfig: FoundryConfig
    last_sync_at: Optional[str] = None


class PatchConnectionRequest(BaseModel):
    last_sync_at: str = Field(
        ...,
        description="ISO-8601 timestamp of the most recent sync.",
    )


class PatchConnectionResponse(BaseModel):
    id: str
    last_sync_at: str
    message: str


# ─── In-memory data store (dummy data) ───────────────────────────────────────
DUMMY_CONNECTIONS: Dict[str, Dict[str, Any]] = {
    "conn_001": {
        "id": "conn_001",
        "credentials": {
            "AppName": "CheraCare Portal",
            "AppSecret": "sk-9f8e7d6c5b4a3210-dead-beef-cafe",
            "AppKey": "ak-1234-5678-abcd-efgh",
            "BaseURL": "https://api.cheracare.example.com/v1",
        },
        "foundryConfig": {
            "profiles_dataset_rid": "ri.foundry.main.dataset.aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "visits_dataset_rid": "ri.foundry.main.dataset.11111111-2222-3333-4444-555555555555",
        },
        "last_sync_at": None,
    },
    "conn_002": {
        "id": "conn_002",
        "credentials": {
            "AppName": "CheraCare Mobile",
            "AppSecret": "sk-0123abcd4567efgh-8901-ijkl-mnop",
            "AppKey": "ak-wxyz-9876-lmno-pqrs",
            "BaseURL": "https://mobile-api.cheracare.example.com/v2",
        },
        "foundryConfig": {
            "profiles_dataset_rid": "ri.foundry.main.dataset.ffffffff-0000-1111-2222-333333333333",
            "visits_dataset_rid": "ri.foundry.main.dataset.66666666-7777-8888-9999-aaaaaaaaaaaa",
        },
        "last_sync_at": "2026-02-16T08:30:00+00:00",
    },
}


# ─── GET endpoint ─────────────────────────────────────────────────────────────
@app.get(
    "/backend/datasources/organizations/connections",
    response_model=List[ConnectionResponse],
    summary="List all organisation datasource connections",
)
async def get_connections():
    """
    Return every connection with its credentials, Foundry config,
    and the timestamp of the most recent sync (if any).
    """
    return list(DUMMY_CONNECTIONS.values())


# ─── GET by ID endpoint ──────────────────────────────────────────────────────
@app.get(
    "/backend/datasources/organizations/connections/{organization_datasource_id}",
    response_model=ConnectionResponse,
    summary="Get a single connection by ID",
)
async def get_connection_by_id(
    organization_datasource_id: str = Path(
        ..., description="ID of the connection to retrieve"
    ),
):
    """
    Return a single connection's credentials, Foundry config,
    and last sync timestamp.

    This is the endpoint consumed by `get_connection_details()`.
    """
    connection = DUMMY_CONNECTIONS.get(organization_datasource_id)
    if connection is None:
        raise HTTPException(
            status_code=404,
            detail=f"Connection '{organization_datasource_id}' not found.",
        )
    return connection


# ─── PATCH endpoint ──────────────────────────────────────────────────────────
@app.patch(
    "/backend/datasources/organizations/connections/{organization_datasource_id}",
    response_model=PatchConnectionResponse,
    summary="Update last_sync_at for a connection",
)
async def patch_connection(
    payload: PatchConnectionRequest,
    organization_datasource_id: str = Path(
        ..., description="ID of the connection to update"
    ),
):
    """
    Accept a JSON body with `last_sync_at` (ISO-8601 string) and
    persist it against the given connection ID.

    This is the endpoint consumed by `update_connection_status()`.
    """
    connection = DUMMY_CONNECTIONS.get(organization_datasource_id)
    if connection is None:
        raise HTTPException(
            status_code=404,
            detail=f"Connection '{organization_datasource_id}' not found.",
        )

    connection["last_sync_at"] = payload.last_sync_at

    return PatchConnectionResponse(
        id=organization_datasource_id,
        last_sync_at=payload.last_sync_at,
        message="last_sync_at updated successfully",
    )


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
