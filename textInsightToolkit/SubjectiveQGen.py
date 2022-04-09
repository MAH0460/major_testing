import nltk

class SubjectiveQGen:
    def __init__(self,textContent):
        #@nimesh_mishra Constructor for building questions
        self.question_templates = ['Justify ','Elaborate about ', 'Write in brief about ', 'What is ', 'What does ']
        self.noun_phrases = []
        self.grammarFormat = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                {<NN>+<IN|DT>*<NNP>+}
                {<NNP>+<NNS>*}
            """
        self.textContent = textContent
        self.parseTree = None
        self.loadEngines()
        self.extractNounPhrases()

    def loadEngines(self):
        chunker = nltk.RegexpParser(self.grammarFormat)
        tokens = nltk.word_tokenize(self.textContent)
        pos_tokens = nltk.tag.pos_tag(tokens)
        self.parseTree = chunker.parse(pos_tokens)

    def extractNounPhrases(self):
        # @ni: Traversing the tree and searching for the subtrees that represents CHUNK.
        # The tokens that form the CHUNK will be considered as a phrase and appended in a list.
        for subtree in self.parseTree.subtrees():
            if subtree.label() == "CHUNK":
                temp = ""
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                    self.noun_phrases.append(temp)

    def forkQuestions(self):
        subjQs = [f'{ques} {phrase}' for phrase in self.noun_phrases for ques in self.question_templates]
        print(self.noun_phrases)
        print(subjQs)
        return subjQs


def subQGenIntegrator(textContent):
    return SubjectiveQGen(textContent).forkQuestions()