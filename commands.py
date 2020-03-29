# python standard libraries
import random

# dependencies
from TwitchPy import Commands

# local modules
from errors import *
import utilities as util



class Basic(Commands.Cog):
    """Simple commands

    Parameters
    ------------
    bot : TwitchPy.TwitchBot.Client
        Allows us to access kill command, IRC, and API
    """
    def __init__(self, bot):
        super().__init__(prefix='!')
        self.bot = bot



    @Commands.create(name='mock')
    async def mock_user(self, ctx, username):
        """Takes a user's last message and mocks it by randomizing the capitalization of each letter.

        Parameters
        -------------
        username : str
        """
        username = util.unmention(username)
        for chat in self.bot.IRC.chat_history:
            if chat.user.name.lower() == username.lower():
                await self.bot.IRC.send(util.mock(chat.msg))
                return



    @Commands.create(name='mock')
    async def mock_msg(self, ctx, *args):
        """Randomizes the capitalization of a message.

        Paramaters
        ------------
        *args : [str]
            The full message to mock.
        """
        mocked_msg = ''
        msg = ' '.join(args)
        await self.bot.IRC.send(util.mock(msg))



    @Commands.create(name=['kill', 'stop', 'exit'], permission='broadcaster')
    async def kill(self, ctx):
        """Kills the bot gracefully.
        """
        await bot.kill()









class CopyPasta(Commands.Cog):
    """Commands that send the same message no matter what.
    """
    def __init__(self, IRC):
        super().__init__(prefix='!')
        self.IRC = IRC



    @Commands.create(name=['emotes', 'emoteslist', 'bttvemotes'])
    async def emotes(self, ctx):
        await self.IRC.send('EZ  Clap  HYPERCLAP  SPANK  SPANKED  FeelsGoldMan')



    @Commands.create()
    async def weather(self, ctx):
        await self.IRC.send('Interesting. The weather patterns here seem natural and not artificial. I wonder if the rings\' environment systems are malfunctioning. Or if the designers wanted the installation to have inclement weather.')









class Points(Commands.Cog):
    def __init__(self, bot, db):
        super().__init__(prefix='!')
        self.bot = bot
        self.db = db



####################################################################################################
########################################## CHECK COMMANDS ##########################################
####################################################################################################



    @Commands.create(name=['points', 'checkpoints'])
    async def check_own_points(self, ctx):
        """Checks how many points the author has.
        """
        points = self.db.get_user_info(ctx.author.name)['points']
        await self.bot.IRC.send(f'@{ctx.author.name} has {points:,} points.')



    @Commands.create(name=['points', 'checkpoints'])
    async def check_others_points(self, ctx, user):
        """Checks how many points another user has.

        Parameters
        ------------
        user : str
        """
        user = util.unmention(user)
        points = self.db.get_user_info(user)['points']
        await self.bot.IRC.send(f'@{user} has {points:,} points.')



    @Commands.create(name=['income', 'pay', 'wage', 'salary', 'checkincome', 'checkpay', 'checkwage', 'checksalary']):
    async def check_own_income(self, ctx):
        """Checks how many points a user gains per cycle
        """
        income = self.db.get_user_info(ctx.author.name)['income']
        await self.bot.IRC.send(f'@{ctx.author.name} has {income:,} income.')



    @Commands.create(name=['income', 'pay', 'wage', 'checkincome', 'checkpay', 'checkwage']):
    async def check_others_income(self, ctx, user):
        """Checks how many points another user gains per cycle

        Parameters
        ----------
        user: str
        """
        user = util.unmention(user)
        income = self.db.get_user_info(user)['income']
        await self.bot.IRC.send(f'@{user} has {income:,} income.')



    @Commands.create(name=['luck', 'checkluck']):
    async def check_own_luck(self, ctx):
        """Checks how much luck a user has.
        """
        luck = self.db.get_user_info(ctx.author.name)['luck']
        await self.bot.IRC.send(f'@{ctx.author.name} has {luck} luck.')



    @Commands.create(name=['luck', 'checkluck']):
    async def check_others_luck(self, ctx, user):
        """Checks how much luck another user has.

        Parameters
        ----------
        user: str
        """
        user = util.unmention(user)
        luck = self.db.get_user_info(user)['luck']
        await self.bot.IRC.send(f'@{user} has {luck} luck.')



####################################################################################################
########################################## EDIT COMMANDS ###########################################
####################################################################################################



    @Commands.create(name=['points', 'changepoints', 'editpoints'], permission='moderator')
    async def edit_points(self, ctx, user, operator, amount):
        """Changes how many points a user has.

        Parameters
        ------------
        user : str
        operator : {'+', '-', '*', '/', 'set'}
        amount : str
            The number to add / sub / etc.
            This will be converted to int in database.Handler
        """
        try:
            user = util.unmention(user)
            new_points = self.db.edit_user(user, 'points', operator, amount)
            await self.bot.IRC.send(f'@{user} now has {new_points:,} points.')
        except IncorrectArgument as e:
            await self.bot.IRC.send(e)



    @Commands.create(name=['income', 'changeincome', 'editincome'], permission='moderator')
    async def edit_income(self, ctx, user, operator, amount):
        """Changes how much a user gains per cycle.

        Parameters
        -------------
        user : str
        operator : {'+', '-', '*', '/', 'set'}
        amount : str
            This will be converted to int in database.Handler
        """
        try:
            user = util.unmention(user)
            new_income = self.db.edit_user(user, 'income', operator, amount)
            await self.bot.IRC.send(f'@{user} now has {new_income:,} income.')
        except IncorrectArgument as e:
            await self.bot.IRC.send(e)



    @Commands.create(name=['luck', 'changeluck', 'editluck'], permission='moderator')
    async def edit_luck(self, ctx, user, operator, amount):
        """Changes how much a user gains per cycle.

        Parameters
        -------------
        user : str
        operator : {'+', '-', '*', '/', 'set'}
        amount : str
            This will be converted to int in database.Handler
        """
        try:
            user = util.unmention(user)
            new_luck = self.db.edit_user(user, 'luck', operator, amount)
            await self.bot.IRC.send(f'@{user} now has {new_luck} luck.')
        except IncorrectArgument as e:
            await self.bot.IRC.send(e)



####################################################################################################
########################################## OTHER COMMANDS ##########################################
####################################################################################################



    @Commands.create(name=['givepoints', 'donatepoints', 'transferpoints'])
    async def give_points(self, ctx, user, amount):
        """Allows one user to give their points to another user.

        Parameters
        ------------
        user : str
        amount : str
            This will be converted to int in database.Handler
        """
        donor = ctx.author.name
        receiver = util.unmention(user)

        try:
            donor_points, receiver_points = self.db.transfer_points(donor, receiver, amount)
            await self.bot.IRC.send(f'{donor} gives {receiver} {amount:,} points. How charitable!')
            await self.bot.IRC.send(f'@{donor} now has {donor_points:,} points.')
            await self.bot.IRC.send(f'@{receiver} now has {receiver_points:,} points.')
        except InsufficientFunds as msg:
            await self.bot.IRC.send(msg)



    @Commands.create(name='gamble')
    async def gamble(self, ctx, amount):
        """Rolls a number and based on the result, either takes or gives points to the user.

        Rolls a number between the user's luck and 100.
        So a higher luck value essentially means they have a higher chance to win.
        Result Table:
            100     : The user gets back double what they bet and gains 5 income.
            51-99   : The user gets back double what they bet.
            50      : The user gets back what they bet. (net neutral)
            1-49    : The user loses what they bet.
            <0      : The user loses twice what they bet.

        Parameters
        -----------
        amount : str
            This will be converted to int in database.Handler
        """
        # input sanitization
        try:
            util.check_amount(amount)
            self.db.check_funds(ctx.author.name, amount)
        except (IncorrectArgument, InsufficientFunds) as e:
            await self.bot.IRC.send(e)
            return

        luck = self.db.get_user_info(ctx.author.name)['luck']
        roll = random.randint(luck, 100)
        self.db.edit_user(ctx.author.name, 'points', '-', amount)

        if roll = 100:
            new_balance = self.db.edit_user(ctx.author.name, 'points', '+', int(amount)*2)
            new_income = self.db.edit_user(ctx.author.name, 'income', '+', '5')
            await self.bot.IRC.send(f'@{ctx.author.name} rolled a {roll}! You win {amount:,} points and 5 more income! You now have {new_balance:,} points and {new_income} income.')
        if roll > 50:
            new_balance = self.db.edit_user(ctx.author.name, 'points', '+', int(amount)*2)
            await self.bot.IRC.send(f'@{ctx.author.name} rolled a {roll} and has won {amount:,} points! You now have {new_balance:,} points.')
        elif roll == 50:
            new_balance = self.db.edit_user(ctx.author.name, 'points', '+', amount)
            await self.bot.IRC.send(f'@{ctx.author.name} rolled a {roll} and has neither won nor lost any points.')
        elif roll > 0:
            new_balance = self.db.edit_user(ctx.author.name, 'points', '-', amount)
            await self.bot.IRC.send(f'@{ctx.author.name} rolled a {roll} and has lost {amount:,} points! You now have {new_balance:,} points.')
        else:
            new_balance = self.db.edit_user(ctx.author.name, 'points', '-', int(amount)*2)
            await self.bot.IRC.send(f'@{ctx.author.name} rolled a {roll} and has lost {amount:,} points! You now have {new_balance:,} points.' )