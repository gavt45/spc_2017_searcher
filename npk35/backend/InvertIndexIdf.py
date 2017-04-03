import os
import re
import pymorphy2
from math import log
from sklearn.feature_extraction.text import CountVectorizer

morph = pymorphy2.MorphAnalyzer()


def lemmatize(token):
    try:
        gram_info = morph.parse(token)
        return gram_info[0].normal_form
    except:
        return token


def clean(text):
    # заменяем все знаки препинания, кроме дефиса, на пробелы
    text = re.sub('[!"#$%&\'()*+,\../:;<=>?@[\\]^_`{|}~«–»—№<>]+', ' ', text)
    words = text.lower().split()
    # лемматизируем, выкидывая всё, что является числом и чья длина 2 или меньше
    tokens = [lemmatize(w) for w in words if len(w) > 2 and not w.isdigit() and not w.split('-')[0].isdigit()]
    return tokens


def process_files(path):
    file2words = {}  # создаем пустой словарь
    for file in os.listdir(path):
        fileName = path + file
        with open(fileName, encoding='utf-8') as f:  # открываем;
            words = clean(f.read())
            file2words[fileName] = words
    return file2words


file2words = process_files('C:\\файлы1\\')

clean_docs = [' '.join(words) for words in file2words.values()]
filenames = list(file2words.keys())


def index_one_file(words):
    fileIndex = {}
    for index, word in enumerate(words):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]
    return fileIndex


def make_index(file2words):
    index = {}
    for filename in file2words.keys():
        index[filename] = index_one_file(file2words[filename])
    return index


index = make_index(file2words)


def make_invertedIndex(index):
    invertedIndex, df = {}, {}

    for filename in index.keys():
        for word in index[filename].keys():
            if word in df.keys():
                df[word] += 1
            else:
                df[word] = 1
            if word in invertedIndex.keys():
                if filename in invertedIndex[word].keys():
                    invertedIndex[word][filename].extend(index[filename][word][:])
                else:
                    invertedIndex[word][filename] = index[filename][word]
            else:
                invertedIndex[word] = {filename: index[filename][word]}

    N = len(filenames)
    idf = {word: log(N / df[word]) for word in df}

    return invertedIndex, idf


invertedIndex, idf = make_invertedIndex(index)
# print (invertedIndex)
# print (idf)
import json

# у нас два словаря - invertedIndex, idf, чтобы не создавать два файла, сложим их все в один массив
data = [invertedIndex, idf, file2words]
with open('C:\\Users\Julia\index_idf_file2words.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
