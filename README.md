# FoodGramLLM

## Форматы запросов

### Генерация вопросов

```
url = <server_url>/gemini/questions/en/
```

Аргументы:
```
- recipe_name - название рецепта
- ingredients - 
```

## Как это использовать

### Создаем окружение
```
python -m venv venv

.\venv\Scripts\activate
```
### Устанавливаем библиотеки 
```
pip install -r requirements.txt
```

### Файл с ключом
Создаем файл с именем `.env` в папке проекта.

В него добавляем строчку со своим ключом. 
```
GEMINI_API_KEY=<api_key>
```


### Запускаем сервер
В терминале запускаем команду
```
py .\llm_server\manage.py runserver
```

