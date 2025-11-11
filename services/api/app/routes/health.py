from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/healthz", tags=["system"])
async def healthz():
    return JSONResponse(content={"status": "ok"}, status_code=200)
