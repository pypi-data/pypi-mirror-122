class EndpointNotFound(Exception):
    
    def __init__(self, message, *args):
        super().__init__(message, *args)
