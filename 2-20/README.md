#!/bin/bash

# Имя файла
README_FILE="README.md"

# Содержимое README
cat > $README_FILE <<EOL
# NER Highlight Visualization

## Описание
Этот проект позволяет визуализировать результаты **Named Entity Recognition (NER)**, раскрашивая сущности в тексте в разные цвета в зависимости от их типа.  
Используется модель \`dslim/bert-base-NER\` от Hugging Face.

Пример:  
- PERSON — синий  
- LOCATION — красный  
- ORGANIZATION — зелёный  
- MISC — фиолетовый  

---

## Установка

1. Склонируйте репозиторий (если есть) или создайте проект локально.
2. Установите зависимости:

\`\`\`bash
pip install transformers torch ipython
\`\`\`

> Рекомендуется использовать Jupyter Notebook для визуализации HTML.

---

## Использование

1. Импортируйте необходимые библиотеки:

\`\`\`python
from transformers import pipeline
from IPython.display import display, HTML
\`\`\`

2. Создайте пайплайн NER:

\`\`\`python
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
\`\`\`

3. Определите текст для анализа:

\`\`\`python
text = "Barack Obama was born in Hawaii and worked at the White House."
entities = ner_pipeline(text)
\`\`\`

4. Определите цветовую карту для типов сущностей:

\`\`\`python
colors = {
    "PER": "blue",
    "LOC": "red",
    "ORG": "green",
    "MISC": "purple"
}
\`\`\`

5. Используйте функцию для визуализации:

\`\`\`python
def highlight_entities(text, entities):
    html_text = ""
    last_idx = 0
    for ent in entities:
        start, end = ent['start'], ent['end']
        entity_type = ent['entity_group']
        color = colors.get(entity_type, "black")
        html_text += text[last_idx:start]
        html_text += f'<span style="color:{color}; font-weight:bold">{text[start:end]}</span>'
        last_idx = end
    html_text += text[last_idx:]
    return html_text

html_output = highlight_entities(text, entities)
display(HTML(html_output))
\`\`\`

---

## Пример вывода

![Пример подсветки](example.png)  
*Barack Obama* — синий (PERSON), *Hawaii* — красный (LOC), *White House* — зелёный (ORG)

---

## Настройки

- Можно менять цвета сущностей в словаре \`colors\`.
- Любой текст можно подставлять вместо примера.
- Подходит для использования в Jupyter Notebook или сохранения в HTML файл.
EOL

echo "README.md успешно создан!"
