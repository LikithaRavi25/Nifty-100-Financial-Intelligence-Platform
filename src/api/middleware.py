import time

from fastapi import Request


async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = round(time.time() - start, 4)

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{duration}s"
    )

    return response