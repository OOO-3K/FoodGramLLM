# FoodGramLLM

## Форматы запросов

### Генерация вопросов

```
url = <server_url>/gemini/questions/en/
```

Аргументы:

```py
- recipe_name - название рецепта (str)
- ingredients - список ингредиентов ([str])
- steps - список шагов приготовления рецепта ([str])
- time - время приготовления в минутах (int)
```

Ответ:

```py
json {
    'response' : str,       # ответ модели
    'questions' : [[str]]   # Список вопросов для каждого шага (массив для каждого шага)
}
```

```py
import requests, json

response = requests.post(
    url=url, 
    data={
        'recipe_name': 'some name',
        'ingredients': json.dumps(['ingr1', 'ingr2']),
        'steps': json.dumps(['step1','step2']),
        'time': 10
    }
)

if response.ok:
    res = response.json()
```

### Генерация описания

```
url = <server_url>/gemini/questions/en/
```

Аргументы:

```py
- recipe_name - название рецепта (str)
- ingredients - список ингредиентов ([str])
- steps - список шагов приготовления рецепта ([str])
- time - время приготовления в минутах (int)
```

Ответ:

```py
json {
    'description' : str        # ответ модели
}
```

```py
import requests, json

response = requests.post(
    url=url, 
    data={
        'recipe_name': 'some name',
        'ingredients': json.dumps(['ingr1', 'ingr2']),
        'steps': json.dumps(['step1','step2']),
        'time': 10
    }
)

if response.ok:
    res = response.json()
```

### Ответ на вопрос

```
url = <server_url>/gemini/questions/en/
```

Аргументы:

```py
- recipe_name - название рецепта (str)
- ingredients - список ингредиентов ([str])
- steps - список шагов приготовления рецепта ([str])
- time - время приготовления в минутах (int)

- step_num - номер шага, для которого задается вопрос (int)
- question - вопрос (строка)

[optional]
- history - история ответов на вопросы (массив из json-объектов) 
    [{
        'role' : 'user' | 'model', 
        'parts' : str # текст вопроса/ответа
    }]
```

Ответ:

```py
json {
    'user' : {
        'role' : 'user',
        'parts' : str       # запрос к модели
    },
    'model' : {
        'role' :'model',
        'parts' : str       # ответ модели
    },
    'answer' : str           # ответ модели
}
```

Части 'user' и 'model' можно использовать для построения истории ответов на вопросы.

Пример без истории:

```py
import requests, json

response = requests.post(
    url=url, 
    data={
        'recipe_name': 'some name',
        'ingredients': json.dumps(['ingr1', 'ingr2']),
        'steps': json.dumps(['step1','step2']),
        'time': 10,

        'step_num' : 3,
        'question' : 'How long should the dough be baked for?',
    }
)

if response.ok:
    res = response.json()
```

С историей:

```py
history = [response.json()['user'], response.json()['model']]

response = requests.post(
    url=url, 
    data={
        'recipe_name': 'some name',
        'ingredients': json.dumps(['ingr1', 'ingr2']),
        'steps': json.dumps(['step1','step2']),
        'time': 10,

        'step_num' : 3,
        'question' : 'How long should the dough be baked for?',
        'history' : json.dumps(history)
    }
)

if response.ok:
    res = response.json()
```

## Как это использовать

### Создаем окружение

```ps
python -m venv venv

.\venv\Scripts\activate
```

### Устанавливаем библиотеки 

```ps
pip install -r requirements.txt
```

### Файл с ключом
Создаем файл с именем `.env` в папке проекта.

В него добавляем строчку со своим ключом. 

```file
GEMINI_API_KEY=<api_key>
```

### Запускаем сервер

В терминале запускаем команду

```ps
py .\llm_server\manage.py runserver 8080
```
Номер порта может быть любым. По умолчанию - `8000`.
