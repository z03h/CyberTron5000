class EmbedError(Exception):
    def __init__(self):
        self.message = "One of the passed in elements is not an embed."
    
    def __str__(self):
        return self.message
