from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from llms.prompt import make_prompt_for_questions

@csrf_exempt
def gemini_en_index(request):
    app_config = apps.get_app_config('gemini_call')

    api = app_config.api

    if request.method != 'POST':
        return HttpResponse("Invalid request", status=400)

    recipe_name = request.POST.get('recipe_name')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    time = request.POST.get('time')

    try: 
        prompt = make_prompt_for_questions(recipe_name, ingredients, steps, time)
    except ValueError as e:
        return HttpResponse(f"Invalid request: {e}", status=400)
        
    response, questions = api.get_recipe_questions(prompt)

    return JsonResponse({
        'response': response,
        'questions': questions
    })