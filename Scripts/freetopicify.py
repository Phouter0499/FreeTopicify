import re
import spacy
from BasicWikimediaAPI import *
from wordfreq import zipf_frequency
from collections import Counter

def get_topics_ner(doc):
    # USE NER TO GET THE MOST IMPORTANT IDEAS
    entities = []
    for ent in doc.ents:
        # exclude any with these labels. side note: look at ent label scheme for en_core_web_lg
        if any(x == ent.label_ for x in ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']):
            continue
        else:
            entities.append(ent.text)
    entities = sorted(Counter(entities).items(), key=lambda x: x[1], reverse=True)
    return entities

def get_topics_nouns(doc):
    # USE NOUNS TO GET THE MOST IMPORTANT IDEAS
    nouns = list({token.lemma_ for token in doc if token.pos_ == "NOUN" and re.search(r"\w", token.lemma_)})
    nouns = sorted(nouns, key=lambda x: zipf_frequency(x, 'en'), reverse=False)
    return nouns

with open("essay.txt", "r", encoding="utf-8") as f:
    essay = f.read()
nlp = spacy.load("en_core_web_lg")
doc = nlp(essay)

entities = get_topics_ner(doc)
nouns = get_topics_nouns(doc)

# MAKE QUERY OPERANDS
operands = []
for ent in entities:
    operands.append(ent[0])
for noun in nouns:
    if noun.lower() in {o.lower() for o in operands}:
        continue
    operands.append(noun)
# MAKE QUERY
query = ""
for operand in operands:
    if " " in operand:
        temp_query = f'{query} OR "{operand}"' if query else operand
    else:
        temp_query = f"{query} OR {operand}" if query else operand
    if len(temp_query) <= 300:
        query = temp_query
    else:
        break
search_results = search_content(query, 15)
main_nodes = []
for search_result in search_results:
    main_nodes.append((search_result['title'], search_result['description'], search_result['key']))
with open(r"output.txt", "w", encoding="utf-8") as f:
    print(query)
    for main_node in main_nodes:        
        if main_node[1]:
            f.write(f"[[{main_node[0]}]]: {main_node[1]}\n")
        else:
            f.write(f"[[{main_node[0]}]]\n")
        html = get_html(main_node[2])
        link_texts = get_link_texts(html)
        body = ", ".join([f"[[{link_text}]]" for link_text in link_texts])
        f.write(f"{body}\n\n")