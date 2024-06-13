import asyncio, logging, sys
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


class Form(StatesGroup):
    header = State()
    text = State()
    link_text = State()
    link_url = State()

dp = Dispatcher()
form_router = Router(name=__name__)



@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.header)
    await message.answer("Привет. Выбери шапку сообщений!")


@form_router.message(Form.header)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(header=message.text)
    await state.set_state(Form.text)
    await message.answer(
        f"Отлично, {html.quote(message.text)}!\nКакой текст соообщения?",
    )

@form_router.message(Form.text)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(Form.link_text)
    await message.reply("Текст ссылки?")


@form_router.message(Form.link_text)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_text=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Линк ссылки?")


@form_router.message(Form.link_url)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_url=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Линк ссылки?")
async def show_summary(message: Message, data: {}, positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())