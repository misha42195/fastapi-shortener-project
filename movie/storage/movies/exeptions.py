class MoviesBaseError(Exception):
    """
    Base exception class for movie-related errors.
    """


class MovieAlreadyExistsError(MoviesBaseError):
    """
    Raised when attempting to create a movie that already exists.
    """
