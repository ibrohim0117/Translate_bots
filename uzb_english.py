import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from translate import Translator
from u_e_d import reg, chek, kb, Habar, creat_table

logging.basicConfig(level=logging.INFO)  # noqa
API_TOKEN = os.getenv('TOKEN')
bot = Bot(API_TOKEN)  # noqa

storage = MemoryStorage()

dp = Dispatcher(bot, storage=MemoryStorage())

check = {
    'check': 'en_uz'
}


@dp.message_handler(commands=['start'])
async def suz(msg: types.Message):
    await bot.set_my_commands([BotCommand(command="/start", description="Botni qayta ishga tushurish"),
                               BotCommand(command="/enuz", description="English -> Uzbek holati"),
                               BotCommand(command="/uzen", description="Uzbek -> English holati"),
                               BotCommand(command="/uzru", description="Uzbek -> Rus holati"),
                               BotCommand(command="/ruuz", description="Rus -> Uzbek holati")
                               ])

    if msg.from_user.id == 1038185913:
        await msg.answer("Admin uchun menyular", reply_markup=kb)

    l = chek()  # noqa
    if str(msg.from_user.id) not in l:
        reg(msg.from_user.id, str(msg.from_user.username))

    if check['check'] == 'en_uz':   # noqa
        s = "Bot  English - O'zbek holatida. " \
            "O'zbek  - English holatiga o'tish uchun  /uzen  buyrug'ini bering."
        await msg.answer(s)

    elif check['check'] == 'uz_en':
        s = "Bot  O'zbek  - English  holatida. " \
            " English - O'zbek holatiga o'tish uchun  /enuz  buyrug'ini bering."
        await msg.answer(s)

    elif check['check'] == 'uz_ru':
        s = "Bot O'zbek - Rus holatida. " \
            "Rus - O'zbek holatiga o'tish uchun  /ruuz  buyrug'ini bering."
        await msg.answer(s)

    else:
        s = "Bot  Rus - O'zbek  holatida. " \
            " O'zbek - Rus holatiga o'tish uchun  /uzru  buyrug'ini bering."
        await msg.answer(s)

@dp.message_handler(commands=['uzen'])    # noqa
async def suz(msg: types.Message):
    s = "O'zbek - English holatiga o'tildi. " \
        "English - O'zbek holatiga o'tish uchun  /enuz  buyrug'ini bering."
    check.update({'check': 'uz_en'})
    await msg.answer(s)


@dp.message_handler(commands=['enuz'])
async def suz1(msg: types.Message):
    s = "English - O'zbek holatiga o'tildi. " \
        "O'zbek  - English holatiga o'tish uchun  /uzen  buyrug'ini bering."
    check.update({'check': 'en_uz'})
    await msg.answer(s)


@dp.message_handler(commands=['uzru'])    # noqa
async def suz2(msg: types.Message):
    s = "O'zbek - Rus holatiga o'tildi. " \
        "Rus - O'zbek holatiga o'tish uchun  /ruuz  buyrug'ini bering."
    check.update({'check': 'uz_ru'})
    await msg.answer(s)


@dp.message_handler(commands=['ruuz'])
async def suz3(msg: types.Message):
    s = "Rus - O'zbek holatiga o'tildi. " \
        "O'zbek - Rus holatiga o'tish uchun  /uzru  buyrug'ini bering."
    check.update({'check': 'ru_uz'})
    await msg.answer(s)


@dp.message_handler(Text("📋 E'lon joylash"))
async def latter(msg: types.Message):
    await Habar.letter.set()
    await msg.answer("Xabarni kiriting: ")


@dp.message_handler(state=Habar.letter, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    await msg.answer(text="Reklama jo'natish boshlandi!")
    l = chek()  # noqa
    for i in l:
        try:
            await msg.copy_to(i, caption=msg.caption, caption_entities=msg.caption_entities)
        except:  # noqa
            pass
    await state.finish()


@dp.message_handler()
async def fung(msg: types.Message):
    if check['check'] == 'en_uz':   # noqa
        translator1 = Translator(to_lang="uz", from_lang='en')
        translation1 = translator1.translate(msg.text)
        if "&#39;" in translation1:  # noqa
            translation1 = translation1.replace("&#39;", "'")
        if "&#10;" in translation1:
            translation1 = translation1.replace("&#10;", '\n')
        if "&quot;" in translation1:
            translation1 = translation1.replace("&quot;", '\"')
        if "&gt;" in translation1:
            translation1 = translation1.replace("&gt;", '>')
        if "&lt;" in translation1:
            translation1 = translation1.replace("&lt;", '<')
        await msg.answer(translation1)

    elif check['check'] == 'uz_en':
        translator = Translator(to_lang='en', from_lang='uz')
        translation = translator.translate(msg.text)
        await msg.answer(translation)

    elif check['check'] == 'uz_ru':     # noqa
        translator1 = Translator(to_lang='ru', from_lang='uz')
        translation1 = translator1.translate(msg.text)  # noqa
        await msg.answer(translation1)

    else:
        translator = Translator(to_lang='uz', from_lang='ru')
        translation = translator.translate(msg.text)
        await msg.answer(translation)

async def on_startup(dp):   # noqa
    creat_table()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
