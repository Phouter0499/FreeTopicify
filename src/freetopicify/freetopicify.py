import re
import spacy
from .basic_wikimedia_api_wrapper import *
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
    nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN" and re.search(r"\w", token.lemma_)]
    # local frequency vs global frequency
    # basically I want specialized vocabulary thats used a lot and exclude general nouns
    calculate_weight = lambda x: nouns.count(x)/max(zipf_frequency(x, 'en'), 0.001)
    nouns_glf = sorted(nouns, key=calculate_weight, reverse=True)
    return nouns_glf

def get_OMDF_topics(input, limit=15, depth_mode=True):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(input)
    # MAKE QUERY OPERANDS
    entities = get_topics_ner(doc)
    nouns = get_topics_nouns(doc)
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
    # SEND QUERY AND PROCESS QUERY RESULTS
    search_results = search_content(query, limit)
    if depth_mode:
        tree = []
        for search_result in search_results:
            head = f"[[{search_result['title']}]]"
            key = search_result['key']
            html = get_html(key)
            link_texts = get_link_texts(html)
            branches = [f"[[{link_text}]]" for link_text in link_texts]
            tree.append((head, branches))
        return tree
    else:
        return [f"[[{r['title']}]]" for r in search_results]

if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()
    with open("output.txt", "w", encoding="utf-8") as f:
        for head, branches in get_OMDF_topics(text, 5):
            f.write(f"{head}\n")
            f.write(", ".join(branches))
            f.write("\n\n")