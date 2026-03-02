from app.bot.handlers.utils import prepare_field_edit
from app.bot.handlers.constants import CREATION_ORDER


async def fill_profile(message, state, step=0):
    creation_name = CREATION_ORDER[step]
    field_data = await prepare_field_edit(creation_name, state)

    await state.set_state(field_data.state.create_state)
    await message.answer(field_data.text, reply_markup=field_data.rm)
