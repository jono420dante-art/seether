from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Transparent Programs & Design API",
    description="AI-first automation engines for e-com/SaaS/dropshipping",
    version="1.0.0"
)

# Zero-trust security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jono-tower.fyi"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)

@app.get("/health")
async def health_check():
    return {"status": "operational", "version": "1.0.0"}
