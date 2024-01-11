rom pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, ChatNotModified, RPCError
from pyrogram.types import ChatPermissions, Message
from plugins.helper.admin_check import admin_fliter
from plugins.group_manage.databse.approve_db import Approve
from plugins.group_manage.tr_engine import tlang
from plugins.group_manage.utils.custom_filters import command, restrict_filter
from info import LOG_CHANNEL
from utils import temp
import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


@Client.on_message(command("locktypes"))
async def lock_types(_, m: Message):
    await m.reply_text(
        (
            "**Lock Types:**\n"
            " - `all` = Everything\n"
            " - `msg` = Messages\n"
            " - `media` = Media, such as Photo and Video.\n"
            " - `polls` = Polls\n"
            " - `invite` = Add users to Group\n"
            " - `pin` = Pin Messages\n"
            " - `info` = Change Group Info\n"
            " - `webprev` = Web Page Previews\n"
            " - `inlinebots`, `inline` = Inline bots\n"
            " - `animations` = Animations\n"
            " - `games` = Game Bots\n"
            " - `stickers` = Stickers"
        ),
    )
    return


@Client.on_message(command("lock") & admin_fliter)
async def lock_perm(c: Client, m: Message):
    if len(m.text.split()) < 2:
        await m.reply_text("Please enter a permission to lock!")
        return
    lock_type = m.text.split(None, 1)[1]
    chat_id = m.chat.id

    if not lock_type:
        await m.reply_text("locked 🔐")
        return

    get_perm = m.chat.permissions

    msg = get_perm.can_send_messages
    media = get_perm.can_send_media_messages
    webprev = get_perm.can_add_web_page_previews
    polls = get_perm.can_send_polls
    info = get_perm.can_change_info
    invite = get_perm.can_invite_users
    pin = get_perm.can_pin_messages
    stickers = animations = games = inlinebots = None

    if lock_type == "all":
        try:
            await c.set_chat_permissions(chat_id, ChatPermissions())
            LOGGER.info(f"{m.from_user.id} locked all permissions in {m.chat.id}")
        except ChatNotModified:
            pass
        except ChatAdminRequired:
            await m.reply_text("Ehh no  permission :)")
        await m.reply_text("locked all 🔐")
        await c.send_message(LOG_CHANNEL, text=f"**LOCKS**\n\n**USER**: {m.from_user.mention}\n\n**USER ID**:`{m.from_user.id}`\n\n**PERMISSIONS: LOCKD ALL**\n\nin **CHAT NAME**: {m.chat.title}\n**CHAT ID** `{m.chat.id}`\n\n\n**POWERD BY:** {temp.B_LINK}")
        await prevent_approved(m)
        return

    if lock_type == "msg":
        msg = False
        perm = "messages"

    elif lock_type == "media":
        media = False
        perm = "audios, documents, photos, videos, video notes, voice notes"

    elif lock_type == "stickers":
        stickers = False
        perm = "stickers"

    elif lock_type == "animations":
        animations = False
        perm = "animations"

    elif lock_type == "games":
        games = False
        perm = "games"

    elif lock_type in ("inlinebots", "inline"):
        inlinebots = False
        perm = "inline bots"

    elif lock_type == "webprev":
        webprev = False
        perm = "web page previews"

    elif lock_type == "polls":
        polls = False
        perm = "polls"

    elif lock_type == "info":
        info = False
        perm = "info"

    elif lock_type == "invite":
        invite = False
        perm = "invite"

    elif lock_type == "pin":
        pin = False
        perm = "pin"

    else:
        await m.reply_text("Invalid lock type!")
        return
    try:
        await c.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=msg,
                can_send_media_messages=media,
                can_send_other_messages=any([stickers, animations, games, inlinebots]),
                can_add_web_page_previews=webprev,
                can_send_polls=polls,
                can_change_info=info,
                can_invite_users=invite,
                can_pin_messages=pin,
            ),
        )
        LOGGER.info(f"{m.from_user.id} locked selected permissions in {m.chat.id}")
    except ChatNotModified:
        pass
    except ChatAdminRequired:
        await m.reply_text("I don't have a permission")
    await m.reply_text(
        "Locked {} for this chat".format(perm),
    )
    await c.send_message(LOG_CHANNEL, text=f"**LOCKS**\n\n**USER**: {m.from_user.mention}\n\n**USER ID**:`{m.from_user.id}`\n\n**PERMISSIONS: LOCKD {perm}**\n\nin **CHAT NAME**: {m.chat.title}\n**CHAT ID** `{m.chat.id}`\n\n\n**POWERD BY:** {temp.B_LINK}")
    await prevent_approved(m)
    return

@Client.on_message(command("locks") & admin_fliter)
async def view_locks(_, m: Message):
    chkmsg = await m.reply_text(tlang(m, "locks.check_perm_msg"))
    v_perm = m.chat.permissions

    async def convert_to_emoji(val: bool):
        if val:
            return "✅"
        return "❌"

    vmsg = await convert_to_emoji(v_perm.can_send_messages)
    vmedia = await convert_to_emoji(v_perm.can_send_media_messages)
    vother = await convert_to_emoji(v_perm.can_send_other_messages)
    vwebprev = await convert_to_emoji(v_perm.can_add_web_page_previews)
    vpolls = await convert_to_emoji(v_perm.can_send_polls)
    vinfo = await convert_to_emoji(v_perm.can_change_info)
    vinvite = await convert_to_emoji(v_perm.can_invite_users)
    vpin = await convert_to_emoji(v_perm.can_pin_messages)

    if v_perm is not None:
        try:
            permission_view_str = (tlang(m, "locks.view_perm")).format(
                vmsg=vmsg,
                vmedia=vmedia,
                vother=vother,
                vwebprev=vwebprev,
                vpolls=vpolls,
                vinfo=vinfo,
                vinvite=vinvite,
                vpin=vpin,
            )
            LOGGER.info(f"{m.from_user.id} used locks cmd in {m.chat.id}")
            await chkmsg.edit_text(permission_view_str)

        except RPCError as e_f:
            await chkmsg.edit_text("Something went wrong")
            await m.reply_text(e_f)
    return


@Client.on_message(command("unlock") & admin_fliter)
async def unlock_perm(c: Client, m: Message):
    if len(m.text.split()) < 2:
        await m.reply_text("Please enter a permission to unlock!")
        return
    unlock_type = m.text.split(None, 1)[1]
    chat_id = m.chat.id

    if not unlock_type:
        await m.reply_text(tlang(m, "locks.unlocks_perm_sp"))
        return

    if unlock_type == "all":
        try:
            await c.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )
            LOGGER.info(f"{m.from_user.id} unlocked all permissions in {m.chat.id}")
        except ChatNotModified:
            pass
        except ChatAdminRequired:
            await m.reply_text("I'm not Admin!")
        await m.reply_text("Unlock all 🔓")
        await c.send_message(LOG_CHANNEL, text=f"**LOCKS**\n\n**USER**: {m.from_user.mention}\n\n**USER ID**:`{m.from_user.id}`\n\n**PERMISSIONS: UNLOCKD ALL**\n\nin **CHAT NAME**: {m.chat.title}\n**CHAT ID** `{m.chat.id}`\n\n\n**POWERD BY:** {temp.B_LINK}")
        await prevent_approved(m)
        return

    get_uperm = m.chat.permissions

    umsg = get_uperm.can_send_messages
    umedia = get_uperm.can_send_media_messages
    uwebprev = get_uperm.can_add_web_page_previews
    upolls = get_uperm.can_send_polls
    uinfo = get_uperm.can_change_info
    uinvite = get_uperm.can_invite_users
    upin = get_uperm.can_pin_messages
    ustickers = uanimations = ugames = uinlinebots = None

    if unlock_type == "msg":
        umsg = True
        uperm = "messages"

    elif unlock_type == "media":
        umedia = True
        uperm = "audios, documents, photos, videos, video notes, voice notes"

    elif unlock_type == "stickers":
        ustickers = True
        uperm = "stickers"

    elif unlock_type == "animations":
        uanimations = True
        uperm = "animations"

    elif unlock_type == "games":
        ugames = True
        uperm = "games"

    elif unlock_type in ("inlinebots", "inline"):
        uinlinebots = True
        uperm = "inline bots"

    elif unlock_type == "webprev":
        uwebprev = True
        uperm = "web page previews"

    elif unlock_type == "polls":
        upolls = True
        uperm = "polls"

    elif unlock_type == "info":
        uinfo = True
        uperm = "info"

    elif unlock_type == "invite":
        uinvite = True
        uperm = "invite"

    elif unlock_type == "pin":
        upin = True
        uperm = "pin"

    else:
        await m.reply_text("Invalid lock type!")
        return

    try:
        LOGGER.info(f"{m.from_user.id} unlocked selected permissions in {m.chat.id}")
        await c.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=umsg,
                can_send_media_messages=umedia,
                can_send_other_messages=any(
                    [ustickers, uanimations, ugames, uinlinebots],
                ),
                can_add_web_page_previews=uwebprev,
                can_send_polls=upolls,
                can_change_info=uinfo,
                can_invite_users=uinvite,
                can_pin_messages=upin,
            ),
        )
    except ChatNotModified:
        pass
    except ChatAdminRequired:
        await m.reply_text("I'm not Admin!")
    await m.reply_text(
        "Unlocked {} for this chat.".format(uperm),
    )
    await c.send_message(LOG_CHANNEL, text=f"**LOCKS**\n\n**USER**: {m.from_user.mention}\n\n**USER ID**:`{m.from_user.id}`\n\n**PERMISSIONS: UNLOCKD {uperm}**\n\nin **CHAT NAME**: {m.chat.title}\n**CHAT ID** `{m.chat.id}`\n\n\n**POWERD BY:** {temp.B_LINK}")
    await prevent_approved(m)
    return


async def prevent_approved(m: Message):
    approved_users = Approve(m.chat.id).list_approved()
    ul = [user[0] for user in approved_users]
    for i in ul:
        try:
            await m.chat.unban_member(user_id=i)
        except (ChatAdminRequired, ChatNotModified, RPCError):
            continue
        LOGGER.info(f"Approved {i} in {m.chat.id}")
        await sleep(0.1)
    return
