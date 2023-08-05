class ReleaseException(Exception):
    """Base release exception."""

    def __init__(self, msg):
        self.msg = msg


class ActiveBranchNotMainException(ReleaseException):
    """Raises when working on a non-main branch."""


class DirtyTreeException(ReleaseException):
    """Raises when tree is dirty."""
