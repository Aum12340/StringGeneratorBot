from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "Please Choose Which String Session You Want To Generate 😇",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔰 Telethon - For Userbot 🔰", callback_data="telethon")],
          [
            InlineKeyboardButton("⚜️ Pyrogram - For Musicbot ⚜️", callback_data="pyrogram")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("Starting {} Session Generation".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'Please Send Your `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('Not A Valid API_ID (which must be an integer). Please Start Generating Session Again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'Please Send Your `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'Now Please Send Your `PHONE_NUMBER` With Your Country Code. \n\n**Example** : `+919876543210`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("Sending OTP...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` and `API_HASH` Combination Is Invalid. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`PHONE_NUMBER` Is Invalid. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "Please Check For An OTP In Official Telegram Account. If You Got It, Send OTP Here After Reading The Below Format. \n\nIf OTP Is **12345** \nPlease Send It As `1 2 3 4 5`. \n\n__**(NOTE:- IF OTP IS NOT RECEIVED THEN GENERATE STRING AFTER 2-3 HOURS)**__", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('Time Limit Reached Of 10 Minutes. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('OTP Is Invalid. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('OTP is Expired. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'Your Account Has Enabled Two-Step Verification. Please Provide The Password.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('Time Limit Reached Of 5 minutes. Please Start Generating Session Again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('Invalid Password Provided. Please Start Generating Session Again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
        try:
            await client(JoinChannelRequest("@Official_K_LegendBot"))
            await client(LeaveChannelRequest("@Official_LegendBot"))
            await client(LeaveChannelRequest("@Legend_Userbot"))
        except BaseException:
            pass
    else:
        string_session = await client.export_session_string()
    text = "**🔥 {} STRING SESSION 🔥** \n\n`{}` \n\n**⚜️ SUCCESSFULLY GENERATED STRING SESSION ⚜️** \n**⚠️ DON'T SHARE STRING SESSION WITH ANYONE ⚠️**".format("TELETHON" if telethon else "PYROGRAM", string_session)
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply("Successfully Generated {} String Session. \n\nPlease Check Your Saved Messages😇".format("**TELETHON**" if telethon else "**PYROGRAM**")),
    reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="String Session ↗️", url=f"tg://openmessage?user_id={chat.id}")]]
        )

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled The Process!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Restarted The Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled The Generation Process!", quote=True)
        return True
    else:
        return False
