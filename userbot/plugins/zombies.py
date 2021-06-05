import asyncio
import io
from asyncio import sleep
from datetime import datetime
from math import sqrt
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
    ChatAdminRequiredError,
    UserAdminInvalidError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantsKicked,
    ChatBannedRights,
    MessageActionChannelMigrateFrom,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from telethon.utils import get_input_location

from userbot import BOTLOG, BOTLOG_CHATID

from userbot.utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.cmdhelp import CmdHelp
from userbot.uniborgConfig import Config

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@bot.on(admin_cmd(pattern=f"zombies ?(.*)"))
@bot.on(sudo_cmd(pattern="zombies ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Zombi veya silinmiş hesap bulunamadı bu grupta, Grup temizdir`"
    if con != "clean":
        event = await edit_or_reply(
            show, "`Hayalet aranıyor/Silin/zombi hesapları...`"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"__Found__ **{del_u}** __ghost/deleted/zombie account(s) in this group,\
                           \nclean them by using__ `.zombies clean`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(show, "`Burada yönetici değilim.!`")
        return
    event = await edit_or_reply(
        show, "`Silinen hesaplar siliniyor...\nBunu yapabilirim.?!?!`"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_or_reply(event, "`Bu grupta yasaklama hakkım yok.`")
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"
    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"
    await edit_or_reply(event, del_status)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#CLEANUP\
            \n{del_status}\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )



CmdHelp("zombies").add_command(
  "zombies", None, "Silinenleri arar/hayalet/gruptaki zombi hesabı"
).add_command(
  "zombies clean", None, "Hayaleti yasaklar/Silin/gruptan zombi hesabı. Grubu daha iyi bir yer yapar"
).add()
