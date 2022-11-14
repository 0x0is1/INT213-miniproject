from utils.embedGenerator import Embedder

class App:
    def __init__(self, root):
        self.root = root
        self.embedder = Embedder(self.root)

    def initializeUI(self):
        self.embedder.studentPanel()        
