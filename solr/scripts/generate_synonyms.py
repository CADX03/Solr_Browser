import pandas as pd
import nltk
#from nltk import download
from nltk.corpus import wordnet

#"synonyms.txt"

def synonyms():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('wordnet')
    nltk.download('punkt_tab')
    nltk.download('omw-1.4')
    nltk.download('wordnet_ic')
    nltk.download('names')
    nltk.download('brown')
    nltk.download('gutenberg')

    file_path = f'./output.json'
    dataset = pd.read_json(file_path)
    #print(dataset)


    #all_texts = [review['text'] for reviews_list in dataset['reviews'] for review in reviews_list]
    all_texts = dataset['Description'].dropna().tolist()

    word_dict = {}
    words_checked = set()

    for desc in all_texts:
        if not isinstance(desc, str):
            continue

        words = nltk.word_tokenize(desc)
        nouns = [word.lower() for word, pos in nltk.pos_tag(words) if pos in ['NN', 'NNS'] and word.lower() not in words_checked]

        for noun in nouns:
            synonyms = []
            for syn in wordnet.synsets(noun):
                for lm in syn.lemmas():
                    if lm.name().lower() != noun:
                        synonyms.append(lm.name())
            if len(synonyms) > 1:
                word_dict[noun] = set(synonyms)
                words_checked.add(noun)

    with open("synonyms.txt", 'w') as f:
        for k, v in word_dict.items():
            matches = list(v - {k})
            list_synonyms = k + ", " + ", ".join(matches)
            f.write(list_synonyms + "\n")
        f.close()

if __name__ == '__main__':
        synonyms()