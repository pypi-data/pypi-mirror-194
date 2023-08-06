class YumError(Exception):
    def __init__(self, code: int = 500, reason: str = "Unknown error") -> None:
        super(YumError, self).__init__()
        self.code = code
        self.reason = reason


class YumUnavailable(YumError):
    def __init__(self, reason: str = "Service Unavailable") -> None:
        super(YumUnavailable, self).__init__(503, reason)


class YumNotImplemented(YumError):
    def __init__(self, reason: str = "Not Implemented") -> None:
        super(YumNotImplemented, self).__init__(501, reason)


class YumTimeout(YumError):
    def __init__(self, reason: str = "Time out") -> None:
        super(YumTimeout, self).__init__(504, reason)


class YumBadRequest(YumError):
    def __init__(self, reason: str = "not found") -> None:
        super(YumBadRequest, self).__init__(400, reason)


class YumNotFound(YumError):
    def __init__(self, reason: str = "not found") -> None:
        super(YumNotFound, self).__init__(404, reason)
