#TODO: add nutritions
#TODO: add description generation
#TODO: make answer generation

import os
import sys

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from llms.dataset import get_recipe
import pandas as pd
from typing import List

def list_to_str(lst: List[int | str | float]) -> str:
    return '\n'.join(map(lambda idx_item: f'{idx_item[0]+1}. ' + f'{idx_item[1]}', enumerate(lst)))

def time_to_str(time: int | None ) -> str:
    if time is None:
        return ''
    time = int(time)
    if time < 60:
        return f'Cooking time: {time} minutes'
    elif time < 60 * 24:
        return f'Cooking time: {time//60} hours and {time%60} minutes'
    else:
        time = time // (60 * 24)
        return f'Cooking time: {time} days and {time%24} hours'

    return f'Cooking time: {time} minutes' 

def make_prompt_for_questions(recipe_name: str = None, ingredients: List[str] = None, steps: List[str] = None, time: str = None ) -> str:
    recipe_name = f'Name: {recipe_name}' if recipe_name else ''

    ingredients_str = f'Ingredients:\n{list_to_str(ingredients)}' if ingredients else ''

    if not steps:
        raise ValueError('Steps must be provided')

    steps_str = f'Steps:\n{list_to_str(steps)}'

    time_str = time_to_str(time)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'templates/questions_template.txt')
    template = open(file_path, 'r').read()
    
    return template.format(
        recipe_name=recipe_name,
        ingredients=ingredients_str,
        steps=steps_str,
        time=time_str
    )

def example_prompt(idx=0):
    recipe = get_recipe(idx)

    recipe_name = recipe['name']
    ingredients = recipe['ingredients']
    steps = recipe['steps']
    time = recipe['minutes']

    ingredients = ingredients[2:-2].split("', '")
    steps = steps[2:-2].split("', '")

    prompt = make_prompt_for_description(recipe_name, ingredients, steps, time)
    return prompt

def make_prompt_for_description(recipe_name: str = None, ingredients: List[str] = None, steps: List[str] = None, time: str = None ) -> str:
    recipe_name = f'Name: {recipe_name}' if recipe_name else ''

    ingredients_str = f'Ingredients:\n{list_to_str(ingredients)}' if ingredients else ''

    if not steps:
        raise ValueError('Steps must be provided')

    steps_str = f'Steps:\n{list_to_str(steps)}'

    time_str = time_to_str(time)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'templates/description_template.txt')
    template = open(file_path, 'r').read()
    
    return template.format(
        recipe_name=recipe_name,
        ingredients=ingredients_str,
        steps=steps_str,
        time=time_str
    )
    
    pass

def main():
    prompt = example_prompt()
    print(prompt)
    pass

if __name__ == "__main__":
    main()