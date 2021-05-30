from fastapi import FastAPI
from fastapi import Request, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    try:
        request_body = await request.json()
        print(request_body)
        request.app.logger.info(request_body)
    except Exception:
        pass

    # response data, seems only useful when the response is default Response
    content = b''
    async for chunk in response.body_iterator:
        content += chunk
    response_data = str(content, encoding='utf-8')


    return Response(
        content=content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


@app.get("/")
async def root():
    response = {"message": "Hello World"}
    status = 200
    return JSONResponse(content=response, status_code=status)


class Test(BaseModel):
    id: str
    name: str


@app.post("/test_post/")
    # @ LOG INCOMING - OUTGOING STUFF
async def testing(request: Test, r: Request):
    a = await r.json()
    response = {"message": "Success"}
    status = 200
    return JSONResponse(content=response, status_code=status)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("toot.main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
