# websocket
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws" , tags=["websockets / live kitchen"])

class connectionmanager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self,websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_new_order(self,order_data: dict):
        for connection in self.active_connections:
            await connection.send_json({
                "event" : "new_order","message" : "new order plz check","data" : order_data
            })

manager = connectionmanager()

@router.websocket("/kitchen")
async def websocket_kitchen_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)