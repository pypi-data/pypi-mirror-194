from pyrogram import filters, Client
from config import CMD_HNDLR as cmds
from geezlibs import DEVS

def geez(command: str, prefixes: cmds):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper

def devs(command: str):
    def wrapper(func):
        @Client.on_message(filters.command(command, "*") & filters.user(DEVS))
        def wrapped_func(client, message):
            return func(client, message)

        return wrapped_func

    return wrapper

from geezlibs.geez.autobot import *