import os, re, pymorphy2, json
from math import log
from .search import lemmatize

class indexer():
    default_path = None
    json_name = None

    def __init__(self, default_path, json_name):
        print("Using indexer default path is "+default_path+"; json name is "+json_name)
        self.default_path=default_path
        self.json_name=json_name

    def lemmatize(self, token):
        try:
            morph = pymorphy2.MorphAnalyzer()
            gram_info = morph.parse(token)
            return gram_info[0].normal_form
        except:
            return token

    def clean(self, text):
        # заменяем все знаки препинания, кроме дефиса, на пробелы
        text = re.sub('[!"#$%&\'()*+,\../:;<=>?@[\\]^_`{|}~«–»—№<>]+', ' ', text)
        words = text.lower().split()
        # лемматизируем, выкидывая всё, что является числом и чья длина 2 или меньше
        tokens = [lemmatize(w) for w in words if len(w) > 2 and not w.isdigit() and not w.split('-')[0].isdigit()]
        return tokens

    def process_files(self, path):
        file2words = {}  # создаем пустой словарь
        for file in os.listdir(path):
            fileName = path + file
            with open(fileName, encoding='utf-8') as f:    # открываем;
                words = self.clean(f.read())
                file2words[fileName] = words
        return file2words

    def index_one_file(self, words):
        fileIndex = {}
        for index, word in enumerate(words):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
        return fileIndex

    def make_index(self, file2words):
        index = {}
        for filename in file2words.keys():
            index[filename] = self.index_one_file(file2words[filename])
        return index

    def make_invertedIndex(self, index, filenames):
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
        return invertedIndex,idf

    def Main(self):
        file2words = self.process_files(self.default_path + 'files')
        clean_docs = [' '.join(words) for words in file2words.values()]
        filenames = list(file2words.keys())
        index = self.make_index(file2words)
        invertedIndex, idf = self.make_invertedIndex(index, filenames)
        print("inverted index is: "+str(invertedIndex))
        print("idf is: "+str(idf))
        # у нас два словаря - invertedIndex, idf, чтобы не создавать два файла, сложим их все в один массив
        data = [invertedIndex, idf, file2words]
        with open(self.default_path+self.json_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
