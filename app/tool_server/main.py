from fastapi import FastAPI

from app.tool_server.routes import router

app = FastAPI(title="Tool Server")

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
