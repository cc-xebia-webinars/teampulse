import logging
import time

from fastapi import Request

logger = logging.getLogger("teampulse.api")


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = int((time.perf_counter() - start_time) * 1000)
    logger.info("%s %s %s %sms", request.method, request.url.path, response.status_code, elapsed_ms)
    return response
