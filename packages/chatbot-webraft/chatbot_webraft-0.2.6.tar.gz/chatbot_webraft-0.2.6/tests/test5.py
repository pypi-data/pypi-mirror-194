import random
from chatbot_webraft import chatbot
#Import library


#set model name
model = "my-model"

#create modelsample2.csv
chatbot.create_model(model)

#load CSV dataset , Mention input column (question) and label column (answer)
chatbot.dataset("sample.csv","context","response",model)


#run in loop

# Define a function to rephrase a sentence using synonyms
def bert(word,model,words_list1,words_list2):
    from sentence_transformers import SentenceTransformer, util

    # Load the pre-trained BERT model
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    # Define your sentences
    sentences = words_list1

    # Encode the sentences into sentence embeddings
    sentence_embeddings = model.encode(sentences)

    # Define your user input
    user_input = word

    # Encode the user input into a sentence embedding
    user_embedding = model.encode(user_input)

    # Calculate the cosine similarity between the user input embedding and the sentence embeddings
    similarity_scores = util.pytorch_cos_sim(user_embedding, sentence_embeddings)

    # Find the index of the most similar sentence
    most_similar_sentence_index = similarity_scores.argmax().item()

    # Print the index of the most similar sentence
    return words_list2[most_similar_sentence_index]

def rephrase_sentence(sentence, synonyms):
    # Split the sentence into words
    words = sentence.split()

    # Loop through each word in the sentence
    new_words = []
    for word in words:
        # If the word has a synonym in the dictionary, replace it with a random synonym from the selected list
        if word in synonyms:
            synonym_list = synonyms[word]
            new_word = random.choice(synonym_list)
        # Otherwise, keep the original word
        else:
            new_word = word
        new_words.append(new_word)

    # Join the new words into a rephrased sentence
    return ' '.join(new_words)

# Define lists of custom synonyms for each word
happy_synonyms = ['glad', 'joyful', 'elated']
angry_synonyms = ['upset', 'mad', 'irate']
run_synonyms = ['jog', 'sprint', 'dash']
big_synonyms = ['large', 'huge', 'enormous']
small_synonyms = ['tiny', 'micro', 'microscopic']
hot_synonyms = ['warm', 'toasty', 'boiling']
good_synonyms = ['great', 'excellent', 'superb']
bad_synonyms = ['terrible', 'awful', 'dreadful']
beautiful_synonyms = ['gorgeous', 'stunning', 'elegant']

# Combine the synonym lists into a dictionary
synonyms = {
    'happy': happy_synonyms,
    'angry': angry_synonyms,
    'run': run_synonyms,
    'big': big_synonyms,
    'small': small_synonyms,
    'hot': hot_synonyms,
    'good': good_synonyms,
    'bad': bad_synonyms,
    'beautiful': beautiful_synonyms
}

while True:
    # Get input from the user
    prompt = input("You: ")
    x = chatbot.model_load("bert", prompt, model)
    # Rephrase the input sentence using the selected synonyms
    output = rephrase_sentence(x, synonyms)

    # Print the rephrased output
    print("UNI-BOT: " + output)
