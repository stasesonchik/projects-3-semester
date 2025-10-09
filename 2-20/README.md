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

Рекомендуется использовать Jupyter Notebook для отображения HTML с подсветкой.

Использование:

from ner_highlighter import create_ner_pipeline, display_highlighted_text

# Создаём пайплайн NER
ner_pipeline = create_ner_pipeline()

# Текст для анализа
text = """
Alice and Bob traveled from New York to Paris last summer. 
They visited the Louvre and met with representatives from UNESCO.
"""

# Отображаем подсветку
display_highlighted_text(text, ner_pipeline)

Функции модуля:

1. create_ner_pipeline(model_name: str = "dslim/bert-base-NER")
   Создает пайплайн HuggingFace для NER.

2. highlight_entities(text: str, entities: List[Dict], colors: Dict[str, str] = None) -> str
   Подсвечивает сущности HTML-тегами, возвращает готовый HTML.

3. display_highlighted_text(text: str, ner_pipe: pipeline, colors: Dict[str, str] = None)
   Выполняет NER на тексте и отображает результат в Jupyter.

Настройки:

- Цвета можно менять через словарь colors при вызове функций.
- Можно использовать любую предобученную модель HuggingFace для NER.
- Работает с любым английским текстом.

Пример визуализации:

После выполнения кода в Jupyter Notebook текст будет подсвечен цветами по типу сущностей:

- Alice, Bob → PERSON (синий)
- New York, Paris → LOC (красный)
- Louvre, UNESCO → ORG (зелёный)
- Coldplay → MISC (фиолетовый)
