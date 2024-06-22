from aiogram import F, types
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from django.contrib.auth.hashers import make_password

from apps.models import User
from tgbot.bot.handler.buttons import menu_buttons
from tgbot.bot.loader import dp


@dp.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("nomeringizni kiriting ☎", reply_markup=menu_buttons())


@dp.message(F.content_type.in_({ContentType.CONTACT}))
async def phone_number_handler(msg: types.Message):
    phone = msg.contact.phone_number
    password_in_database = make_password(f"{phone}{msg.from_user.id}")
    password = f"{phone}{msg.from_user.id}"
    if not await User.objects.filter(
            phone_number=phone).aexists() and msg.from_user.username and not await User.objects.filter(
            tg_id=msg.from_user.id).aexists():
        await User(last_name=msg.from_user.username, username=msg.from_user.username, phone_number=phone,
                   tg_id=msg.from_user.id, password=password_in_database).asave()

        await msg.answer(f"Your password is {password}")
        await msg.answer('link in site <a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a>', parse_mode="HTML")
    elif not await User.objects.filter(phone_number=phone).aexists() and not await User.objects.filter(
            tg_id=msg.from_user.id).aexists():
        await User(last_name=str(msg.from_user.id), username=str(msg.from_user.id), phone_number=phone,
                   tg_id=msg.from_user.id, password=password_in_database).asave()

        await msg.answer(f"Your password is {password}")
        await msg.answer(f"link in site http://127.0.0.1:8000/")
    else:
        await msg.answer("siz royxatdan o'tkansiz 😊")

