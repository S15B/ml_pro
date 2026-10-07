import time
import uuid
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, Field

from cost import db
from cost.config import settings


class Features(BaseModel):
    model_config = {"extra": "forbid"}

    geo_lat: float = Field(ge=-90, le=90)
    geo_lon: float = Field(ge=-180, le=180)
    region: int
    building_type: int
    level: int = Field(ge=1, le=40)
    levels: int = Field(ge=1, le=40)
    rooms: int = Field(ge=0, le=5)
    area: float = Field(gt=0, le=200)
    kitchen_area: float = Field(gt=0, le=100)
    object_type: int = Field(ge=0, le=1)
    days_passed: int = Field(ge=0)
    mortgage_rate: float | None = Field(ge=0)
    usd_rate: float | None = Field(gt=0)
    relative_level: float = Field(gt=0, le=1)
    is_last_level: int = Field(ge=0, le=1)
    distance: float = Field(ge=0)


class Prediction(BaseModel):
    #model_config = {"protected_namespaces": ()}

    price: float
    model_version: str
    request_id: str
    latency_ms: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = joblib.load(settings.model_path)
    app.state.pipeline = bundle["pipeline"]
    app.state.meta = bundle["metadata"]
    app.state.version = bundle["metadata"]["version"]

    db.init()
    yield
    app.state.pipeline = None


app = FastAPI(title="cost-predict", version="0.1.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model_version": getattr(app.state, "version", "unknown")}

@app.get("/ready")
def ready():
    if getattr(app.state, "pipeline", "None") is  None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"status": "ready"}



@app.post("/v1/predict")
def predict(x: Features, bg: BackgroundTasks) -> Prediction:
    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())
    payload = x.model_dump()

    frame = pd.DataFrame([payload]).astype({"region": "object", "building_type": "object"})
    frame = frame.loc[:, app.state.meta["features"]]

    price = float(app.state.pipeline.predict(frame)[0])

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    bg.add_task(db.save_prediction, request_id, payload, price, app.state.version, latency_ms)

    return Prediction(price=price, model_version = app.state.version, request_id=request_id, latency_ms=latency_ms)








