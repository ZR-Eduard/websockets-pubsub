import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket.socketManager import WebSocketManager
import json
import argparse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

#parser = argparse.ArgumentParser()
#parser.add_argument("-p", "--port", default=8000, type=int)
#args = parser.parse_args()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI()

# Adding the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the public folder at /public
app.mount("/public", StaticFiles(directory="./public"), name="public")

socket_manager = WebSocketManager()

class MessageBody(BaseModel):
    message: str

@app.post("/broadcast/{room_id}/{user_id}")
async def broadcast_message(room_id: str, user_id: int, message_body: MessageBody):
    message = {
        "user_id": user_id,
        "room_id": room_id,
        "message": message_body.message
    }
    #await socket_manager.broadcast_to_room(room_id, json.dumps(message))
    await socket_manager.broadcast_to_room(room_id, json.dumps(message))
    return {"message": "Broadcasted successfully"}


@app.websocket("/api/v1/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: int):
    await socket_manager.add_user_to_room(room_id, websocket)
    message = {
        "user_id": user_id,
        "room_id": room_id,
        "message": f"User {user_id} connected to room - {room_id}"
    }
    await socket_manager.broadcast_to_room(room_id, json.dumps(message))
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "user_id": user_id,
                "room_id": room_id,
                "message": data
            }
            await socket_manager.broadcast_to_room(room_id, json.dumps(message))

    except WebSocketDisconnect:
        await socket_manager.remove_user_from_room(room_id, websocket)

        message = {
            "user_id": user_id,
            "room_id": room_id,
            "message": f"User {user_id} disconnected from room - {room_id}"
        }
        await socket_manager.broadcast_to_room(room_id, json.dumps(message))


#if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=args.port, reload=True)
if __name__ == "__main__":
    import uvicorn
    logging.info("Starting Super Server")
    uvicorn.run(app, host="0.0.0.0", port=8100)

