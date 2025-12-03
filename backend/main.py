from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from upload import router as upload_router
from reasoning import router as reasoning_router
from diagnostic import router as diagnostic_router
app = FastAPI(
    title="OBOS Intelligence Backend",
    description="Backend API for the OBOS Agentic AI Operating System",
    version="1.0.0",
)
app.include_router(upload_router, prefix="/api")
app.include_router(reasoning_router, prefix="/api")
app.include_router(diagnostic_router, prefix="/api")
# Allow frontend to connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "OBOS Intelligence Backend is running!"}
