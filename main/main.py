import base
import config
from aiogram import types,Dispatcher,executor,Bot

bot=Bot(config.token)
dp=Dispatcher(bot)
base.creat_table()

@dp.message_handler(commands=["start"])
async def started (message: types.Message):
    if message.chat.type == "private":
        key=types.InlineKeyboardMarkup()

        b2 = types.InlineKeyboardButton(text='Как пользоваться❓', callback_data='qts')
        b1=types.InlineKeyboardButton(text='Добавить в группу➕',callback_data='add')
        b3 = types.InlineKeyboardButton(text='Реклама📈', callback_data='ads')
        b4 = types.InlineKeyboardButton(text='Купить бота💵', callback_data='buy')
        key.add(b1,b3)
        key.add(b2,b4)
        await bot.send_message(message.chat.id,f"Здраствуйте {message.chat.first_name} !Выберите пункт⬇",parse_mode='html',reply_markup=key)

@dp.message_handler(commands=["mute"],commands_prefix="!")
async def load(message:types.Message):
    await message.delete()
    try:
        num=message.text.split()[1]
    except:
        await bot.send_message(message.chat.id, "Не хватает аргументов!")
        return

    if not num.isdigit():
        await bot.send_message(message.chat.id,"Нужно указать число!\nПример: !mute 10")
        return

    member=await bot.get_chat_member(message.chat.id,message.from_user.id)
    if member.is_chat_admin():
        if message.reply_to_message is not None:
            base.add_mute(message.reply_to_message.from_user.id,num=num,fname=message.reply_to_message.from_user.first_name)
            name=message.reply_to_message.from_user.get_mention(as_html=True)
            await bot.send_message(message.chat.id,f"Теперь данный пользователь {name} может писать после {num} секунд!",parse_mode="Html")

@dp.message_handler(commands=["unmute"],commands_prefix="!")
async def deletethis(message:types.Message):
    await message.delete()
    member=await  bot.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if member.is_chat_admin():
        if message.reply_to_message is not None:
            base.del_mute(message.reply_to_message.from_user.id)
            name= message.reply_to_message.from_user.get_mention(as_html=True)
            await bot.send_message(message.chat.id,f"Теперь данный пользователь {name} , может писать",parse_mode="html")
        elif len(message.text.split()) == 2 and message.text.split()[1].isdigit():
            idu=int(message.text.split()[1])
            base.del_mute(id)
            name='<a href="tg://user?id=idu">Пользователь</a>'
            await bot.send_message(message.chat.id, f"Теперь данный пользователь {name} , может писать",
                                   parse_mode="html")


@dp.message_handler(commands=["ban"],commands_prefix="!")
async def bunned_users(message:types.Message):
    if message.chat.type!="private":
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.is_chat_admin():
            if message.reply_to_message is not None:
                await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                base.banned(id=message.reply_to_message.from_user.id,user=message.reply_to_message.from_user.username,nick=message.reply_to_message.from_user.first_name)
                await bot.send_message(message.chat.id, "Я исключил данного пользователя!")
            else:
                await bot.send_message(message.chat.id,"Данная команда должна быть в ответе на сообщение ИЛИ вы дали боту права администратора.")




@dp.message_handler(commands=["unban"],commands_prefix="!")
async def bunned_users(message:types.Message):
    if message.chat.type!="private":
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.is_chat_admin():
            try:
                if message.reply_to_message is not None:
                    await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                    base.unbaning(message.reply_to_message.from_user.id)
                    await bot.send_message(message.chat.id, "Я разбанил данного пользователя!")
            except:
                await bot.send_message(message.chat.id,"Данная команда должна быть в ответе на сообщение ИЛИ вы дали боту права администратора.")

@dp.message_handler(commands=["blist"],commands_prefix="!")
async def blacklist(message:types.Message):
    bl=base.BlackList()
    bl_msg="ID: ------ USER: ------ NAME:\n"
    if bl != []:
        for i in bl:
            bl_msg += f"{i[0]} - {i[1]} - {i[2]}\n"

        await bot.send_message(message.chat.id, bl_msg)
    else:
        await bot.send_message(message.chat.id, "Список пустой!")

@dp.message_handler(content_types=["text"])
async def priting(message:types.Message):
    if base.mute(message.from_user.id):
        await message.delete()

@dp.callback_query_handler(lambda call:True)
async def called(call:types.CallbackQuery):
    if call.data=="add":
        key=types.InlineKeyboardMarkup()
        bk=types.InlineKeyboardButton(text='Back🔙',callback_data='menu')
        key.add(bk)
        await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text='Добавьте самого бота в ваш чат. Затем выдайте боту, права администратора, после этого бот будет стабильно работать.',reply_markup=key)
    elif call.data=="qts":
        key=types.InlineKeyboardMarkup()
        bk = types.InlineKeyboardButton(text='Back🔙', callback_data='menu')
        key.add(bk)
        await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Список комманд:"+
                                                    "\n`!ban ` - Забанить пользоваться" +
                                                    "\n`!unban [id пользователя или ответ на сообщение]` - Разабанить пользоваться" +
                                                    "\n`!mute [число]` - Замутить пользавателя.Длится секудами"+
                                                    "\n`!unmute [id пользователя или ответ на сообщение]` - Размутить пользователя" +
                                                    "\n`!blist` - список забаненых пользавателей",reply_markup=key,parse_mode="Markdown")
    elif call.data=="ads":
        key = types.InlineKeyboardMarkup()
        bk = types.InlineKeyboardButton(text='Back🔙', callback_data='menu')
        key.add(bk)
        await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"Писать по поводу рекламы: @AuthorXAK",parse_mode='html',reply_markup=key)

    elif call.data=="buy":
        key = types.InlineKeyboardMarkup()
        bk = types.InlineKeyboardButton(text='Back🔙', callback_data='menu')
        key.add(bk)
        await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Данного бота можно купить у данного пользователя: @AuthorXAK",reply_markup=key)

    elif call.data=="menu":
        key = types.InlineKeyboardMarkup()

        b1 = types.InlineKeyboardButton(text='Добавить в группу➕', callback_data='add')
        b2 = types.InlineKeyboardButton(text='Как пользоваться❓', callback_data='qts')
        b3 = types.InlineKeyboardButton(text='Реклама📈', callback_data='ads')
        b4 = types.InlineKeyboardButton(text='Купить бота💵', callback_data='buy')
        key.add(b1, b3)
        key.add(b2, b4)
        await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= f"Здраствуйте {call.message.chat.first_name} !Выберите пункт⬇", reply_markup=key)


executor.start_polling(dp)