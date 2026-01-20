from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommender import recommend_trip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    text: str
    traveller_type: str

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/recommend")
def recommend(req: TripRequest):
    plans = recommend_trip(req.text, req.traveller_type)
    return {
        "plans": plans
    }
