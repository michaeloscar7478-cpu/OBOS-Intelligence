from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OBOS Intelligence Backend",
    description="Backend API for the OBOS Agentic AI Operating System",
    version="1.0.0",
)

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
