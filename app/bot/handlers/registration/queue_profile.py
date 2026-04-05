from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.states import Registration
from app.bot.handlers.utils import show_match_profile
from app.bot.handlers.kb import action_buttons
from app.database.models import User
from app.database.enums import QueueName, ActionType
from app.services import MatchingService
from app.core.lexicon import LEXICON
from app.core.utils import SimpleObject as so


async def generic_queue_manager(message: Message, state: FSMContext,
                                key: str, fetch_coro, error_text: str):
    queue = await state.get_value(key)
    current_key = f"current-{key}"

    if not queue:
        queue = await fetch_coro

    if not queue:
        await state.update_data(
            {current_key: None}
        )
        await message.answer(error_text)
        return

    profile_data = queue.pop(0)

    await state.update_data({
        key: queue,
        current_key: profile_data
    })

    return profile_data


async def process_match_queue(message: Message, state: FSMContext, user: User,
                              session: AsyncSession, match_service: MatchingService):
    profile_data = await generic_queue_manager(
        message, state, QueueName.MATCH,
        match_service.get_match(user, session),
        LEXICON.error.match_over
    )
    if profile_data:
        await state.set_state(Registration.match_action)
        await message.answer(LEXICON.message.find_match, reply_markup=action_buttons())
        await show_match_profile(message, profile_data)


async def process_like_queue(message: Message, state: FSMContext, user: User,
                             session: AsyncSession, match_service: MatchingService):
    profile_data = await generic_queue_manager(
        message, state, QueueName.RECEIVED_LIKE,
        match_service.fetch_received_like(session, user),
        LEXICON.error.received_like
    )
    if profile_data:
        await state.set_state(Registration.received_like_action)
        await message.answer(LEXICON.message.find_likes, reply_markup=action_buttons())
        await show_match_profile(message, profile_data)


queue_config = {
    Registration.match_action: so(
        key=QueueName.CURRENT_MATCH,
        process_queue=process_match_queue,
        msg=LEXICON.message.match_notify
    ),
    Registration.received_like_action: so(
        key=QueueName.CURRENT_RECEIVED_LIKE,
        process_queue=process_like_queue,
        msg=LEXICON.message.response_math
    )
}

match_action_mapping = {
    LEXICON.button.like: ActionType.like,
    LEXICON.button.dislike: ActionType.dislike,
}
