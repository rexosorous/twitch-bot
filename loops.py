# python standard libraries
import asyncio

# local modules
import games



class Points:
    """Adds points to all users in the chat.

    Parameters
    ------------
    bot : TwitchPy.TwitchBot.Client
    db : database.Handler

    Attributes
    -----------
    interval : int
        how long to wait before adding points again.
    """
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.interval = 15

    async def loop(self):
        for user in self.bot.API.get_viewers():
            info = self.db.get_user_info(user)
            self.db.edit_user(user, 'points', '+', info['income'])
        await asyncio.sleep(self.intervale)






class Games:
    """Games that spawn randomly in which the user can participate in.

    Current Games:
        Mystery Box
        Lottery

    Parameters
    ------------
    bot : TwitchPy.TwitchBot.Client
    db : database.Handler
    """
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.box = games.MysteryBox(self.bot, self.db)
        self.lotto = games.Lottery(self.bot, self.db)



    async def loop(self):
        """Chooses which game to spawn.
        """
        pass