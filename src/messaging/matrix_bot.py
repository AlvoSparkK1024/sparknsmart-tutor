import asyncio
import os
from nio import AsyncClient, RoomMessageText
from src.orchestration.runtime import Runtime
from src.core.schemas import Message

class MatrixBot:
    def __init__(self):
        self.client = None
        self.room_id = None
        self.runtime = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        self.runtime.bus.subscribe("send_message", self.send_message)
        
        user = os.getenv("MATRIX_USER")
        password = os.getenv("MATRIX_PASSWORD")
        homeserver = os.getenv("MATRIX_HOMESERVER", "https://matrix.org")
        self.room_id = os.getenv("MATRIX_ROOM_ID")

        if user and password and self.room_id:
            self.client = AsyncClient(homeserver, user)
            await self.client.login(password)
            print(f"Logged in to Matrix as {user}")
        else:
            print("Matrix credentials missing. Messaging disabled.")

    async def send_message(self, data: Dict[str, Any]):
        if not self.client or not self.room_id:
            print(f"Mock Send: {data}")
            return

        msg = Message(**data)
        
        # Upload image if present
        content_uri = None
        if msg.image_path and os.path.exists(msg.image_path):
            try:
                resp, _ = await self.client.upload(
                    lambda w, p: w.write(open(msg.image_path, "rb").read()),
                    content_type="image/png",
                    filename="chart.png"
                )
                content_uri = resp.content_uri
            except Exception as e:
                print(f"Failed to upload image: {e}")

        # Send text
        await self.client.room_send(
            room_id=self.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": msg.content
            }
        )
        
        # Send image if uploaded
        if content_uri:
             await self.client.room_send(
                room_id=self.room_id,
                message_type="m.room.message",
                content={
                    "msgtype": "m.image",
                    "body": "Energy Chart",
                    "url": content_uri
                }
            )
