import asyncio
from typing import Callable, Dict, List, Any

class MessageBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    async def publish(self, topic: str, message: Any):
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(message)
                else:
                    callback(message)
