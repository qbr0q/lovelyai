from openai import AsyncOpenAI
from typing import Literal

from app.core import settings, config


class AIService:
    def __init__(self):
        self.base_url = settings.ai.base_url
        self.api_key = config.openrouter_api_key
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

    async def ai_request(self,
                         system_prompt: str,
                         user_prompt: str,
                         response_type: Literal["text", "json_object"] = "text",
                         temperature: float = 0.7
                         ):
        try:
            response = await self.client.chat.completions.create(
                model=settings.ai.default_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                response_format={"type": response_type}
            )

            content = response.choices[0].message.content.strip()

            return content

        except Exception as e:
            print(f"AI Service Error: {e}")
            return None
