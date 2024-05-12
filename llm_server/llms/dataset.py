import pandas as pd
import os
def get_recipe(idx=0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'recipies/RAW_recipes_shortened.csv')

    food_df = pd.read_csv(file_path)
    if idx > food_df.shape[0]-1:
        raise ValueError('Index out of range')

    recipe = food_df.iloc[idx]
    return recipe
    # return '\n'.join(map(lambda idx_step: f'{idx_step[0]+1}. ' + idx_step[1], enumerate(recipe[2:-2].split("', '"))))