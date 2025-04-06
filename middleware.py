from typing import Any, Coroutine, Callable, Awaitable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from  starlette.middleware.base import BaseHTTPMiddleware
from acces_token import verefy_token
from route import public_router
from starlette.responses import Response


class VerefySessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        print(f"Request path: {request.url.path}")
        
        # Список публичных маршрутов
        public_urls = ["","/docs", "/openapi.json", "/traslate"] + [route.path for route in public_router.routes]
        
        if request.url.path in public_urls:
            # Если маршрут публичный, пропускаем запрос без проверки токена
            response = await call_next(request)
            return response
        try:
            await verefy_token(request)
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": f"Internal server error: {e}"})