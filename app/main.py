from fastapi import FastAPI

from .routes.todos import router as todos_router
from .utils.exceptions import add_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo List API",
        description="A simple FastAPI application for creating, listing, and managing to-do items",
        version="0.1.0"
    )

    app.include_router(todos_router)
    add_exception_handlers(app)

    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "Welcome to the Todo List API",
            "routes": {
                "create_todo": "/todos/",
                "list_todos": "/todos/?status=pending",
                "complete_todo": "/todos/{todo_id}/complete",
                "delete_todo": "/todos/{todo_id}"
            },
            "docs": "/docs",
            "openapi": "/openapi.json"
        }

    return app
