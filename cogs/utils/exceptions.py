class EmbedError(Exception):
    def __init__(self):
        self.message = "Error! You passed incorrect embed arguments!"
    
    def __str__(self):
        return self.message
