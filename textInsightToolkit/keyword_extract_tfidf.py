# %%
# @ashutosh_solanki
from string import punctuation
#from matplotlib.pyplot import text
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Data cleanup
punctuation = punctuation + "\n"
stop_words = stopwords.words("english")

# Creating the frequency table


def text_cleanup(text):
    # ps = PorterStemmer()
    tokens = word_tokenize(text)
    cleaned_text = ""
    for word in tokens:
        word = word.lower()
        # word = ps.stem(word)
        if word not in stop_words and word not in punctuation:
            # word = lemm.lemmatize(word)
            cleaned_text += word + " "
    return cleaned_text


def sortcoo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_top_v(feature_names, sorted_items, topn=10):
    # use only topn items from vector
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
    # create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def vectorization(data, stopwords):
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    cv = CountVectorizer(stop_words=stopwords)
    wcv = cv.fit_transform([data])
    # print(list(cv.vocabulary_.keys())[:10])
    tfidft = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidft.fit(wcv)
    feature_name = cv.get_feature_names()
    tfidfv = tfidft.transform(cv.transform([data]))
    sorted_item = sortcoo(tfidfv.tocoo())
    top10 = extract_top_v(feature_name, sorted_item, 10)
    # print(data)
    lst = []
    for k in top10:
        if k not in stopwords:
            lst.append(k)
    return lst


def getBigrams(text):
    from textInsightToolkit.keyword_extract_nltk_bigrams import BigramFinder
    BF = BigramFinder(text)
    return BF.bigram_finder()


def tagIntegrator(data):
    lst = vectorization(text_cleanup(data), stop_words)
    bigram_list = getBigrams(data)
    return lst + bigram_list


if __name__ == '__main__':
    print(tagIntegrator(input()))
# %%
