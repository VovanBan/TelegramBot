from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart
from weather import get_weather
import database

bot = Bot(token='5465365408:AAEf6jDHgqTKQBG6-dxywz6rlWesslpdPMU', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

replyKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttonGeo = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
replyKeyboard.add(buttonGeo)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>, этот бот может показать <b>погоду</b>\n'
                              f'Для этого просто <b>отправь геолокацию</b>', reply_markup=replyKeyboard)


@dp.message_handler(content_types='location')
async def get_weather_bot(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    data = get_weather(lat, lon)
    await message.answer_photo(photo=data['weatherPhoto'], caption=f'***{data["data_now"]}***\n'
                                                                   f'<b>Местоположение</b>: {data["city"]}\n'
                                                                   f'<b>Погода</b>: {data["smile"]}\n'
                                                                   f'<b>Температура</b>: {data["temp"]}\n'
                                                                   f'<b>Скорость ветра</b>: {data["wind"]}\n'
                                                                   f'<b>Восход в</b> {data["sunrise"]}\n'
                                                                   f'<b>Закат в</b> {data["sunset"]}\n'
                               )
    database.updateDatabase(str(message.from_user.first_name), int(message.from_user.id), float(lat), float(lon))

@dp.message_handler(commands='list', user_id='1136649586')
async def get_database(message: types.Message):
    listUsers = database.lockDatabase()
    if len(listUsers) != 0:
        for user in listUsers:
            await message.answer(text=f'Name: {user[0]}\n'
                                      f'ID: {user[1]}\n'
                                      f'lat: {user[2]}\n'
                                      f'lon: {user[3]}'
                                 )
    else:
        await message.answer(text='Список пуст')

@dp.message_handler(commands='delete')
async def delete_element(message: types.Message):
    print(message.get_args())
    if message.get_args() != '':
        database.deleteElementDatabase(int(message.get_args()))
        await message.answer(text='Пользователь удалён')
    else:
        await message.answer(text='Нет аргументов')

executor.start_polling(dp, skip_updates=True)
