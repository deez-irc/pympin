import configparser
import datetime
import importlib
import pydle
import time
# these are custom modules
from modules import ibip
from modules import log


class Bot(pydle.Client):
    """Smokes your bot class."""
    def __init__(self, nickname, fallback_nicknames, username, realname,
                 owner, admins, auto_joins):
        super().__init__(nickname, fallback_nicknames, username, realname)
        self.owner = owner
        self.admins = admins
        self.auto_joins = auto_joins
        self.real_nick = nickname
        self.timestamp = 0
        self.triggered = 0

    async def eval(self, target, source, message):
        """Evaluate some Python code. Quite useful for debugging."""
        if source not in self.admins:
            return  # admin only command

        expression = ' '.join(message[1:])

        try:
            await self.message(
                target,
                str(eval(expression))
            )

        except SyntaxError as e:
            await self.message(
                target,
                f"{source}: SyntaxError: {e}"
            )

        return

    async def module_reload(self, target, source, message):
        """Attempt to reload a module."""
        if source not in self.admins:
            return

        try:
            importlib.reload(globals()[message[1]])
            await self.message(
                target,
                f"{source}: Module '{message[1]}' was reloaded."
            )

        except KeyError as e:
            await self.message(
                target,
                f"{source}: KeyError: {e}"
            )

        except NameError as e:
            await self.message(
                target,
                f"{source}: NameError: {e}"
            )

        except TypeError as e:
            await self.message(
                target,
                f"{source}: TypeError: {e}"
            )

        return

    async def on_connect(self):
        """This code gets executed on successful connection to the server."""
        self.timestamp = int(time.time())
        for channel in self.auto_joins:
            await self.join(channel)
        return

    async def on_invite(self, channel, by):
        await self.notice(
            by,
            f"If you would like me to join {channel}, "
            f"please contact {self.owner}."
        )
        return

    async def on_join(self, channel, user):
        if user == self.owner:
            await self.set_mode(channel, 'o', user)
        return

    async def on_kick(self, channel, target, by, reason):
        await self.join(channel)
        time.sleep(1)

        if self.in_channel(channel) is True:
            return

        else:
            await self.notice(
                self.owner,
                f"{by} banned me from {channel} [{reason}]"
            )

    async def on_message(self, target, source, message):
        """Parse incoming messages for commands and whatnot."""
        log.log(
            self.network,
            target,
            source,
            message
        )
        message = message.split()

        if source == self.nickname:
            return

        if message[0].startswith('.'):
            # flood protection
            check = log.check_rate(self.network, target, source)
            if check[0] <= 3:
                pass

            if check[0] == 4:
                await self.notice(
                    source,
                    "You can only send 3 commands every 30 seconds. " +
                    "Your commands will be ignored for " +
                    f"{30 - (int(time.time()) - check[1])} more seconds, " +
                    "provided you don't continue to spam lines that start " +
                    "with a dot."
                )
                return

            if check[0] > 4:
                return

        if message[0].startswith('.bots'):
            # comply with IRC Bot Identification Protocol
            await ibip.reply(self, target, source)

        elif message[0].startswith('.eval'):
            # evaluate Python expressions, useful for debugging
            await self.eval(target, source, message)

        elif message[0].startswith('.join'):
            # join a channel or channels
            if source != self.owner:
                return
            else:
                await self.join(message[1])

        elif message[0].startswith('.quit'):
            # quit IRC and exit the program
            if source in self.admins:
                await self.quit()

        elif message[0].startswith('.reload'):
            # attempt to reload a Python module
            await self.module_reload(target, source, message)

        elif message[0].startswith('.report'):
            # prepare a report on current channel/user (owner only for now)
            if source != self.owner:
                return

            try:
                if message[1] and message[1] in self.channels[target]['users']:
                    bytes_logged = log.bytes_logged(
                        self.network,
                        target,
                        source,
                        message[1]
                    )
                    await self.message(
                        target,
                        f"{source}: {message[1]} has sent a total of " +
                        f"{bytes_logged} bytes to {target}."
                    )

            except IndexError:
                bytes_logged = log.bytes_logged(
                    self.network,
                    target,
                    source
                )
                await self.message(
                    target,
                    f"{source}: I have logged {bytes_logged} bytes " +
                    f"of messages on {target}."
                )

        elif message[0].startswith('.uptime'):
            # display uptime
            await self.message(
                target,
                f"{source}: My current uptime is: {self.uptime()}"
            )

        return

    async def on_nick_change(self, old, new):
        if old == self.real_nick:
            await self.set_nickname(self.real_nick)
        return

    async def on_quit(self, user, message=None):
        """Get your nick back when your ghost quits."""
        if user == self.real_nick:
            await self.set_nickname(self.real_nick)
        return

    def uptime(self):
        """Calculate time elapsed since connecting to the server."""
        return datetime.timedelta(seconds=int(time.time()) - self.timestamp)


parser = configparser.ConfigParser()
parser.read('config.ini')
client = Bot(
    parser.get('Settings', 'nickname'),
    parser.get('Settings', 'fallback_nicknames').split(),
    parser.get('Settings', 'username'),
    parser.get('Settings', 'realname'),
    parser.get('Settings', 'owner'),
    parser.get('Settings', 'admins').split(),
    parser.get('Settings', 'auto_joins').split()
)

client.run(parser.get('Settings', 'server'))
client.handle_forever()
