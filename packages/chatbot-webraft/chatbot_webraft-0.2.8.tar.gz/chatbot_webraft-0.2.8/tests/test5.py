import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from random import choice
from difflib import SequenceMatcher

# Define initial lists of words
noun_phrases = ["the cat", "the dog", "the bird", "the tree"]
verbs = ["is", "looks", "seems", "goes", "works", "hacks", "lags", "watches", "sexy"]
adjectives = ["happy", "sad", "angry", "excited", "busy", "creative", "beautiful"]
adverbs = ["very", "quite", "extremely", "much", "very much", "confidently", "gracefully"]

# Define a similarity threshold for generated sentences
similarity_threshold = 1

# Get input from user and split it into words
user_input = input("Enter a sentence: ")
user_words = word_tokenize(user_input.lower())

# Append user words to appropriate lists
for word in user_words:
    if word in noun_phrases:
        continue
    elif word in verbs:
        continue
    elif word in adjectives:
        continue
    elif word in adverbs:
        continue
    else:
        pos_tag = nltk.pos_tag([word])[0][1]
        if pos_tag.startswith("NN"):
            noun_phrases.append(word)
        elif pos_tag.startswith("VB"):
            verbs.append(word)
        elif pos_tag.startswith("JJ"):
            adjectives.append(word)
        elif pos_tag.startswith("RB"):
            adverbs.append(word)

# Generate sentences until one is similar enough to the user input
generated_sentence = ""
while True:
    sentence_structure = choice([1, 2, 3])
    if sentence_structure == 1:
        np = choice(noun_phrases)
        v = choice(verbs)
        adj = choice(adjectives)
        generated_sentence = f"{np} {v} {adj}."
        pos_tags = nltk.pos_tag(word_tokenize(generated_sentence))
        if pos_tags[-1][1].startswith("NN"):
            noun_phrases.append(pos_tags[-1][0])
            generated_sentence = f"{np} {v} {adj} {pos_tags[-1][0]}."
    elif sentence_structure == 2:
        np1 = choice(noun_phrases)
        np2 = choice(noun_phrases)
        v = choice(verbs)
        generated_sentence = f"{np1} {v} like {np2}."
        pos_tags = nltk.pos_tag(word_tokenize(generated_sentence))
        if pos_tags[-1][1].startswith("NN"):
            noun_phrases.append(pos_tags[-1][0])
            generated_sentence = f"{np1} {v} like {np2} {pos_tags[-1][0]}."
    else:
        adj = choice(adjectives)
        adv = choice(adverbs)
        v = choice(verbs)
        generated_sentence = f"It {v} {adv} {adj}."
        pos_tags = nltk.pos_tag(word_tokenize(generated_sentence))
        if pos_tags[-1][1].startswith("NN"):
            noun_phrases.append(pos_tags[-1][0])

    # Calculate similarity between generated sentence and user input
    similarity_ratio = SequenceMatcher(None, user_input, generated_sentence).ratio()
    print(similarity_ratio)
    if similarity_ratio >= similarity_threshold:
        print(generated_sentence)
        break
