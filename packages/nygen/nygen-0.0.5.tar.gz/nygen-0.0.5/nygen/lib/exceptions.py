class GenException(Exception):
    pass


class BadProjName(GenException):
    pass


class DestinationExistsException(GenException):
    pass


class CondaEnvironmentExistsException(GenException):
    pass


class MissingArgumentException(GenException):
    pass


class CondaException(GenException):
    pass
