import json
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.services.ai_service.prompts.system_prompts import PROFILE_PARSER_SYSTEM
from app.services.ai_service.prompts.user_prompts import PROFILE_PARSER_USER
# from app.bot.handlers.utils import show_editable_profile
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


def get_gar_city(gar_service, city):
    gar_city = ""
    if city:
        gar_city = gar_service.get_gar_address(city)
        if gar_city:
            gar_city = gar_city[0].get("name")
    return gar_city


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
