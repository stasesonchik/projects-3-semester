"""
NER Highlighter

Модуль для распознавания сущностей в тексте и визуализации их с подсветкой цветов.

Зависимости:
- transformers >= 4.30.0
- torch
- IPython (для отображения в Jupyter)
"""

from transformers import pipeline
from IPython.display import display, HTML
from typing import Dict, List


def create_ner_pipeline(model_name: str = "dslim/bert-base-NER") -> pipeline:
    """
    Создает пайплайн для NER.

    Параметры:
    - model_name: название предобученной модели HuggingFace.

    Возвращает:
    - pipeline для NER.
    """
    try:
        ner_pipe = pipeline(
            "ner",
            model=model_name,
            aggregation_strategy="simple"  # объединяет токены одной сущности
        )
        return ner_pipe
    except Exception as e:
        raise RuntimeError(f"Ошибка при создании NER пайплайна: {e}")


def highlight_entities(
    text: str,
    entities: List[Dict],
    colors: Dict[str, str] = None
) -> str:
    """
    Подсвечивает сущности в тексте с помощью HTML.

    Параметры:
    - text: исходный текст.
    - entities: список сущностей, полученных из NER пайплайна.
    - colors: словарь с цветами для каждого типа сущности.

    Возвращает:
    - HTML строку с подсветкой сущностей.
    """
    if colors is None:
        colors = {
            "PER": "blue",
            "LOC": "red",
            "ORG": "green",
            "MISC": "purple"
        }

    html_text = ""
    last_idx = 0
    for ent in entities:
        try:
            start, end = ent['start'], ent['end']
            entity_type = ent.get('entity_group', 'MISC')
            color = colors.get(entity_type, "black")
            html_text += text[last_idx:start]  # обычный текст
            html_text += f'<span style="color:{color}; font-weight:bold">{text[start:end]}</span>'
            last_idx = end
        except KeyError:
            continue  # игнорируем некорректные записи
    html_text += text[last_idx:]
    return html_text


def display_highlighted_text(text: str, ner_pipe: pipeline, colors: Dict[str, str] = None):
    """
    Выполняет NER на тексте и отображает результат с подсветкой.

    Параметры:
    - text: исходный текст.
    - ner_pipe: пайплайн NER.
    - colors: словарь цветов.
    """
    try:
        entities = ner_pipe(text)
        html_output = highlight_entities(text, entities, colors)
        display(HTML(html_output))
    except Exception as e:
        print(f"Ошибка при обработке текста: {e}")


# ===== Пример использования =====
if __name__ == "__main__":
    # Пример текста для визуализации
    example_text = """
    Alice and Bob traveled from New York to Paris last summer. 
    They visited the Louvre and met with representatives from UNESCO. 
    Later, they attended a concert by Coldplay at the Stade de France. 
    Alice said she loved the croissants, while Bob preferred the local cheese. 
    Their friend Charlie joined them for a short trip to Montmartre. 
    By the end of their journey, they promised to return next spring.
    """

    # Создаем пайплайн
    ner_pipeline = create_ner_pipeline()

    # Визуализируем текст
    display_highlighted_text(example_text, ner_pipeline)
    html_text = highlight_entities(text, entities, colors)
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html_text)
