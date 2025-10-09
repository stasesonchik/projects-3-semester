NER Highlighter

Описание:
Модуль для распознавания именованных сущностей (NER) в тексте и визуализации их с подсветкой цветов.
Подходит для демонстрации работы NER на любом английском тексте.

Пример типов сущностей и цветов по умолчанию:
- PERSON (PER) — синий
- LOCATION (LOC) — красный
- ORGANIZATION (ORG) — зелёный
- MISC (MISC) — фиолетовый

Установка:
pip install transformers torch ipython

Рекомендуется использовать Jupyter Notebook или JupyterLab для отображения подсветки через HTML.

Функционал:
- Распознавание сущностей в тексте с помощью NER модели HuggingFace.
- Подсветка сущностей цветом для наглядной визуализации.
- Сохранение результата в HTML для использования вне Jupyter.
- Возможность настройки цветов и модели.

Основные функции модуля:

1. create_ner_pipeline(model_name: str = "dslim/bert-base-NER")
   Создает пайплайн HuggingFace для NER.

2. highlight_entities(text: str, entities: List[Dict], colors: Dict[str, str] = None) -> str
   Подсвечивает сущности HTML-тегами, возвращает готовый HTML.

3. display_highlighted_text(text: str, ner_pipe: pipeline, colors: Dict[str, str] = None)
   Выполняет NER на тексте и отображает результат в Jupyter.

Сохранение результата в HTML:
html_text = highlight_entities(text, entities, colors)
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_text)

Пример использования:

from ner_highlighter import create_ner_pipeline, display_highlighted_text, highlight_entities

# Создаём пайплайн
ner_pipeline = create_ner_pipeline()

# Пример текста для анализа
text = """
Alice and Bob traveled from New York to Paris last summer. 
They visited the Louvre and met with representatives from UNESCO.
"""

# Отображение в Jupyter
display_highlighted_text(text, ner_pipeline)

# Сохранение в HTML
entities = ner_pipeline(text)
html_text = highlight_entities(text, entities)
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_text)

Настройки и адаптация:
- Цвета можно изменить через словарь colors при вызове функций.
- Модель NER можно заменить любой другой предобученной моделью HuggingFace.
- Входные данные — любой текст на английском языке.
- Выходные данные — HTML-строка или отображение в Jupyter.

Пример визуализации:
- Alice, Bob → PERSON (синий)
- New York, Paris → LOC (красный)
- Louvre, UNESCO → ORG (зелёный)
- Coldplay → MISC (фиолетовый)

Преимущества:
- Легко адаптируется под разные тексты и модели.
- Модульный и параметризуемый код.
- Возможность использовать как визуализацию в Jupyter, так и сохранять HTML.
- Надёжная обработка ошибок и некорректных данных.

Требования:
- Python 3.8+
- transformers
- torch
- ipython
- Совместимость с Windows, Mac и Linux
