import structlog

logger = structlog.get_logger()


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class PromptBlockedError(AppError):
    def __init__(self, message: str = "Prompt violates content policy") -> None:
        super().__init__(
            code="PROMPT_BLOCKED",
            message=message,
            status_code=422,
        )


class JobNotFoundError(AppError):
    def __init__(self, job_id: str) -> None:
        super().__init__(
            code="JOB_NOT_FOUND",
            message=f"Job {job_id} not found",
            status_code=404,
        )


class GenerationFailedError(AppError):
    def __init__(self, message: str = "Image generation failed") -> None:
        super().__init__(
            code="GENERATION_FAILED",
            message=message,
            status_code=500,
        )


def register_exception_handlers(app: "FastAPI") -> None:  # type: ignore[name-defined]  # noqa: F821
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(
            "Application error",
            code=exc.code,
            message=exc.message,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": [],
                }
            },
        )
