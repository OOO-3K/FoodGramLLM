from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from llms.prompt import make_prompt_for_questions, make_prompt_for_description, make_system_instruction
import json

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

@csrf_exempt
def gemini_answers_en_index(request):
    app_config = apps.get_app_config('gemini_call')

    if request.method != 'POST':
        return HttpResponse("Invalid request: not a POST method", status=402)

    recipe_name = request.POST.get('recipe_name')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    time = request.POST.get('time')

    step_num = request.POST.get('step_num')
    question = request.POST.get('question')

    hist = request.POST.get('history')
    if hist:
        history = json.loads(hist)
    else:
        history = []

    try: 
        system_prompt = make_system_instruction(recipe_name, ingredients, steps, time)
    except ValueError as e:
        return HttpResponse(f"Invalid request: {e}", status=401)

    api = app_config.api.get_chat_api(system_prompt)

    print(type(history))
    
    print(history)
    print('---')
    chat = api.chat_model.start_chat(history=history)
    print(chat.history)
    prompt = f'''Question for step {step_num}: {question}'''

    try:
        response = chat.send_message(prompt)
    except Exception as e:
        return HttpResponse(f"Invalid request: {e}", status=401)

    return JsonResponse({
        'user': {
            'role': 'user',
            'parts' : prompt
        },
        'model': {
            'role': 'model',
            'parts': response.text
        },
        'answer' : response.text,
    })    