class GasEstimationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = -32000
        self.message = message
