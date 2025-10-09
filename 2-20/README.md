# NER Highlighter

## Описание
Модуль для распознавания именованных сущностей (NER) в тексте и визуализации их с подсветкой цветов.  
Позволяет как отображать результат в Jupyter Notebook, так и сохранять в HTML-файл.

Пример типов сущностей и цветов по умолчанию:  
- PERSON (`PER`) — синий  
- LOCATION (`LOC`) — красный  
- ORGANIZATION (`ORG`) — зелёный  
- MISC (`MISC`) — фиолетовый  

---

## Установка

```bash
pip install transformers torch ipython
Рекомендуется использовать Jupyter Notebook для отображения HTML с подсветкой, но модуль работает и в стандартном Python.

Использование
python
Копировать код
from ner_highlighter import create_ner_pipeline, display_highlighted_text, save_highlighted_html

# Создаём пайплайн NER
ner_pipeline = create_ner_pipeline()

# Текст для анализа
text = """
Alice and Bob traveled from New York to Paris last summer. 
They visited the Louvre and met with representatives from UNESCO.
"""

# Отображаем подсветку в Jupyter
display_highlighted_text(text, ner_pipeline)

# Сохраняем результат в HTML
save_highlighted_html(text, ner_pipeline, "output.html")
Функции модуля
create_ner_pipeline(model_name: str = "dslim/bert-base-NER") -> pipeline
Создает предобученный пайплайн HuggingFace для NER.

Параметры:

model_name: название модели HuggingFace (по умолчанию "dslim/bert-base-NER")

Возвращает:

pipeline для выполнения NER

highlight_entities(text: str, entities: List[Dict], colors: Dict[str, str] = None) -> str
Подсвечивает сущности в тексте HTML-тегами.

Параметры:

text: исходный текст

entities: список сущностей, полученных из NER пайплайна

colors: словарь цветов для каждого типа сущности (по умолчанию:

python
Копировать код
{
    "PER": "blue",
    "LOC": "red",
    "ORG": "green",
    "MISC": "purple"
}
```)  
Возвращает:

HTML-строку с подсветкой сущностей

display_highlighted_text(text: str, ner_pipe: pipeline, colors: Dict[str, str] = None)
Выполняет NER на тексте и отображает результат с подсветкой в Jupyter Notebook.

Параметры:

text: текст для анализа

ner_pipe: пайплайн NER

colors: словарь цветов для типов сущностей

save_highlighted_html(text: str, ner_pipe: pipeline, file_path: str, colors: Dict[str, str] = None)
Выполняет NER и сохраняет результат в HTML-файл.

Параметры:

text: текст для анализа

ner_pipe: пайплайн NER

file_path: путь для сохранения HTML-файла

colors: словарь цветов для типов сущностей

Пример использования:

python
Копировать код
save_highlighted_html(text, ner_pipeline, "output.html")
Настройки
Цвета можно менять через словарь colors.

Можно использовать любую предобученную модель HuggingFace.

Подходит для любых английских текстов.

Пример визуализации
После выполнения кода в Jupyter Notebook текст будет подсвечен цветами по типу сущностей:

Alice, Bob → PERSON (синий)

New York, Paris → LOC (красный)

Louvre, UNESCO → ORG (зелёный)

Coldplay → MISC (фиолетовый)
