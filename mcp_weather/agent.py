class Agent():
    def __init__(self, name="Agent"):
        self.name = name
    def respond(self,context):
        last= context[-1].content if context else ""
        return f"Echo: '{last}'understood"