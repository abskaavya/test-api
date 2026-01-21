import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import os

app = FastAPI()

# 1. Security Configuration
# We will look for a header named "X-Access-Token"
API_KEY_NAME = "X-Access-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Get the actual secret token from Environment Variables (for safety)
# If not set (local testing), it defaults to "my-secret-token"
REAL_API_KEY = os.getenv("API_SECRET", "my-secret-token")

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == REAL_API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

# 2. Load Data
# We load the CSV into memory when the app starts to be fast.
try:
    df = pd.read_csv("company_data.csv")
    # Convert NaN values to None so JSON can handle them
    data_store = df.where(pd.notnull(df), None).to_dict(orient="records")
except Exception as e:
    print(f"Error loading CSV: {e}")
    data_store = []

# 3. The Endpoint
@app.get("/data")
async def get_data(api_key: str = Depends(get_api_key)):
    """
    Returns the data only if the correct token is provided.
    """
    return {
        "count": len(data_store),
        "data": data_store
    }

@app.get("/")
def root():
    return {"message": "API is online. Use /data endpoint with a token."}