from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os

from config import settings
from routers import categories, resources, auth, admin, nodes, api_keys, enum_items, resource_themes

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

app.include_router(categories.router)
app.include_router(resources.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(nodes.router)
app.include_router(api_keys.router)
app.include_router(enum_items.router)
app.include_router(resource_themes.router)


@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
