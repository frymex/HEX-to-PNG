from aiogram import Bot, executor, Dispatcher
from aiogram.types import Message

import aiohttp
from aiogram.utils.exceptions import InvalidHTTPUrlContent, WrongFileIdentifier

from colorama import Fore, Back, Style

API_TOKEN = 'token'
COLORED_PRINT = False

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd(msg: Message):
    await msg.answer('<b>Send HEX code, and I send PNG picture</>\n\n'
                     '<i>Example: <code>#212121</></>')


@dp.message_handler(text_startswith='#')
async def hex_cmd(msg: Message):
    code_str = msg.text.split('#')[1][:6]
    url_server = 'http://hexcolor16.com/{hex}-{w}x{h}.png'
    try:
        await msg.answer_photo(
            url_server.format(hex=code_str, w='1080', h='1080')
        )

        await msg.answer_document(
            url_server.format(hex=code_str, w='1080', h='1080'),
            caption='<b>🖼️ Size: <code>1080x1080</>\n'
                    f'📃 Filename: <code>{code_str}-1080x1080.png</>\n'
                    f'🧬 HEX: <code>#{code_str}</>'
                    f'</>'
        )
    except (InvalidHTTPUrlContent, WrongFileIdentifier):
        maybe_len = len(msg.text.split('#')[1])
        err_by_len = True if maybe_len < 6 else False

        session = aiohttp.ClientSession()
        request = await session.get(
            url_server.format(hex=code_str, w='1080', h='1080')
        )
        await session.close()
        err_by_request = False if request.ok else False
        request.close()

        await msg.answer(f'<b>☠️ ERROR: '
                         f'<code>'
                         f'{"The length of the HEX type must be greater than 6 symbols" if err_by_len else "Internal server error" if err_by_request else "Unknown error"}</code></b>')


async def on_execute(dispatcher: Dispatcher):
    bot_obj: Bot = dispatcher.bot
    me = await bot_obj.get_me()

    if COLORED_PRINT:
        print(Back.BLUE)
        print(Back.BLUE)
        print(Back.BLUE)
        print(Back.LIGHTBLACK_EX + Fore.RED + Style.NORMAL + f'-> Bot created by [ https://t.me/cazqev ] <-')
        print(Back.LIGHTBLACK_EX + Fore.RED + Style.NORMAL + f'-> Bot started as @{me.username} <-')
        print(Back.YELLOW)
        print(Back.YELLOW)
        print(Back.YELLOW)
    else:
        print('\n\n')
        print(f'-> Bot created by [ https://t.me/cazqev ] <-')
        print(f'-> Bot started as @{me.username} <-')
        print('\n')


executor.start_polling(dp, on_startup=on_execute)
