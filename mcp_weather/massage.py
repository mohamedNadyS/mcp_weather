import uuid
from datetime import datetime

class Massage:
    def __init__(self, sender,content,metadata=None):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.sender =sender
        self.content = content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content} (ID: {self.id})"