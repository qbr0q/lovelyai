from app.bot.handlers.utils import prepare_field_edit
from app.bot.handlers.constants import CREATION_ORDER
from app.database.models import UserFilter, UserMedia


async def fill_profile(message, state, step=0):
    creation_name = CREATION_ORDER[step]
    field_data = await prepare_field_edit(state, creation_name)

    await state.set_state(field_data.state.create_state)
    await message.answer(field_data.text, reply_markup=field_data.rm)


async def save_profile(session, profile_data, user):
    user_filter_record = UserFilter(user_id=user.id)

    user_media_records = []
    for media in profile_data.media:
        media_data = media[-1]
        user_media_records.append(
            UserMedia(
                file_id=media_data.file_id,
                unique_file_id=media_data.file_unique_id,
                user_id=user.id
            )
        )

    session.add(user)
    session.add(user_filter_record)
    session.add_all(user_media_records)

