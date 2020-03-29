# python standard libraries
import json

# dependencies
from TwitchPy import TwitchBot

# local modules
import commands
import database
import loops



'''TO DO
    * when someone does a command like '!mock @monipoop', check whether that user exists in API or check if they're in chat?
      before automatically adding them to the database to avoid issues where the database is filled with 'phantom' users which
      are all typos.

    * commands still needed to add:
        help

        redeem: spending points for stuff to happen

        eventlist
        spawnevent

        mystery points box
            bid
            topbid

        lottery
            checklotto
            buytix
            checktix
'''



if __name__ == '__main__':
    with open('login_info.json', 'r') as file:
        login = json.load(file)

    bot = TwitchBot.Client(**login)

    db = database.Handler()

    basic = commands.Basic(bot)
    copypasta = commands.CopyPasta(bot.get_IRC())
    points = commands.Points(bot, db)

    bot.add_cogs([basic, copypasta, points])

    try:
        bot.run()
    finally:
        db.close()