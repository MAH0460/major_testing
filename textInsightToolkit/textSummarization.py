# Developed By : Aashutosh Solanki
# Importing the libraries
import re
from string import punctuation, digits
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import stdin

# Data cleanup
punctuation = punctuation + "\n" + digits
stop_words = ['me', 'my', 'myself', 'ours', 'ourselves', "you're", "you've", "you'll", "you'd", 'your', 'yours',
              'yourself', 'yourselves', 'him', 'his', 'himself', "she's", 'her', 'hers', 'herself', "it's", 'its',
              'itself', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
              "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
              'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'and', 'but', 'if', 'or', 'because', 'as',
              'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
              'during', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
              'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
              'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
              'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",
              'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
              "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
              'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
              "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "essay", "login",
              "signup", "register"]


# Creating the frequency table
def text_cleanup(text):
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()

    tokens = word_tokenize(text)
    word_frequency = {}
    for word in tokens:
        word = word.lower()
        word = ps.stem(word)
        if word not in stop_words:
            if word not in punctuation:
                if word not in word_frequency.keys():
                    word_frequency[word] = 1
                else:
                    word_frequency[word] += 1
    return word_frequency


# Weighting the frequency table
def weighted_table(word_frequency):
    max_frequency = max(word_frequency.values())

    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word] / max_frequency

    return word_frequency


# separating text into sentences
def tokenize_into_sentence(text):
    return sent_tokenize(text)


# Assigning weight to the sentences
def check_topic_in_sentence(keywords, sentence):
    for i in keywords:
        if i.lower() in sentence.lower():
            return True
    return False


# Getting the important keywords from the text
def get_important_keywords(text):
    from textInsightToolkit.keyword_extract_tfidf import tagIntegrator
    keywords = tagIntegrator(text)
    if "essay" in keywords:
        keywords.remove("essay")
    return keywords


# Weighting the sentences
def weighting_sentences(sentences, frequency_table, keywords):
    sentences_weight = {}

    # Assigning the sequences and weight to the sentences
    for sentence in enumerate(sentences):
        sentence_weight = 0
        for word in frequency_table.keys():
            sentence_weight = sentence_weight + \
                (frequency_table[word] * sentence[1].count(word))
        sentences_weight[sentence] = sentence_weight
        if check_topic_in_sentence(keywords, sentence[1]):
            sentences_weight[sentence] += 0.08
    return sentences_weight


# Getting the current length of generating summary
def length(summary):
    length = 0
    for i in summary:
        length += len(i[1].split())
    return length

# Summary creation


def summarizer(weighted_sentences, leng=0):
    summary = []

    # Sorting the sentences according to the weight
    sorted_sentences = sorted(
        weighted_sentences.items(), key=lambda kv: (kv[1], kv[0]))
    sorted_sentences = sorted_sentences[::-1]
    # print(sorted_sentences)
    flag = True
    while flag:
        if length(summary) < leng:
            try:
                if "essay" not in sorted_sentences[0][0][1].lower():
                    summary.append(sorted_sentences[0][0])
                sorted_sentences = sorted_sentences[1:]
            except:
                flag = False
                pass
        else:
            flag = False

    # Sequencing the summary
    summary.sort(key=lambda x: x[0])
    summary = " ".join([re.sub('\\[[0-9]+\\]', "", string=i[1])
                       for i in summary])
    return summary, len(summary.split())


def parasummary(text):
    keywords = get_important_keywords(str(text))
    print("The length of the text is : ", len(text.split()))
    if len(text.split()) == 0:
        print("Unable to detect text. Exiting the program.")
    else:
        length = 200
        word_frequency_table = text_cleanup(text)
        weighted_word_frequency = weighted_table(word_frequency_table)
        tokenized_sentences = tokenize_into_sentence(text)
        weighted = weighting_sentences(
            tokenized_sentences, weighted_word_frequency, keywords)
        summary, length_of_summary = summarizer(weighted, length)
        summary = sent_tokenize(summary)
        return summary
        # print("The length of summary is ", length_of_summary)


def page_wise_summary():
    text = read_from_pdf()
    text = re.sub('\\[[0-9]+\\]', "", string=text)
    keywords = get_important_keywords(str(text))
    total_words = 0
    for i in text:
        total_words += len(i)
    print("Total words in chapter: ", total_words)
    summary = ""
    length_of_text = len(text)
    for i in range(length_of_text):
        word_frequency_table = text_cleanup(text[i])
        weighted_word_frequency = weighted_table(word_frequency_table)
        tokenized_sentences = tokenize_into_sentence(text[i])
        weighted = weighting_sentences(
            tokenized_sentences, weighted_word_frequency, keywords)
        short_summary, _ = summarizer(weighted, 50)
        summary += short_summary
    return summary, len(summary.split())


def read_from_pdf():
    print("Reading PDF please wait")
    try:
        import pdfplumber
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename
        root = Tk()
        path = askopenfilename(title="Select pdf file")
        path = path.replace("/", "\\\\")
        text = []
        with pdfplumber.open(path) as pdf:
            i = 0
            while True:
                try:
                    print("Reading page : ", i + 1)
                    page = pdf.pages[i]
                    newText = page.extract_text()
                    text = re.sub('\\[[0-9]+\\]', "", string=text)
                    text.append(newText)
                    i += 1
                except Exception as e:
                    print(e)
                    break
            pdf.close()

        if len(text) == 0:
            raise TypeError("Unable to read the text")
        return text
    except NotADirectoryError:
        print("Please select a file")
        return ""
    except TypeError:
        print("Unable to read the text")
        return ""
    except Exception as e:
        print("Some error occured: ", e)
        return ""
    finally:
        root.destroy()


# def download_pdf(summary):
#     from fpdf import FPDF
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("arial", size=10)
#     pdf.cell(200, 10, txt=summary, align="L", ln=1)
#     pdf.output("Outputpdf.pdf")
#     print("Pdf generated")


def save_text_file(summary):
    f = open("summaryoutput.txt", "w", encoding="utf-8")
    f.write(summary)


def summaryIntegrator(text, expansion):
    vital_keywords = get_important_keywords(str(text))
    totalWords = len(text.split())
    print("The length of the text is : ", totalWords)
    if totalWords == 0:
        return "Text is empty!"
    else:
        length = (totalWords * int(expansion))//100
        word_frequency_table = text_cleanup(text)
        weighted_word_frequency = weighted_table(word_frequency_table)
        tokenized_sentences = tokenize_into_sentence(text)
        weighted = weighting_sentences(
            tokenized_sentences, weighted_word_frequency, vital_keywords)
        summary, length_of_summary = summarizer(weighted, length)
        summary = sent_tokenize(summary)
        print(*summary, sep="\n\n")
        print("The length of summary is ", length_of_summary)
        return summary


def main():
    choice = int(
        input("Enter 1 or 2: 1 for manually entering text and 2 for reading from pdf"))
    if choice == 1:
        text = input("Enter the text")
        summary = parasummary(text)
        print(*summary, sep="\n\n")
    else:
        summary, length = page_wise_summary()
        print(summary)
        print(length)
        save_text_file(summary)


# Main
if __name__ == '__main__':
    main()

# %%
