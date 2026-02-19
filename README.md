# Test API — Organization Datasource Connections

A **FastAPI** service for managing organisation datasource connections (credentials, Palantir Foundry config, sync status). Backed by an in-memory dummy data store.

## ️ Stack

- **Python 3.11** · **FastAPI 0.115** · **Uvicorn 0.30** · **Pydantic v2**

## 🏁 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run (dev mode)
python main.py
# or
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`.  
Interactive docs → `http://localhost:8000/docs`

## � Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/backend/datasources/organizations/connections` | List all connections |
| `GET` | `/backend/datasources/organizations/connections/{id}` | Get connection by ID |
| `PATCH` | `/backend/datasources/organizations/connections/{id}` | Update `last_sync_at` |

**PATCH body:**
```json
{ "last_sync_at": "2026-02-19T10:00:00+00:00" }
```

## 📂 Structure

```
main.py            # App, models, and route handlers
requirements.txt   # Dependencies
.python-version    # Python 3.11.12
```
