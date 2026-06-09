class BookAlreadyExistsError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class ServerError(Exception):
    pass
