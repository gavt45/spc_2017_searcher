# coding: utf-8
import re, json, pymorphy2
from sklearn.feature_extraction.text import CountVectorizer


class search():
    morph = pymorphy2.MorphAnalyzer()
    vectorizer = CountVectorizer()
    jsonFile = None
    defaultPath = None

    def __init__(self, jsonFile, defaultpath):
        print("Using searcher; json file is: " + jsonFile + " & default path is: " + defaultpath)
        self.jsonFile = jsonFile
        self.defaultPath = defaultpath

    def lemmatize(self, token):
        try:
            gram_info = self.morph.parse(token)
            return gram_info[0].normal_form
        except:
            return token

    def clean(self, text):
        text = re.sub('[!"#$%&\'()*+,\../:;<=>?@[\\]^_`{|}~«–»—№<>]+', ' ', text)
        words = text.lower().split()
        tokens = [self.lemmatize(w) for w in words if len(w) > 2 and not w.isdigit() and not w.split('-')[0].isdigit()]
        return tokens

    def get_documents(self, query, invertedIndex):
        query = ' '.join(self.clean(query))
        if len(query.split()) == 1:
            if query in invertedIndex.keys():
                return [filename for filename in invertedIndex[query].keys()]
            else:
                return []
        else:
            result = []
            for word in query.split():
                if word in invertedIndex.keys():
                    result.append([filename for filename in invertedIndex[word].keys()])
            return list(set(result[0]).intersection(*result))

    def main(self, query):
        if query == '':
            return []
        with open(self.defaultPath + self.jsonFile) as f:
            invertedIndex, idf, file2words = json.load(f)

        docs = self.get_documents(query, invertedIndex)
        clean_docs = [' '.join(file2words[doc]) for doc in docs]

        raw_v = self.vectorizer.fit_transform(clean_docs)
        raw_vectors = raw_v.toarray()
        raw_vectors = [list(v) for v in raw_vectors]
        vectors = dict(zip(docs, raw_vectors))
        vocab = self.vectorizer.get_feature_names()

        idf_vectors = {}
        for doc in vectors:
            idf_vectors[doc] = [tf * idf[vocab[i]] for i, tf in enumerate(vectors[doc])]

        query_vector = self.vectorizer.transform([query]).toarray()
        query_vector = list(query_vector[0])

        cos_sim = {}
        for doc in docs:
            cos_sim[doc] = sum([x * y for x, y in zip(idf_vectors[doc], query_vector)])

        ranked_docs = sorted(cos_sim, key=lambda x: x[1])  # [::-1]

        return ranked_docs
