"""
FastAPI application with GET and PATCH endpoints for
organization datasource connections.
"""

from re import A
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
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
    foundry_config: FoundryConfig
    lastSyncAt: Optional[str] = None


class PatchConnectionRequest(BaseModel):
    lastSyncAt: Union[datetime, str] = Field(
        ...,
        description="ISO-8601 timestamp of the most recent sync (datetime or string).",
    )

    def lastSyncAt_iso(self) -> str:
        """Always return an ISO-8601 string regardless of input type."""
        if isinstance(self.lastSyncAt, datetime):
            return self.lastSyncAt.isoformat()
        return self.lastSyncAt


class PatchConnectionResponse(BaseModel):
    id: str
    lastSyncAt: str
    message: str


# ─── In-memory data store (dummy data) ───────────────────────────────────────
DUMMY_CONNECTIONS: Dict[str, Dict[str, Any]] = {
    "conn_001": {
        "id": "conn_001",
        "credentials": {
            "AppName": "Perry",
            "AppSecret": "876442f4-6468-4f0e-bbbe-c97f82aa1e86",
            "AppKey": "MQAwADMANwA4ADEANwAtADIARQA0ADQAQgBEAEQAOQA1ADIAOQA1ADQAQQBGAEYARAA3ADkAMQBCADgARQBCADUANQBDADgAOABEAA==",
            "BaseURL": "https://cloud.hhaexchange.com",
        },
        "foundry_config": {
            "profiles_dataset_rid": "ri.foundry.main.dataset.11c3e68b-7bfc-4783-82df-a8865663ca8b",
            "visits_dataset_rid": "ri.foundry.main.dataset.57a68f07-1a41-43ea-a188-3611d68f83c5",
        },
        "lastSyncAt": None,
    },
    "conn_002": {
        "id": "conn_002",
        "credentials": {
            "AppName": "Perry", #caresphere llc
            "AppSecret": "443ac9ad-6ac6-4c8f-855b-6460b3d99288",
            "AppKey": "MQA2ADQANgAxADQALQAxADcAOQA4ADAAMABBAEQAMABEADYARQAwAEQAMgA5ADcAQwAyAEUANgAzAEQAOABGADQAMAA0ADkAOAA=",
            "BaseURL": "https://app2.hhaexchange.com",
        },
        "foundry_config": {
            "profiles_dataset_rid": "ri.foundry.main.dataset.a64b4790-85ba-49ef-b320-d077ac044637",
            "visits_dataset_rid": "ri.foundry.main.dataset.dec9dedd-23f5-4a15-ba7d-672226944caf",
        },
        "lastSyncAt": "2026-02-16T08:30:00+00:00",
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
    summary="Update lastSyncAt for a connection",
)
async def patch_connection(
    payload: PatchConnectionRequest,
    organization_datasource_id: str = Path(
        ..., description="ID of the connection to update"
    ),
):
    """
    Accept a JSON body with `lastSyncAt` (ISO-8601 string) and
    persist it against the given connection ID.

    This is the endpoint consumed by `update_connection_status()`.
    """
    connection = DUMMY_CONNECTIONS.get(organization_datasource_id)
    if connection is None:
        raise HTTPException(
            status_code=404,
            detail=f"Connection '{organization_datasource_id}' not found.",
        )

    connection["lastSyncAt"] = payload.lastSyncAt_iso()

    return PatchConnectionResponse(
        id=organization_datasource_id,
        lastSyncAt=payload.lastSyncAt_iso(),
        message="lastSyncAt updated successfully",
    )


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
