class BigramFinder:
    def __init__(self, text):
        self.text = text

    def bigram_finder(self):
        from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
        from nltk.corpus import stopwords

        stopwords_ = set(stopwords.words('english'))
        new_words = ["using", "show", "result", "large", "also",
                     "iv", "one", "two", "new", "previously", "shown", "essay", "essays", "login", "signup", "topic", "search"]
        self.stopwords_ = stopwords_.union(new_words)
        words = [word.lower() for word in self.text.split()
                 if len(word) > 2
                 and word not in self.stopwords_]
        finder = BigramCollocationFinder.from_words(words)
        bgm = BigramAssocMeasures()
        self.score = bgm.mi_like
        self.collocations = {
            '_'.join(bigram): pmi for bigram, pmi in finder.score_ngrams(self.score)}
        # print(self.collocations)
        values = list(self.collocations.items())
        # print(values)
        values = values[:5] + values[-5:]
        values = [i[0] for i in values]
        return values


if __name__ == '__main__':
    text = input("Enter the text")
    bf = BigramFinder(text)
    print(bf.bigram_finder())

# %%
