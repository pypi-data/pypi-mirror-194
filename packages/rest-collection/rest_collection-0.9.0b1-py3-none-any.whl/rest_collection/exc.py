
class RestCollectionError(Exception):
    """Root exception."""


class RestCollectionReferenceError(RestCollectionError, ReferenceError):
    """Error of empty weakref value."""
