# Установка библиотек, если нужно
# pip install transformers torch ipython

from transformers import pipeline
from IPython.display import display, HTML

# 1. Текст для анализа
text = """
Alice and Bob traveled from New York to Paris last summer. 
They visited the Louvre and met with representatives from UNESCO. 
Later, they attended a concert by Coldplay at the Stade de France. 
Alice said she loved the croissants, while Bob preferred the local cheese. 
Their friend Charlie joined them for a short trip to Montmartre. 
By the end of their journey, they promised to return next spring.
"""

# текст на подумать 

text2 = """
– Hey, uncle, what time is it?
– Nineteen, five to.
– Are those boilers some kind of general’s gear or what?
– Well, I’m a general.
– Really? What, you don’t believe me? Honest.
– Dude, those boilers aren’t your style. Take them off.
– You gonna lend me a smoke?
– Swap?
– Swap.
– I give you a cigarette. You give me the boilers.
"""

# 2. Создание пайплайна NER с новой стратегией агрегации
ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"  # заменяет grouped_entities=True
)

# 3. Получение сущностей
entities = ner_pipeline(text)

# 4. Цвета для типов сущностей
colors = {
    "PER": "blue",      # PERSON
    "LOC": "red",       # LOCATION
    "ORG": "green",     # ORGANIZATION
    "MISC": "purple"    # Miscellaneous
}

# 5. Функция для подсветки текста
def highlight_entities(text, entities):
    html_text = ""
    last_idx = 0
    for ent in entities:
        start, end = ent['start'], ent['end']
        color = colors.get(ent['entity_group'], "black")
        html_text += text[last_idx:start]
        html_text += f'<span style="color:{color}; font-weight:bold">{text[start:end]}</span>'
        last_idx = end
    html_text += text[last_idx:]
    return html_text

# 6. Отображение результата в Jupyter
display(HTML(highlight_entities(text, entities)))

html_text = highlight_entities(text, entities)

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_text)

print("HTML с подсветкой сохранён в output.html")
