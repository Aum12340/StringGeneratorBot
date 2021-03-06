from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Hey {}, 
Welcome to {}

You Can Use This Bot To Generate Pyrogram & Telethon String Session. Use Below Buttons To Operate !

**Made With Love By @WarFade â¤ï¸**
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton("ð« Start Generating Session ð«", callback_data="generate")],
        [InlineKeyboardButton(text="ð  Return Home ð ", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("ð« Start Generating Session ð«", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("ð« Start Generating Session ð«", callback_data="generate")],
        [
            InlineKeyboardButton("How to Use â", callback_data="help"),
            InlineKeyboardButton("About ð", callback_data="about")
        ],
        [InlineKeyboardButton("â£ï¸ Contact Owner â£ï¸", url="https://t.me/WarFade")],
    ]

    # Help Message
    HELP = """
â¨ **Available Commands** â¨

/start - Start The Bot
/help - Help Message
/generate - Generate String Session
/cancel - Cancel The Process
/about - About Bot
"""

    # About Message
    ABOUT = """
**About This Bot** 

A Telegram Bot To Generate Pyrogram & Telethon String Sessions. 

Made With â¤ By @WarFade

Sá´á´á´á´Êá´ á´Êá´á´ : [Click Here](https://t.me/WarFade)

FÊá´á´á´á´¡á´Êá´ : [Pyrogram](docs.pyrogram.org)

Lá´É´É¢á´á´É¢á´ : [Python](www.python.org)

Dá´á´ á´Êá´á´á´Ê : @WarFade
    """
