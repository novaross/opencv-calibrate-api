from fastapi import FastAPI
from .calibrate import router as calibrate
from .opencv import router as opencv

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
app.include_router(calibrate.router)
app.include_router(opencv.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
