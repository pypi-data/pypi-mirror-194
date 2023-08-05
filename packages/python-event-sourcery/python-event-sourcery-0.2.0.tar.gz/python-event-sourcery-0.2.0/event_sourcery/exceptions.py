class EventStoreException(Exception):
    pass


class NoEventsToAppend(EventStoreException):
    pass


class ConcurrentStreamWriteError(EventStoreException):
    pass


class Misconfiguration(EventStoreException):
    pass


class VersioningMismatch(EventStoreException):
    pass


class EitherStreamIdOrStreamNameIsRequired(EventStoreException):
    pass


class AnotherStreamWithThisNameButOtherIdExists(EventStoreException):
    pass


class ExpectedVersionUsedOnVersionlessStream(VersioningMismatch):
    pass


class NoExpectedVersionGivenOnVersionedStream(VersioningMismatch):
    pass
