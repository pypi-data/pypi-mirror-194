import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import random
import os
import spacy
from spacy import displacy

def clean_document(strs):
    strs = strs.replace('\\n', '').replace('\\r', '') # newline
    strs = re.sub('[^a-zA-Z]', ' ', strs) # punctuation
    strs = ' '.join(re.split('\s+', strs)) # duplicate whitespace
    strs = strs.lower().strip() # lowercase
    
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(strs)
    lemmatizer = WordNetLemmatizer()
    filtered = [lemmatizer.lemmatize(w) for w in word_tokens if w not in stop_words]
    
    return ' '.join(filtered)


def num_folders(rootdir):
    s = set()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir, file).split('/')
            s.add(path[1])

    return len(s)


def num_years(sentence):
    strs = sentence.split(' ')
    count = 0
    for s in strs:
        match = re.match(r'.*([1-2][0-9]{3})', s)
        if match is not None:
            count += 1
    
    return count

def replace_years(sentence):
    return ' '.join([re.sub(r'.*([1-2][0-9]{3})', 'YEAR', s) for s in sentence.split()])


def ner_count(passage):
    ner = spacy.load("en_core_web_sm")
    names = set()
    dates = []

    tags = ner(passage)
    for entity in tags.ents:
        text = entity.text
        label = entity.label_

        if label == 'PERSON':
            names.add(text)
        elif label == 'DATE':
            dates.append(text)
    return len(names), len(dates)


# Easy Data Augmentation implementation
class EDA:
    
    def __init__(self, alpha) -> None:
        self.alpha = alpha
        self.p = alpha
        self.stop_words = stopwords.words('english')

    def run_data_augmentation(self, passages):
        def find_synonyms(word):
            synonyms = []
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())
            
            return list(set(synonyms))

        def synonym_replacement(sentence):
            words = sentence.split()
            n = int(self.alpha * len(words))
            idxs = [i for i in range(len(words)) if words[i] not in self.stop_words]
            idxs = random.sample(idxs, n)
            for i in idxs:
                synonyms = find_synonyms(words[i])
                if len(synonyms) > 0:
                    words[i] = random.choice(synonyms)
            
            return " ".join(words)

        def random_insertion(sentence):
            words = sentence.split()
            n = int(self.alpha * len(words))
            idxs = [i for i in range(len(words)) if words[i] not in self.stop_words]
            for i in range(n):
                idx = random.choice(idxs)
                word = words[idx]
                synonyms = find_synonyms(words[i])
                synonym = random.choice(synonyms) if len(synonyms) > 0 else None
                if synonym is not None:
                    idx = random.choice(range(len(words)))
                    words.insert(idx, synonym)
            
            return " ".join(words)

        def random_swap(sentence):
            words = sentence.split()
            n = int(self.alpha * len(words))
            for i in range(n):
                a, b = random.sample(range(len(words)), 2)
                words[a], words[b] = words[b], words[a]
            
            return " ".join(words)

        def random_deletion(sentence):
            words = sentence.split()
            words[:] = [word for word in words if random.uniform(0, 1) > self.p]
            return " ".join(words)
        
        
        eda_passages = []
        for passage in passages:
            sentences = passage.split('.')
            new_passage = ""
            for sentence in sentences:
                f = random.randint(0, 3)
                if f == 0:
                    sentence = synonym_replacement(sentence)
                if f == 1:
                    sentence = random_insertion(sentence)
                if f == 2:
                    sentence = random_swap(sentence)
                if f == 3:
                    sentence = random_deletion(sentence)
                new_passage += sentence + ". "
            eda_passages.append(new_passage)
        return eda_passages
    