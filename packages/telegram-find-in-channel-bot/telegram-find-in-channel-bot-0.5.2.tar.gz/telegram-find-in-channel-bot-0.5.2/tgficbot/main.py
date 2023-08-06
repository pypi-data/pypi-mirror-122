from telethon import TelegramClient
from telethon.events import NewMessage, CallbackQuery, MessageEdited
from telethon.events import StopPropagation
from telethon.tl import types, functions
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import ChannelPrivateError

import os
import signal
from pathlib import Path
import logging
import asyncio
import hashlib
import argparse
import configparser
from typing import List

from . import states
from .db import Database
from . import i18n
from . import constants

argp = argparse.ArgumentParser(description='Start Telegram FindInChannelBot.')
argp.add_argument('--config',
                  type=str,
                  default=os.path.expanduser('~/.config/tgficbot.cfg'),
                  help='specify config file')
argp.add_argument('--dbpath',
                  type=str,
                  default=os.path.expanduser('~/.cache/'),
                  help='specify directory to store databases')
args = argp.parse_args()

db = Database(Path(args.dbpath) / 'tgficbot.db')
onstate = states.StateHandler(db)
withi18n = i18n.I18nHandler(db)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

config = configparser.ConfigParser()
config.read(args.config)

bot = TelegramClient(
    str(Path(args.dbpath) / 'bot.session'), config['api']['id'],
    config['api']['hash']).start(bot_token=config['bot']['token'])


@bot.on(NewMessage(pattern=r'/start\s*(.*)'))
@withi18n
async def start_command_handler(event: NewMessage.Event, _):
    if not event.is_private:
        return
    chat = await event.get_chat()
    db.save_user(chat)
    db.conn.commit()
    parameter = event.pattern_match.group(1).strip()

    if parameter:
        channel_title = db.start_searching_with_token(chat, parameter)
        if channel_title is None:
            await event.respond(_('This search token is invalid.'))
            return
        await event.respond(
            _('Now type in what you want to find in **{}**, or /cancel to quit.').
            format(channel_title))
        raise StopPropagation
    await event.respond(
        _('Hi! To /find in your channel, you must /add it to this bot first.'))


@bot.on(NewMessage(pattern='/add'))
@onstate(states.Empty)
@withi18n
async def add_command_handler(event, _):
    await event.respond(
        _('To add your channel, do the following:\n'
          '\n'
          '1. Add this bot to your channel as an admin;\n'
          '2. Forward a message from the channel to me.'))
    user = await event.get_chat()
    db.set_user_state(user, states.AddingAChannel)


@bot.on(NewMessage(pattern='/cancel'))
@withi18n
async def cancel_command_handler(event: NewMessage.Event, _):
    user = await event.get_chat()
    current_state = db.get_user_state(user)
    if current_state == states.Empty:
        return
    db.clear_user_state(user)
    db.set_user_selected(user.id, None)
    await event.respond(_('Aborted.'))


@bot.on(NewMessage())
@onstate(states.AddingAChannel)
@withi18n
async def adding_forward_handler(event: NewMessage.Event, _):
    user = await event.get_chat()

    if event.message.fwd_from is None:
        await event.respond(
            _('Please forward any message from your channel to me, '
              'or /cancel to abort.'))
        return
    if event.message.fwd_from.channel_post is None:
        await event.respond(_('Please forward from a channel.'))
        return

    await event.respond(_('Getting channel infos...'))
    try:
        channel = await bot.get_entity(event.message.fwd_from.from_id)
    except ChannelPrivateError:
        await event.respond(
            _('Please add this bot to your channel before you forward me channel messages.'
              ))
        return

    if channel.admin_rights is None:
        await event.respond(
            _('Please add this bot to your channel before you forward me channel messages.'
              ))
        return
    if db.check_channel_saved(channel):
        await event.respond(_('Channel already added. Abort.'))
        db.clear_user_state(user)
        return

    db.save_channel(channel)
    async for admin in bot.iter_participants(
            channel, filter=types.ChannelParticipantsAdmins):
        db.save_channel_admin_relation(channel.id, admin)

    full_channel = await bot(
        functions.channels.GetFullChannelRequest(channel=channel))
    await event.respond(_('Obtaining previous messages...'))
    for i in range(full_channel.full_chat.read_inbox_max_id):
        message = await bot.get_messages(channel, ids=i)
        db.save_message(message)

    db.conn.commit()
    await event.respond(_('Add finished.'))
    db.clear_user_state(user)


def three_buttons_each_line(buttons: List[Button]) -> List[List[Button]]:
    res = []
    for i in range(0, len(buttons), 3):
        res.append(buttons[i:i + 3])
    return res


def channel_id2button(channel_id: int):
    channel_title = db.get_channel_title(channel_id)
    data = constants.CQ.SelectAChannel.format(channel_id=channel_id)
    return Button.inline(channel_title, data=data)


async def channel_picker(event: NewMessage.Event, user: types.User, message: str, _) -> bool:
    """False: no channel added"""
    user_owned_channel_ids = db.get_user_owned_channels(user)
    if len(user_owned_channel_ids) == 0:
        await event.respond(
            _("You haven't had any channel added to this bot. Please /add a channel first."
              ))
        return False
    buttons = list(map(channel_id2button, user_owned_channel_ids))
    buttons = three_buttons_each_line(buttons)
    await event.respond(message, buttons=buttons)
    return True


@bot.on(NewMessage(pattern=r'/find'))
@onstate(states.Empty)
@withi18n
async def find_command_handler(event: NewMessage.Event, _):
    """Finding interactively"""
    if not event.is_private:
        await event.respond(_('This command can only be used in private chat.')
                            )
        return

    user = await event.get_chat()
    message_text = _('Select a channel to search:')
    if await channel_picker(event, user, message_text, _):
        db.set_user_state(user, states.SelectingAChannelToFind)


async def not_admin_message(event, user, _):
    await event.respond(
        _("Sorry, you don't have the permission to access this channel."))
    db.clear_user_state(user)


@bot.on(CallbackQuery())
@onstate(states.SelectingAChannelToFind)
@withi18n
async def select_channel_to_find_handler(event: CallbackQuery.Event, _):
    user = await event.get_chat()
    data = event.data.decode()
    if not data.startswith(constants.CQ.SelectAChannelPrefix):
        return
    channel_id = int(data.split(':')[1])

    if not db.is_channel_admin(user, channel_id):
        not_admin_message(event, user, _)
        return

    channel_title = db.get_channel_title(channel_id)
    db.set_user_state(user, states.FindingInAChannel)
    db.set_user_selected(user.id, channel_id)
    await event.respond(
        _('Now type in what you want to find in **{}**, or /cancel to quit.').
        format(channel_title))


def get_showmore_buttons(search: str, start: int, total: int):
    """start: begin with 0
    """
    digest = hashlib.md5(search.encode()).hexdigest()
    previous_start = max((start - constants.MessagesEachSearch), 0)
    next_start = min((start + constants.MessagesEachSearch), total)
    # print(previous_start, next_start)
    fsm = constants.CQ.FindShowMore
    button_left = Button.inline('⇦',
                                data=fsm.format(digest=digest,
                                                start=previous_start))
    button_right = Button.inline('⇨',
                                 data=fsm.format(digest=digest,
                                                 start=next_start))
    button_shown = Button.inline(
        f'{start + constants.MessagesEachSearch} / {total}')
    # MessagesEachSearch/total ⇨
    if start == 0:
        return [button_shown, button_right]
    # ⇦ total/total
    if start + constants.MessagesEachSearch >= total:
        button_shown = Button.inline(f'{total} / {total}')
        return [button_left, button_shown]
    # ⇦ start+MessagesEachSearch/total ⇨
    return [button_left, button_shown, button_right]


@bot.on(NewMessage())
@onstate(states.FindingInAChannel)
@withi18n
async def finding_handler(event: NewMessage.Event, _):
    user = await event.get_chat()
    channel_id = db.get_user_selected(user.id)
    pattern = event.raw_text

    found_message_ids = db.find_in_messages(channel_id, pattern)
    if len(found_message_ids) == 0:
        await event.respond(_('No results.'))
        return
    if len(found_message_ids) <= constants.MessagesEachSearch:
        for message_id in found_message_ids:
            await bot.forward_messages(user, message_id, channel_id)
        return

    # If there are too many matches to be shown on once
    db.set_latest_search(user.id, pattern)
    for i in range(constants.MessagesEachSearch):
        await bot.forward_messages(user, found_message_ids[i], channel_id)
    await event.respond(
        _('Only {} results are shown, click the buttons below for more.').
        format(constants.MessagesEachSearch),
        buttons=get_showmore_buttons(search=pattern,
                                     start=0,
                                     total=len(found_message_ids)),
    )


@bot.on(CallbackQuery())
@onstate(states.FindingInAChannel)
@withi18n
async def finding_showmore_handler(event: CallbackQuery.Event, _):
    data = event.data.decode()
    if not data.startswith(constants.CQ.FindShowMorePrefix):
        return
    __, digest, id_start = data.split(':')
    id_start = int(id_start)

    user = await event.get_chat()
    pattern = db.get_latest_search(user.id)
    # Just to make sure the button user clicks is in current search
    if hashlib.md5(pattern.encode()).hexdigest() != digest:
        return
    channel_id = db.get_user_selected(user.id)
    found_message_ids = db.find_in_messages(channel_id, pattern)
    id_end = min(id_start + constants.MessagesEachSearch,
                 len(found_message_ids))
    # print(id_start, id_end)

    for i in range(id_start, id_end):
        await bot.forward_messages(user, found_message_ids[i], channel_id)
    await event.respond(
        _('Only {} results are shown, click the buttons below for more.').
        format(constants.MessagesEachSearch),
        buttons=get_showmore_buttons(search=pattern,
                                     start=id_start,
                                     total=len(found_message_ids)),
    )


@bot.on(NewMessage())
async def channel_newmessage_handler(event: NewMessage.Event):
    """Continuously listen to channel updates, save new messages"""
    if event.is_channel:
        db.save_message(event.message)


@bot.on(MessageEdited())
async def channel_messageedited_handler(event: MessageEdited.Event):
    if event.is_channel:
        db.update_message(event.message)


@bot.on(NewMessage(pattern='/setlang'))
@onstate(states.Empty)
@withi18n
async def lang_command_handler(event: NewMessage.Event, _):
    user = await event.get_chat()
    buttons = [
        Button.inline(i18n.languages[code],
                      data=constants.CQ.SetLang.format(langcode=code))
        for code in i18n.langcodes
    ]
    buttons = three_buttons_each_line(buttons)
    # The follow button take a whole line
    buttons.insert(0, [
        Button.inline(_('Follow Telegram settings'),
                      data=constants.CQ.SetLang.format(langcode='follow'))
    ])
    db.set_user_state(user, states.SettingLang)
    await event.respond(_('Select your language:'), buttons=buttons)


@bot.on(CallbackQuery())
@onstate(states.SettingLang)
async def setting_lang_handler(event: CallbackQuery.Event):
    user = await event.get_chat()
    data = event.data.decode()
    if not data.startswith(constants.CQ.SetLangPrefix):
        return
    langcode = data.split(':')[1]
    if (langcode not in i18n.langcodes) and (langcode != 'follow'):
        await event.respond('Unsupported language selected.')
        return
    db.set_user_lang(user.id, langcode)
    db.clear_user_state(user)

    async def respond(event, _):
        await event.respond(
            _('Hi! To /find in your channel, you must /add it to this bot first.'
              ))

    await withi18n(respond)(event)


@bot.on(NewMessage(pattern=r'/help'))
@onstate(states.Empty)
@withi18n
async def help_command_handler(event: NewMessage.Event, _):
    await event.respond(
        _('/add - Add a channel to the bot\n'
          '/find - Find in a channel\n'
          '/cancel - Cancel or quit current operation\n'
          '/setlang - Set bot language\n'
          '/settoken - Create a token for non-admins to search'))


@bot.on(NewMessage(pattern=r'/settoken'))
@onstate(states.Empty)
@withi18n
async def settoken_command_handler(event: NewMessage.Event, _):
    user = await event.get_chat()
    message_text = _('Select a channel to set search token:')
    if await channel_picker(event, user, message_text, _):
        db.set_user_state(user, states.SelectingAChannelToSetToken)


@bot.on(CallbackQuery())
@onstate(states.SelectingAChannelToSetToken)
@withi18n
async def select_channel_to_set_token_handler(event: CallbackQuery.Event, _):
    user = await event.get_chat()
    data = event.data.decode()
    if not data.startswith(constants.CQ.SelectAChannelPrefix):
        return
    channel_id = int(data.split(':')[1])

    if not db.is_channel_admin(user, channel_id):
        not_admin_message(event, user, _)
        return

    me = await bot.get_me()
    channel_title = db.get_channel_title(channel_id)
    token = db.set_channel_token(channel_id)
    db.clear_user_state(user)
    await event.respond(
        _('Search token for channel **{}** has been set.\n'
          'Share this URL to allow others to search in your channel:\n\n'
          'https://t.me/{}?start={}').format(channel_title, me.username, token))


def sigterm_handler(num, frame):
    db.conn.commit()
    os.sys.exit(130)


def main():
    # Save database when being killed
    signal.signal(signal.SIGTERM, sigterm_handler)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.disconnected)
    except KeyboardInterrupt:
        db.conn.commit()


if __name__ == '__main__':
    main()
