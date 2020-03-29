# python standard libraries
import random

# local modules
from errors import *
import utilities as util



class MysteryBox:
    """A game in which users can bid on a box whose contents are a mystery.

    The box can contain points, income, or luck.

    Parameters
    ------------
    bot : TwitchPy.TwitchBot.Client
    db : database.Handler

    Attributes
    -----------
    See Parameters.

    active : bool
        Whether or not the game is active

    contents : (str, int)
        A tuple whose first element is the type of reward (points or luck)
        and whose second element is the quantity of that type.

    top_bidder : (str, int)
        A tuple whose first element is the user with the highest bid
        and whose second element is the bid amount
    """
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.active = False
        self.contents = tuple()
        self.top_bidder = tuple()



    def init_box(self):
        """Fills the contents of the box with either points, income, or luck.

        Breakdown of the chances of what can be in the box.
        85% chance to spawn points
            The point distribution is between 0 and 700 points following this piece-wise function:
                if 0 <= x <= 100 :  ((x - 50)^3)/5 + 1000
                if x > 100 :        500(x - 100) + 2000
            Basically there's an x^3 distribution between a roll of 0 and 100, and if the roll
            is between 100 and 10, we consider it a critical hit and put extra points in the box.
        10% chance to spawn income
            The income distribution is between 1 and 10 points, linearly.
        5%  chance to spawn luck
            The luck distribution is between 1 and 5, linearly.
        """
        possible_types = ['points'] * 85 + ['income'] * 10 + ['luck'] * 5
        type_ = random.choice(possible_types)

        if type_ == 'points':
            # see formula above
            amount = random.randint(0, 110)
            amount -= 50
            amount = pow(amount, 3)
            amount /= 5
            amount += 1000
            amount = int(amount)
        elif type_ == 'income':
            amount = random.randint(1, 10)
        elif type_ == 'luck':
            amount = random.randint(1, 5)

        self.contents = (type_, amount)



    async def spawn(self):
        """Spawns the box and periodically informs the users how much time is left.

        This game is active only as long as this function is running.
        """
        # create the box
        self.active = True
        self.init_box()

        # timer
        await self.bot.IRC.send('A Mystery Box has appeared! Use "!bid <amount>" to place your bids! A winner will be decided in 1 minute.')
        await asyncio.sleep(30)
        await self.bot.IRC.send('30 seconds left to bid on the Mystery Box.')
        await asyncio.sleep(20)
        await self.bot.IRC.send('Only 10 seconds left to bid on the Mystery Box!')
        await asyncio.sleep(10)

        # award and declare winner
        new_value = self.db.edit_user(self.top_bidder[0], self.contents[0], '+', self.contents[1])
        await self.bot.IRC.send(f'@{self.top_bidder[0]} wins the Mystery Box which contained {self.contents[1]} {self.contents[0]}! You now have {new_value} {self.contents[0]}!')

        # reset attributes
        self.active = False
        self.contents = tuple()
        self.top_bidder = tuple()



    async def bid(self, user: str, amount: int or str):
        """Places a bid on the box.

        Holds onto the bid amount so the user can't gamble away their money, resulting
        in them having insufficient funds to actually buy the box.

        Parameters
        ------------
        user : str
        amount : int or str
        """
        # input sanitization
        try:
            util.check_amount(amount)
            self.db.check_funds(user, amount)
        except (IncorrectArgument, InsufficientFunds) as e:
            await self.bot.IRC.send(e)
            return

        # check if this game is even active
        if not self.active:
            await self.bot.IRC.send(f'There is no Mystery Box to bid on.')
            return

        # check if the bid is high enough
        amount = int(amount)
        if amount <= top_bidder[1]:
            await self.bot.IRC.send(f'That is not a high enough bid, @{user}. You must bid higher than {self.top_bidder[1]} points.')
            return

        # place the bid
        # return points back to the old top bidder
        if self.top_bidder:
            self.db.edit_user(self.top_bidder[0], 'points', '+', self.top_bidder[1])

        # take points from the new top bidder
        self.db.edit_user(user, 'points', '-', amount)

        # set the new top bidder
        self.top_bidder = (user, amount)
        await self.bot.IRC.send(f'@{user} is the new top bidder with {amount} points!')