from fastapi import FastAPI, HTTPException
from redis.cluster import RedisCluster
from pydantic import BaseModel
import uvicorn
from typing import Optional

app = FastAPI(title="Redis Cluster API")

# Redis Cluster configuration
startup_nodes = [
    {"host": "10.0.2.5", "port": 6379},
    {"host": "10.0.2.208", "port": 6379},
    {"host": "10.0.2.186", "port": 6379},
    {"host": "10.0.3.53", "port": 6379},
    {"host": "10.0.3.149", "port": 6379},
    {"host": "10.0.3.83", "port": 6379}
]

# Initialize Redis Cluster
try:
    redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
except Exception as e:
    print(f"Failed to connect to Redis Cluster: {str(e)}")
    raise

# Pydantic model for request validation
class KeyValue(BaseModel):
    key: str
    value: str

@app.get("/")
async def root():
    """Root route to confirm server is running"""
    return {"message": "FastAPI server is running!"}

@app.post("/set")
async def set_value(data: KeyValue):
    """Set a key-value pair in Redis"""
    try:
        await redis_cluster.set(data.key, data.value)
        return {"message": "Value set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get/{key}")
async def get_value(key: str):
    """Get a value by key from Redis"""
    try:
        value = await redis_cluster.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {key: value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

# Requirements:
# pip install fastapi uvicorn redis pydantic