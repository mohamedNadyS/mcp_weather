class Memory:
    def __init__(self):
        self.history = []
    def add(self, item):
        self.history.append(item)
    def get(self):
        return self.history
    
    def saveFile(self):
        with open("history.log", "w") as f:
            for i in self.history:
                f.write(str(i)+"\n")