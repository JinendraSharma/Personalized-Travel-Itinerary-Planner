from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.trips import router as trips_router

app = FastAPI(title="Personalized Travel Itinerary Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips_router)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
