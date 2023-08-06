from pydantic import BaseModel


class LangDetectionConfiguration(BaseModel):
    url = 'https://api.meaningcloud.com/lang-4.0/identification'
    timeout: int = 30
