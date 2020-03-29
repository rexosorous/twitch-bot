class InsufficientFunds(Exception):
    """
    Raised when a user tries to use more points than they have.
    """
    pass



class IncorrectArgument(Exception):
    """
    Raised when a user tries to use a command with incorrect arguments.
    Like if we expect an int, but they send a name.
    """
    pass