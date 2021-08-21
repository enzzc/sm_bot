import random
import spacy
import copy
nlp = spacy.load("fr_core_news_sm")
print('Dataset "fr_core_news_sm" has been loaded.')


def replace_by_random_token(base_sentence, token, pick_tokens):
    try:
        return base_sentence.replace(
            token,
            f' {pick_tokens.pop()} ',
            1
        )
    except IndexError:
        pass
    return base_sentence


def shuffle_objects(base_sentence, pick_sentence):
    pick_nsubj = set()
    pick_nmod = set()
    pick_obj = set()

    initial_sentence = copy.copy(base_sentence)

    for token in nlp(pick_sentence).noun_chunks:
        if token.root.dep_ == 'nsubj':
            pick_nsubj.add(token.text)
        elif token.root.dep_ == 'nmod':
            pick_nmod.add(token.text)
        elif token.root.dep_ == 'obj':
            pick_obj.add(token.text)

    pick_nsubj = list(pick_nsubj)
    pick_nmod = list(pick_nmod)
    pick_obj = list(pick_obj)
    random.shuffle(pick_nsubj)
    random.shuffle(pick_nmod)
    random.shuffle(pick_obj)

    for token in nlp(base_sentence).noun_chunks:
        if token.root.dep_ == 'nsubj':
            base_sentence = replace_by_random_token(
                base_sentence,
                token.text,
                pick_nsubj
            )
        if token.root.dep_ == 'nmod':
            base_sentence = replace_by_random_token(
                base_sentence,
                token.text,
                pick_nmod
            )
        if token.root.dep_ == 'obj':
            base_sentence = replace_by_random_token(
                base_sentence,
                token.text,
                pick_obj
            )

    if initial_sentence != base_sentence:
        return base_sentence


def make_sentence(s1, s2):
    if random.randint(0, 1):  # Randomly permute s1 and s2
        s1, s2 = s2, s1

    sentence = shuffle_objects(s1, s2)
    # Try the other combination if the previous one has failed.
    if sentence is None:
        sentence = shuffle_objects(s2, s1)

    if sentence is not None:
        sentence = ' '.join(sentence.split())
        return sentence
