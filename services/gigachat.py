from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from config import settings
from services.prompts import RESUME_SYSTEM_PROMPT, build_resume_prompt


class GigaChatService:
    def __init__(self):
        self.client = GigaChat(
            credentials=settings.gigachat_credentials,
            model=settings.gigachat_model,
            verify_ssl_certs=False,
            timeout=90,
        )

    async def improve_resume(
        self,
        resume_text: str,
        vacancy_text: str | None = None
    ) -> str:
        user_prompt = build_resume_prompt(resume_text, vacancy_text)

        messages = [
            Messages(role=MessagesRole.SYSTEM, content=RESUME_SYSTEM_PROMPT),
            Messages(role=MessagesRole.USER, content=user_prompt),
        ]

        response = await self.client.achat(
            Chat(
                messages=messages,
                temperature=0.1,      # почти без креативности
                top_p=0.3,
                max_tokens=2000
            )
        )
        return response.choices[0].message.content.strip()
