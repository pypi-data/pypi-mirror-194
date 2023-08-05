class IpsumException(Exception):
    """Base exception class for the package Ipsum."""


class ModelNotFinalizedError(IpsumException):
    """Attempted to generate examples from an unfinalized model."""


class ModelAlreadyFinalizedError(IpsumException):
    """Attempted to train an already finalized model."""
