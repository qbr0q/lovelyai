from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.core.lexicon import LEXICON
from app.services.ai_service import AIService
from app.bot.handlers.utils import extract_profile_data


router = Router()


@router.message(Registration.waiting_for_import)
async def process_import(message: Message, state: FSMContext, ai_service: AIService):
    if not (message.forward_from_chat or message.forward_from):
        await message.answer(LEXICON.error.message_not_forwared)
        return

    if not message.forward_from.is_bot:
        await message.answer(LEXICON.error.message_forwared_not_from_bot)
        return

    raw_text = message.text or message.caption
    profile_data = await extract_profile_data(ai_service, raw_text)
    await message.answer(str(profile_data))
