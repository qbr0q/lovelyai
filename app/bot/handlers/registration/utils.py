import json
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import UserMedia
from app.services.ai_service.prompts.system_prompts import PROFILE_PARSER_SYSTEM
from app.services.ai_service.prompts.user_prompts import PROFILE_PARSER_USER
from app.core.utils import Profile


async def extract_profile_data(ai_service, raw_text):
    user_prompt = PROFILE_PARSER_USER.format(raw_text=raw_text)
    response_raw = await ai_service.ai_request(
        PROFILE_PARSER_SYSTEM,
        user_prompt,
        response_type="json_object",
        temperature=0
    )

    if response_raw.startswith("```"):
        response_raw = response_raw.strip("`").replace("json", "", 1).strip()
    response = json.loads(response_raw)
    profile_data = Profile(**response)

    return profile_data


def record_media(profile_data_media, user_id):
    user_media_records = []
    for media_data in profile_data_media:
        user_media_records.append(
            UserMedia(
                file_id=media_data.file_id,
                file_unique_id=media_data.file_unique_id,
                user_id=user_id
            )
        )
    return user_media_records


async def save_profile(session: AsyncSession, profile_data, user):
    try:
        user_data = profile_data.model_dump(exclude={"media"}, exclude_unset=True)
        for k, v in user_data.items():
            setattr(user, k, v)
        user_media_records = record_media(profile_data.media, user.id)

        session.add(user)
        session.add_all(user_media_records)
    except Exception as e:
        pass


def prepare_media(album, message_photo):
    if album:
        return [media.photo[-1] for media in album]
    elif message_photo:
        return [message_photo[-1]]
    return []


# async def refresh_edit_menu(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     profile_data = state_data.get("profile_data")
#     old_menu_id = state_data.get("menu_id")
#     profile_ui = show_editable_profile(profile_data)
#
#     try:
#         await message.bot.delete_message(message.chat.id, old_menu_id)
#     except Exception as e:
#         pass
#
#     new_msg = await message.answer(
#         text=profile_ui.text,
#         reply_markup=profile_ui.kb
#     )
#
#     await state.update_data(menu_id=new_msg.message_id)
