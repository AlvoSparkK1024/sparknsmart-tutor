from typing import Dict, Any, Optional

class Memory:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def clear(self):
        self._store.clear()

    def dump(self) -> Dict[str, Any]:
        return self._store.copy()
