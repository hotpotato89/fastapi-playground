class BookAlreadyExistsError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserUnactiveError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ServerError(Exception):
    pass
