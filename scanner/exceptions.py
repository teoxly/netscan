class ScanError(Exception):
    pass


class InvalidTargetError(ScanError):
    pass


class ScanTimeoutError(ScanError):
    pass


class ScanExecutionError(ScanError):
    pass