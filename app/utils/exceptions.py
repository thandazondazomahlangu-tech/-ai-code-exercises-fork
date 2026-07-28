from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class TodoNotFoundError(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        self.message = f"Todo item with ID {todo_id} not found"
        super().__init__(self.message)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(TodoNotFoundError)
    async def todo_not_found_handler(request: Request, exc: TodoNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation error in request data",
                "errors": exc.errors()
            }
        )
