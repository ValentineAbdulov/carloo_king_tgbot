import aiohttp
import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text, Command, CommandHelp, CommandStart

from tgbot_template.tgbot.misc.states import carstate


async def start(message: types.Message, state: FSMContext):
    await register_user()
    await message.answer(
        f'Hi here you can look up some cars` specs. To looking please tell me mark of car, which specs you wanna find:'
    )

    await carstate.state1.set()


async def model_(message: types.Message, state: FSMContext):
    mark = message.text
    await message.answer(
        f'Okay, {mark}. So next, please tell me model of car:'
    )
    await carstate.state2.set()
    await state.update_data(mark=mark)
async def get_car(message: types.Message, state: FSMContext ):
    model = message.text
    data = await state.get_data()
    mark= data.get('mark')
    params = {'limit': '10',
              'make': mark,
              "model": model
              }
    headers = {'X-Api-Key': message.bot['config'].misc.X_apikey}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://api.api-ninjas.com/v1/cars', params=params) as response:
            data = await response.json()
            if len(data) == 0:
                await message.answer('Not found :(')
            for car in data:
                await message.answer(f'''car`s spec:
car`s class: {car["class"]},
car`s drive transmission: {car['drive']},
car`stype of transmission: {car['transmission']}
car`s number of cylinders in engine: {car['cylinders']},
car`s model year: {car['year']},
car`s city fuel consumption (in miles per gallon): {car['city_mpg']},
car`s highway fuel consumption (in miles per gallon): {car['highway_mpg']},
car`s combination (city and highway) fuel consumption (in miles per gallon): {car['combination_mpg']},
''')
    await state.finish()




def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'] )
    dp.register_message_handler(model_, state=carstate.state1)
    dp.register_message_handler(get_car, state=carstate.state2)


