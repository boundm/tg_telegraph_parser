from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.core.logic import parse_title

router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("👋 Привет! Отправь название статьи")

@router.message(F.text)
async def parse_handler(msg: Message):
    title = msg.text.strip()

    if "," in title:
        await msg.answer("❗ Пожалуйста, отправьте только одно название статьи за раз.")
        return

    await msg.answer("⏳ Ищу статью, это может занять время...")

    results = await parse_title(title, offset=2)

    if not results:
        await msg.answer("❌ Ничего не найдено.")
        return

    for i in range(0, len(results), 20):
        await msg.answer("\n".join(results[i:i + 20]))
