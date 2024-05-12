from django.apps import AppConfig
from llms.llm import GeminiAPI

class GeminiCallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gemini_call"

    def ready(self):
        self.api = GeminiAPI()
        pass