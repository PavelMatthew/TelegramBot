import asyncio
import math as m
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


def solve(a, b, c):
    D = m.pow(b, 2) - 4 * a * c

    if a != 0:
        if D > 0:
            x1 = (-b + m.pow(D, 0.5)) / (2 * a)
            x2 = (-b - m.pow(D, 0.5)) / (2 * a)
            return x1, x2
        elif D == 0:

            x1 = (-b + m.pow(D, 0.5)) / (2 * a)
            return x1

        else:
            return "Нет действительных корней"
    else:
        return 'a = 0, это не квадратное уравнение'

bot = Bot(token='YOUR TOKEN')
dp = Dispatcher()


class Arguments(StatesGroup):
    a = State()
    b = State()
    c = State()


@dp.message(Command('solve'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Arguments.a)
    await message.answer('Решим уравнение вида: a*x^2+b*x+c = 0')
    await message.answer('Введите a')


@dp.message(Arguments.a)
async def get_a(message: Message, state: FSMContext):
    await state.update_data(a=message.text)
    await state.set_state(Arguments.b)
    await message.answer('Введите b')


@dp.message(Arguments.b)
async def get_b(message: Message, state: FSMContext):
    await state.update_data(b=message.text)
    await state.set_state(Arguments.c)
    await message.answer('Введите c')


@dp.message(Arguments.c)
async def get_c(message: Message, state: FSMContext):
    await state.update_data(c=message.text)
    data = await state.get_data()
    #str(solve(float(data['a']), float(data['b']), float(data['c'])))
    await message.answer(str(solve(float(data['a']), float(data['b']), float(data['c']))))
    await state.clear()


async def main_f():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main_f())

    except KeyboardInterrupt:
         print('Бот выключен')
