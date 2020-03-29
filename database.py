# python standard libraries
import sqlite3

# local modules
from errors import *
import utilities as util



class Handler:
    """Handles all database interactions
    """
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.sql = self.conn.cursor()



    def _create_table(self):
        """Creates the users table.
        SHOULD NOT BE USED.
        Here only for reference
        """
        self.sql.execute('''CREATE TABLE users (name TEXT, points INTEGER, income INTEGER, luck INTEGER)''')
        self.conn.commit()



    def init_users(viewers: str or [str]):
        """Adds users into the database if they're not already in there.

        Parameters
        ------------
        users : str or [str]
            A list of all the viewers to add into the database (if applicable)
        """
        viewers = util.makeiter(viewers)
        db_users = self.sql.execute('''SELECT name FROM users''').fetchall()    # [('name1',), ('name2',), ('name3')]
        for user in viewers['broadcaster'] + viewers['moderators'] + viewers['viewers']:
            if user not in db_users:
                starting_points = 500
                starting_income = 10
                starting_luck = 0
                self.sql.execute('''INSERT INTO users VALUES (?, ?, ?, ?)''', (user, starting_points, starting_income, starting_luck))
        self.conn.commit()



    def get_user_info(user: str) -> dict:
        """Gets all the info about a user (the row in the database)

        Parameters
        ------------
        user : str

        Returns
        ---------
        dict
            Keys are database column names.
        """
        self.init_users(user)
        info = self.sql.execute('''SELECT * FROM users WHERE name=?''', (user, )).fetchone()
        user_info = {
            'name': info[0],
            'points': info[1],
            'income': info[2],
            'luck': info[3]
        }
        return user_info



    def check_funds(user: str, amount: int):
        """Makes sure a user has enough points to do what they want.

        Parameters
        ------------
        user : str
        amount : int

        Raises
        -------
        InsufficientFunds
        """
        info = self.get_user_info(user)
        if info['points'] < amount:
            raise InsufficientFunds(f'@{user} has insufficient funds. {user} is short {amount - info["points"]} points.')



    def edit_user(user: str, field: str, operator: str, amount: int or str) -> int:
        """Edits a user's points, income, or luck

        Parameters
        ------------
        user : str
        field : {'points', 'income', 'luck'}
        operator : {'+', '-', '*', '/', 'set'}
        amount : int or str
            The amount to add, subtract, set, etc. to the field. This is a string because we'll likely get this
            as a string from twitch chat anyway

        Returns
        ---------
        int
            User's point balance after editing.

        Raises
        ---------
        IncorrectArgument
            Raised when the user sends an incorrect argument.
            Ex: If amount is not a number of if operator isn't one of the above.
        """
        self.init_users(user)

        # sanitize inputs
        if field not in ['points', 'income', 'luck']:
            raise IncorrectArgument(f'{field} is not a recognized argument for this command.')
        if operator not in ['+', '-', '*', '/', 'set']:
            raise IncorrectArgument(f'{operator} is not a recognized argument for this command.')
        if not amount.isdigit():
            raise IncorrectArgument(f'{amount} is not a number.')

        if operator == 'set':
            new_amount = int(amount)
        else:
            current_amount = self.sql.execute(f'''SELECT {field} FROM users WHERE name=?''', (user, )).fetchone()[0]
            expression = f'{current_amount} {opreator} {amount}'
            new_amount = int(eval(expression))

        self.sql.execute(f'''UPDATE users SET {field}=? WHERE name=?''', (new_amount, user))
        self.conn.commit()

        return new_amount



    def transfer_points(donor: str, recipient: str, amount: int or str) -> int, int:
        """Transfers points from one user to another

        Parameters
        ------------
        donor : str
        recipient : str
        amount : int or str

        Returns
        ---------
        int, int
            The new points balance of both donor and recipient respectively.
        """
        self.init_users([donor, recipient])
        amount = int(amount)

        self.check_funds(donor, amount)
        donor_balance = self.edit_user(donor, 'points', '-', amount)
        recipient_balance = self.edit_user(recipient, 'points', '+', amount)
        return donor_balance, recipient_balance



    def close(self):
        """Gracefully closes sqlite3 connection
        """
        self.conn.close()