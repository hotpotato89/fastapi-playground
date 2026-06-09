class BookAlreadyExistsError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class ServerError(Exception):
    pass
