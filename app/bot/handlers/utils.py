import json

from app.services.ai_service.prompts.system_prompts import PROFILE_PARSER_SYSTEM
from app.services.ai_service.prompts.user_prompts import PROFILE_PARSER_USER


async def extract_profile_data(ai_service, raw_text):
    user_prompt = PROFILE_PARSER_USER.format(raw_text=raw_text)
    profile_data = await ai_service.ai_request(
        PROFILE_PARSER_SYSTEM,
        user_prompt,
        response_type="json_object",
        temperature=0
    )

    if profile_data.startswith("```"):
        profile_data = profile_data.strip("`").replace("json", "", 1).strip()

    return json.loads(profile_data)
