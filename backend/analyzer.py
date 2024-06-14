from typing import List, Tuple
from openai import OpenAI
import os
import base64

from globals import OPENAI_API_KEY, get_os_meme_path


class Analyzer:
    def __init__(self, api_key: str = OPENAI_API_KEY, model:str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    @staticmethod
    def encode_image(image_path: str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @classmethod
    def prompt(cls) -> str:
        return """Analyze attached meme. 
If there's any text on the image extract it and try to explain it.
In the last line return only the comma-separated keywords describing the meme.  
"""

    def _analyze_image(self, image_path: str) -> str:
        b64_encoded_image = Analyzer.encode_image(image_path)
        extension = image_path.split('/')[-1].split('.')[-1]
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": self.prompt()},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{extension};base64,{b64_encoded_image}"
                    }
                }
            ]
        }

        completion = self.client.chat.completions.create(
            messages=[message],
            model=self.model,
        )

        return completion.choices[0].message.content
    
    def analyze_image(self, image_path: str) -> Tuple[str, List[str]]:
        _image_path = get_os_meme_path(image_path)
        output = self._analyze_image(_image_path)
        lines = output.split('\n')
        keywords = lines.pop()
        keywords = [_txt.strip() for _txt in keywords.split(',')]
        return '\n'.join(lines), keywords