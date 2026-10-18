class StreamStatsError(Exception):
    pass

class InvalidFormatError(StreamStatsError):
    pass

class InvalidEventError(StreamStatsError):
    pass

class InvalidTimestampError(InvalidEventError):
    pass
