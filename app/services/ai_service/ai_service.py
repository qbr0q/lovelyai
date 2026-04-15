from time import time
from typing import Literal
from openai import AsyncOpenAI
from sentence_transformers import SentenceTransformer

from app.core import settings, config
from app.core.utils import SimpleObject as so
from app.database.enums import AiRequestType
from .prompts import system_prompts, user_prompts
from .utils import LimitToken, log_request, has_limit


class AIService:
    def __init__(self):
        self.base_url = settings.ai.base_url
        self.base_model = settings.ai.default_model
        self.token_limit = settings.ai.daily_limit
        self.api_key = config.openrouter_api_key
        self.embedder = SentenceTransformer(settings.ai.embedder_model)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self):
        client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        return client

    async def ai_request(
            self,
            prompt_text: str,
            action_type: str,
            user_id: int,
            response_type: Literal["text", "json_object"] = "text",
            temperature: float = 0.7
    ):
        if await has_limit(self.token_limit, user_id):
            raise LimitToken()
        system_prompt, user_prompt = self._get_prompts(action_type, prompt_text)

        start_time = time()
        response = await self.call_api(system_prompt, user_prompt,
                                       response_type, temperature)
        end_time = time() - start_time

        await log_request(
            action_type=action_type,
            prompt_text=prompt_text,
            completion_text=response.content,
            tokens_used=response.token_used,
            response_time=end_time,
            model_name=self.base_model,
            user_id=user_id
        )

        return response.content

    async def call_api(
            self,
            system_prompt: str,
            user_prompt: str,
            response_type,
            temperature
    ):
        try:
            response = await self.client.chat.completions.create(
                model=self.base_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                response_format={"type": response_type}
            )

            return so(
                content=response.choices[0].message.content.strip(),
                token_used=response.usage.total_tokens
            )

        except Exception as e:
            print(f"AI Service Error: {e}")
            return None

    @staticmethod
    def _get_prompts(action_type, raw_request):
        if action_type == AiRequestType.create_profile:
            return system_prompts.PROFILE_PARSER_SYSTEM, \
                   user_prompts.PROFILE_PARSER_USER % raw_request

    def get_embedding(self, text: str):
        embedding = self.embedder.encode(text)
        return embedding.tolist()
