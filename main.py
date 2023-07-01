import asyncio

import config
from states import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile, ContentType
from aiogram.dispatcher import FSMContext
import logging

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


FIRST = []
SECOND = []
THIRD = []
FOUR = []
FIVE = []


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Здравствуйте!'))
    await message.answer("Приветствую", reply_markup=keyboard)


async def hello(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Хочу записаться на бесплатную консультацию'))
    keyboard.add(types.KeyboardButton(text='Хочу ссылку на бесплатный вебинар'))
    keyboard.add(types.KeyboardButton(text='Вопрос по Самостоятельному банкротству'))
    keyboard.add(types.KeyboardButton(text="""Документы Образцы\n(Кредиторы, Банки, Суды, ФССП и для МФЦ"""))
    keyboard.add(types.KeyboardButton(text='Хочу узнать стоимость банкротства'))
    await message.answer("Какой вопрос вас интересует?", reply_markup=keyboard)


async def first_form(message: types.Message, state: FSMContext):
    if message.from_user.id not in FIRST:
        await state.update_data(form=1)
        await message.answer("""Заполните форму, наш сотрудник перезвонит в рабочее время в течении 15 мин. и запишет Вас\n\n(для получения документов укажите действующую эл.почту)""")
        await FormOne.name.set()
        return await message.answer("Введите ваше имя")
    await message.answer("Вы уже заполняли форму")


@dp.message_handler(state=FormOne.name)
async def first_form_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона (пример - 79623241232)")
    await FormOne.phone.set()


@dp.message_handler(state=FormOne.phone)
async def first_form_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите вашу почту")
    await FormOne.email.set()


@dp.message_handler(state=FormOne.email)
async def first_form_email(message: types.Message, state: FSMContext):
    global FIRST, SECOND, THIRD, FIVE
    data = await state.get_data()
    if data['form'] == 1:
        FIRST.append(message.from_user.id)
        for chat_id in config.ID:
            await bot.send_message(chat_id=chat_id, text=f'Пользователь выбрал "Хочу ссылку на бесплатный вебинар"\n'
                                                         f'Имя - {data["name"]}\nПочта - {message.text}\nТелефон - {data["phone"]}')
    elif data['form'] == 2:
        SECOND.append(message.from_user.id)
        for chat_id in config.ID:
            await bot.send_message(chat_id=chat_id, text=f'Пользователь выбрал "Хочу записаться на бесплатную консультацию"\n'
                                                         f'Имя - {data["name"]}\nПочта - {message.text}\nТелефон - {data["phone"]}')
    elif data['form'] == 3:
        THIRD.append(message.from_user.id)
        for chat_id in config.ID:
            await bot.send_message(chat_id=chat_id, text=f'Пользователь выбрал "Документы Образцы\n(Кредиторы, Банки, Суды, ФССП и для МФЦ)"\n'
                                                         f'Ответы на вопросы:\n'
                                                         f'Документы - {data["doc"]}\n'
                                                         f'Имя - {data["name"]}\nПочта - {message.text}\nТелефон - {data["phone"]}')
    elif data['form'] == 5:
        FIVE.append(message.from_user.id)
        for chat_id in config.ID:
            await bot.send_message(chat_id=chat_id, text=f'Пользователь выбрал "Вопрос по Самостоятельному банкротству"\n'
                                                         f'Ответы на вопросы:\n'
                                                         f'Первый вопрос - {data["comp"]}\nВторой вопрос - {data["instructions"]}\nТретий вопрос - {data["last"]}\n'
                                                         f'Имя - {data["name"]}\nПочта - {message.text}\nТелефон - {data["phone"]}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Хочу записаться на бесплатную консультацию'))
    keyboard.add(types.KeyboardButton(text='Хочу ссылку на бесплатный вебинар'))
    keyboard.add(types.KeyboardButton(text='Вопрос по Самостоятельному банкротству'))
    keyboard.add(types.KeyboardButton(text="""Документы Образцы\n(Кредиторы, Банки, Суды, ФССП и для МФЦ"""))
    keyboard.add(types.KeyboardButton(text='Хочу узнать стоимость банкротства'))
    await state.update_data(email=message.text)
    await message.answer("Отлично", reply_markup=keyboard)
    await state.finish()


async def second_form(message: types.Message, state: FSMContext):
    if message.from_user.id not in SECOND:
        await state.update_data(form=2)
        await message.answer("""Заполните форму для получения ссылки и оповещения о начале вебинара\n\n(для получения документов укажите действующую эл.почту)""")
        await FormOne.name.set()
        return await message.answer("Введите ваше имя")
    await message.answer("Вы уже заполняли форму")


async def start_third_form(message: types.Message, state: FSMContext):
    if message.from_user.id in THIRD:
        return await message.answer("Вы уже заполняли форму")
    await message.answer("""Давайте определим подходит ли Вам процедура банкротства и сможете ли Вы самостоятельно подготовить и подать документы.\n\nОтветьте на вопросы.""")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Да", "Нет"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer("У вас есть доступ к компьютеру и принтеру для заполнения и печати документов?", reply_markup=keyboard)
    await FormThird.comp.set()


@dp.message_handler(state=FormThird.comp)
async def comp_third_form(message: types.Message, state: FSMContext):
    if message.text not in ["Да", "Нет"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Да", "Нет"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Вы сможете по видео-инструкции провести розыск своего долга, а также зарегистрироваться на сайтах интернет ресурсов (Почта России, Гос.Услуги, НБКИ, КадАрбитр)?', reply_markup=keyboard)
    await FormThird.instructions.set()
    await state.update_data(comp=message.text)


@dp.message_handler(state=FormThird.instructions)
async def instructions_third_form(message: types.Message, state: FSMContext):
    if message.text not in ["Да", "Нет"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Да", "Нет"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer("""И последний вопрос,\n\nУ вас есть залоговое имущество, а также за последние 3 года были ли сделки Купли Продажи имущества дороже 100'000 руб?""", reply_markup=keyboard)
    await FormThird.last.set()
    await state.update_data(instructions=message.text)


@dp.message_handler(state=FormThird.last)
async def end_third_form(message: types.Message, state: FSMContext):
    if message.text not in ["Да", "Нет"]:
        return await message.answer("Попробуйте еще раз")
    await state.update_data(last=message.text, form=3)
    await message.answer("""Заполните форму и напишите свой вопрос, мы перезвоним и ответим на вопрос\n\n(для получения документов укажите действующую эл.почту)""")
    await FormOne.name.set()
    await message.answer("Введите ваше имя")


async def four_form(message: types.Message, state: FSMContext):
    if message.from_user.id not in FOUR:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for text in ['Допускаю просрочки по платежам и не знаю что делать дальше', 'Уже есть Исполнительные производства и приставы начали списывать деньги с дохода', 'Тяжело платить платежи. Есть залоговое имущество',
                     'Возможно подхожу под внесудебное банкротство']:
            keyboard.add(types.KeyboardButton(text=text))
        await message.answer('Давайте уточним информацию. Выберите какая ситуация подходит вам больше?', reply_markup=keyboard)
        return await FormFour.situation.set()
    await message.answer("Вы уже заполняли форму")


@dp.message_handler(state=FormFour.situation)
async def form_four_situation(message: types.Message, state: FSMContext):
    if message.text not in ['Допускаю просрочки по платежам и не знаю что делать дальше', 'Уже есть Исполнительные производства и приставы начали списывать деньги с дохода', 'Тяжело платить платежи. Есть залоговое имущество',
                 'Возможно подхожу под внесудебное банкротство']:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["До 300'000 руб", "Более 300'000 руб"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Какова общая сумма Вашего долга на данное время?\n\n(банки, мфо, юр.лица, физ. лица, ЖКХ, налоги, страховые компании)', reply_markup=keyboard)
    await FormFour.price.set()
    await state.update_data(situation=message.text)


@dp.message_handler(state=FormFour.price)
async def form_four_price(message: types.Message, state: FSMContext):
    if message.text not in ["До 300'000 руб", "Более 300'000 руб"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Нет, не зарегистрировано", "Да, зарегистрировано"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Зарегистрирована ли на вас квартира (доля в квартире), либо жилой дом, являющийся единственным жильем?', reply_markup=keyboard)
    await FormFour.reg_home.set()
    await state.update_data(price=message.text)


@dp.message_handler(state=FormFour.reg_home)
async def form_four_reg_home(message: types.Message, state: FSMContext):
    if message.text not in ["Нет, не зарегистрировано", "Да, зарегистрировано"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Нет, не зарегистрировано", "Да, любой вид транспорта"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Зарегистрирован ли на вас транспорт?', reply_markup=keyboard)
    await FormFour.reg_auto.set()
    await state.update_data(reg_home=message.text)


@dp.message_handler(state=FormFour.reg_auto)
async def form_four_reg_auto(message: types.Message, state: FSMContext):
    if message.text not in ["Нет, не зарегистрировано", "Да, любой вид транспорта"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Нет, не имеется", "Да, имеется"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Имеется ли у Вас имущество,являющееся предметом залога, либо ипотечное имущество?', reply_markup=keyboard)
    await FormFour.reg_deposit.set()
    await state.update_data(reg_auto=message.text)


@dp.message_handler(state=FormFour.reg_deposit)
async def form_four_reg_deposit(message: types.Message, state: FSMContext):
    if message.text not in ["Нет, не имеется", "Да, имеется"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Нет, не совершались", "Да, совершались"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer("""Совершались ли вами сделки в течение последних трёх лет суммой свыше 100 тысяч рублей?\n\nПамятка: сделки купли-продажи, дарения, брачный договор; покупка или продажа недвижимого или движимого имущества – квартиры, машины, дачи, дома, земли, гаража, акций и прочих ценных бумаг, получение дивидендов. покупка юридического лица или компании, и прочие сделки стоимостью более 100 тысяч рублей""", reply_markup=keyboard)
    await FormFour.transactions.set()
    await state.update_data(reg_deposit=message.text)


@dp.message_handler(state=FormFour.transactions)
async def form_four_transactions(message: types.Message, state: FSMContext):
    if message.text not in ["Нет, не совершались", "Да, совершались"]:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Работаю", "Не работаю", 'Студент', 'Пенсионер', 'Предприниматель (ИП)', 'Учредитель компании', 'Генеральный директор', 'Военнослужащий']:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Сведения о Вашей трудовой деятельности',
                         reply_markup=keyboard)
    await FormFour.activity.set()
    await state.update_data(transactions=message.text)


@dp.message_handler(state=FormFour.activity)
async def form_four_activity(message: types.Message, state: FSMContext):
    if message.text not in ["Работаю", "Не работаю", 'Студент', 'Пенсионер', 'Предприниматель (ИП)', 'Учредитель компании', 'Генеральный директор', 'Военнослужащий']:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Не женат / не замужем", "Женат / Замужем\n\n(в случае официального брака)", 'В разводе (более 3-х лет)', 'В разводе (менее 3-х лет)']:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Укажите Ваше семейное положение',
                         reply_markup=keyboard)
    await FormFour.family.set()
    await state.update_data(activity=message.text)


@dp.message_handler(state=FormFour.family)
async def form_four_family(message: types.Message, state: FSMContext):
    if message.text not in ["Не женат / не замужем", "Женат / Замужем\n\n(в случае официального брака)", 'В разводе (более 3-х лет)', 'В разводе (менее 3-х лет)']:
        return await message.answer("Попробуйте еще раз")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Нет, не являюсь", "Да, являюсь"]:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer('Являетесь ли Вы родителем, усыновителем или опекуном несовершеннолетнего ребёнка?',
                         reply_markup=keyboard)
    await FormFour.parents.set()
    await state.update_data(family=message.text)


@dp.message_handler(state=FormFour.parents)
async def form_four_parents(message: types.Message, state: FSMContext):
    global FOUR
    data = await state.get_data()
    FOUR.append(message.from_user.id)
    for chat_id in config.ID:
        await bot.send_message(chat_id=chat_id,
                               text=f'Пользователь выбрал "Хочу узнать стоимость банкротства"\n'
                                    f'Ответы на вопросы:\n'
                                    f'Первый вопрос - {data["situation"]}\nВторой вопрос - {data["price"]}\nТретий вопрос - {data["reg_home"]}\n'
                                    f'Четвертый вопрос - {data["reg_auto"]}\nПятый вопрос - {data["reg_deposit"]}\nШестой вопрос - {data["transactions"]}\n'
                                    f'Седьмой вопрос - {data["activity"]}\nВосьмой вопрос - {data["family"]}\nДевятый вопрос - {message.text}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Хочу записаться на бесплатную консультацию'))
    keyboard.add(types.KeyboardButton(text='Хочу ссылку на бесплатный вебинар'))
    keyboard.add(types.KeyboardButton(text='Вопрос по Самостоятельному банкротству'))
    keyboard.add(types.KeyboardButton(text="""Документы Образцы\n(Кредиторы, Банки, Суды, ФССП и для МФЦ"""))
    keyboard.add(types.KeyboardButton(text='Хочу узнать стоимость банкротства'))
    if message.text not in ["Нет, не являюсь", "Да, являюсь"]:
        return await message.answer("Попробуйте еще раз")
    await state.update_data(parents=message.text)
    await state.finish()
    await message.answer('Отлично', reply_markup=keyboard)


async def start_five_form(message: types.Message, state: FSMContext):
    if message.from_user.id in FIVE:
        return await message.answer("Вы уже заполняли форму")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in ["Досудебные документы кредиторам", "Внесудебное банкротство (МФЦ)", "Судебные документы", 'Выкуп долга', 'ФССП', 'Коллектора']:
        keyboard.add(types.KeyboardButton(text=text))
    await message.answer("Какие документы Вас интересуют?", reply_markup=keyboard)
    await FormFive.doc.set()


@dp.message_handler(state=FormFive.doc)
async def doc_five_form(message: types.Message, state: FSMContext):
    if message.text not in ["Досудебные документы кредиторам", "Внесудебное банкротство (МФЦ)", "Судебные документы", 'Выкуп долга', 'ФССП', 'Коллектора']:
        return await message.answer("Попробуйте еще раз")
    await message.answer("""Стоимость пакета всех документов на 1 мес. 199 руб.\n\nЗаполните форму для оплаты и получения доступа.\n\n(укажите действующие контакты)""")
    await state.update_data(doc=message.text, form=5)
    await FormOne.name.set()
    await message.answer("Введите ваше имя")


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message, state: FSMContext):
    if message.text.capitalize() == 'Здравствуйте!':
        await asyncio.create_task(hello(message, state))
    elif message.text.capitalize() == 'Хочу записаться на бесплатную консультацию':
        await asyncio.create_task(first_form(message, state))
    elif message.text.capitalize() == 'Хочу ссылку на бесплатный вебинар':
        await asyncio.create_task(second_form(message, state))
    elif message.text == 'Вопрос по Самостоятельному банкротству':
        await asyncio.create_task(start_third_form(message, state))
    elif message.text.capitalize() == 'Хочу узнать стоимость банкротства':
        await asyncio.create_task(four_form(message, state))
    elif message.text == 'Документы Образцы\n(Кредиторы, Банки, Суды, ФССП и для МФЦ':
        await asyncio.create_task(start_five_form(message, state))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
