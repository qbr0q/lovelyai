from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.handlers.registration.registration import Registration
from app.core.lexicon import LEXICON


router = Router()


@router.message(F.text == LEXICON.button.import_profile)
async def start_import(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_import)
    await message.answer(LEXICON.state.waiting_import)
