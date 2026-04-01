from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from jose import JWTError, jwt

from app.chatkit_server import create_chatkit_server
from app.chatkit_store import RequestContext
from app.config import settings
from app.database import create_db_and_tables
from app.routers.chat import router as chat_router
from app.routers.tasks import router as tasks_router
from chatkit.server import StreamingResult


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Todo API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3030"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)
app.include_router(chat_router)

chatkit_server = create_chatkit_server()


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return Response(content='{"error":"Unauthorized"}', status_code=401, media_type="application/json")

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
    except JWTError:
        return Response(content='{"error":"Invalid token"}', status_code=401, media_type="application/json")

    user_id = payload.get("sub")
    if not user_id:
        return Response(content='{"error":"Invalid token payload"}', status_code=401, media_type="application/json")

    context = RequestContext(user_id=user_id)
    body = await request.body()
    result = await chatkit_server.process(body, context)

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


@app.get("/")
def health_check():
    return {"status": "ok"}
