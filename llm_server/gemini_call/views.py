from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from llms.prompt import make_prompt_for_questions, make_prompt_for_description

@csrf_exempt
def gemini_questions_en_index(request):
    app_config = apps.get_app_config('gemini_call')

    api = app_config.api

    if request.method != 'POST':
        return HttpResponse("Invalid request: not a POST method", status=402)

    recipe_name = request.POST.get('recipe_name')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    time = request.POST.get('time')

    try: 
        prompt = make_prompt_for_questions(recipe_name, ingredients, steps, time)
    except ValueError as e:
        return HttpResponse(f"Invalid request: {e}", status=401)

    response, questions = api.get_recipe_questions(prompt)

    if not questions:
        return HttpResponse(f"Invalid request: empty list of questions", status=400)

    return JsonResponse({
        'response': response,
        'questions': questions
    })

@csrf_exempt
def gemini_description_en_index(request):
    app_config = apps.get_app_config('gemini_call')

    api = app_config.api

    if request.method != 'POST':
        return HttpResponse("Invalid request: not a POST method", status=402)

    recipe_name = request.POST.get('recipe_name')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    time = request.POST.get('time')

    try: 
        prompt = make_prompt_for_description(recipe_name, ingredients, steps, time)
    except ValueError as e:
        return HttpResponse(f"Invalid request: {e}", status=401)

    response = api.get_recipe_description(prompt)

    return JsonResponse({
        'description': response,
    })