import random



def unmention(user: str) -> str:
    """If a user's name was mentioned with '@', remove it to help make usernames more consisent.
    We don't want to work with usernames with '@' in it.

    Parameters
    ------------
    user : str
        The username we want to remove the '@' from (if applicable)

    Returns
    -------------
    str
        The user param without the '@' at the start. If the '@' is not present, return the user param unchanged.
    """
    return user[1:] if user.startswith('@') else user



def mock(msg: str) -> str:
    """Randomizes the capitalization of each character in a string

    Parameters
    ------------
    msg : str
        The string to mock.

    Returns
    ---------
    str
        msg with random capitalization.
    """
    mocked_msg = ''
    for char in msg:
        if random.choice([True, False]):
            mocked_msg += char.upper()
        else:
            mocked_msg += char.lower()
    return mocked_msg



def makeiter(var):
    """Converts a variable into a list of it's not already an iterable (not including strings.
    If it's already an iterable, don't do anything to it.

    Parameters
    ------------
    var
        the variable to check.

    Returns
    ------------
    var
        an iterable version of the parameter (if it's not already one)
    """
    if not hasattr(var, '__iter__') or isinstance(var, str):
        return [var]
    return var



def check_amount(amount: int or str):
    """Checks to see if the user enters a valid number.
    A valid number is a positive integer > 0.

    Parameters
    -------------
    amount : int or str

    Raises
    ---------
    IncorrectArgument
    """
    try:
        amount = int(amount)
        if amount < 0:
            raise IncorrectArgument(f'Error: {amount} is not a positive integer.')
    except ValueError:
        raise IncorrectArgument(f'Error: {amount} is not a positive integer.')