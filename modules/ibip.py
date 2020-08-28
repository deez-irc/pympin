"""ibip.py - comply with IRC Bot Identification Protocol"""

import sys

__author__ = 'deez@based.red'
__version__ = '1.0'
__license__ = 'GPLv3'


async def reply(bot, target, source):
    await bot.message(
        target,
        f"Reporting in! [Python] Hello, {source}! " +
        f"My current uptime is: {bot.uptime()}"
    )
