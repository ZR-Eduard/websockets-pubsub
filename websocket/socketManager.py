from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    def __init__(self):
        """
        Initializes the WebSocketManager.

        Attributes:
            rooms (dict): A dictionary to store WebSocket connections in different rooms.
        """
        self.rooms: dict = {}

    async def add_user_to_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Adds a user's WebSocket connection to a room.

        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        await websocket.accept()

        if room_id not in self.rooms:
            self.rooms[room_id] = []
        
        self.rooms[room_id].append(websocket)
        print(f"Added user to room {room_id}")

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        """
        Broadcasts a message to all connected WebSockets in a room.

        Args:
            room_id (str): Room ID or channel name.
            message (str): Message to be broadcasted.
        """
        if room_id in self.rooms:
            for socket in list(self.rooms[room_id]):  # Convert to list to avoid modification during iteration
                try:
                    await socket.send_text(message)
                except WebSocketDisconnect:
                    # Handle the disconnection, e.g., remove the socket from the room
                    self.rooms[room_id].remove(socket)
                    print(f"Removed disconnected socket from room {room_id}")
        else:
            print(f"Room {room_id} not found")

    async def broadcast_to_all_directly(self, message: str) -> None:
        """
        Broadcasts a message directly to all connected WebSocket clients across all rooms.

        Args:
            message (str): Message to be broadcasted.
        """
        for room_id, sockets in self.rooms.items():
            await self.broadcast_to_room(room_id, message)

    async def remove_user_from_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Removes a user's WebSocket connection from a room.

        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        if room_id in self.rooms and websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
            print(f"Removed user from room {room_id}")
            if len(self.rooms[room_id]) == 0:
                del self.rooms[room_id]
                print(f"Deleted empty room {room_id}")
