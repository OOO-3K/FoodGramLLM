#TODO: handle errors in APIs such as limit overrun etc.
#TODO: translate
#TODO: other API
import google.generativeai as genai

import numpy as np
import pandas as pd

import google.generativeai as genai
import google.ai.generativelanguage as glm

import os
import re

from.prompt import make_prompt_for_questions, example_prompt
from pprint import pprint

import PIL.Image

from dotenv import load_dotenv
load_dotenv()

class GeminiAPI:

    def __init__(self):
        __gemini_api_key = os.getenv("GEMINI_API_KEY")

        genai.configure(api_key=__gemini_api_key)

        self.model = genai.GenerativeModel('gemini-pro')
        pass

    def call(self, prompt: str, image: PIL.Image.Image | None = None, max_tokens: int = 100, temperature: float = 0.75, top_p: float = 0.95, top_k: int = 0):
        whole_prompt = [prompt]
        if image is not None:
            whole_prompt.append(image)
        response = self.model.generate_content(
            whole_prompt,
            # generation_config=genai.types.GenerationConfig(
            #     # Only one candidate for now.
            #     candidate_count=1,
            #     stop_sequences=['x'],
            #     max_output_tokens=20,
            #     temperature=1.0,
            #     top_p=top_p,
            #     top_k=top_k
            # )
        )
        return response.text

    def get_recipe_questions(self, recipe_prompt: str):
        response = self.call(recipe_prompt)

        questions = []

        # try:
        regex = r"<step (\d+)>([\s\S]*?)</step \d+>"
        matches = re.finditer(regex, response, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            questions.append(match.group(2).strip().split('\n'))
            # 0 - not used
            # 1 - number of step
            # 2 - step text

            # questions.append([])
            # print(match.groups())
            # for groupNum in range(1, len(match.groups())):
            #     groupNum = groupNum + 1
            #     block = match.group(groupNum)
                
            #     questions[-1].append(block)

        # except Exception as e:
        #     raise ValueError('Error in response parsing: ' + str(e))
        # pass

        return response, questions

    def get_recipe_description(self, recipe_prompt: str):
        response = self.call(recipe_prompt)
        return response
def main():
    prompt = example_prompt(80)

    gemini_api = GeminiAPI()
    # response = gemini_api.call(prompt)
    # print(response)
    # response, questions = gemini_api.get_recipe_questions(prompt)
    response = gemini_api.get_recipe_description(prompt)
    print(response)
    pass

if __name__ == "__main__":
    main()