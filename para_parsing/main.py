import os
from para_parsing.file_parser import Parser
import nltk
nltk.data.path.append(os.path.abspath(os.path.curdir))

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


class QAMapper:
    def __init__(self, paragraph_file_name):
        self.parser = Parser(paragraph_file_name)

    def tokenize_questions(self):
        word_tokenize_questions = [nltk.word_tokenize(q) for q in self.parser.questions]
        self.token_questions = [nltk.pos_tag(q) for q in word_tokenize_questions]

    def tokenize_sentences(self):
        word_tokenize_sentences = [nltk.word_tokenize(s) for s in self.parser.answer_sentences]
        self.token_sentences = [nltk.pos_tag(s) for s in word_tokenize_sentences]

    def find_answers(self):
        # Tokenize questions and sentences from paragraph to find similarity
        self.tokenize_questions()
        self.tokenize_sentences()
        self.qa_mapper = {}
        for i in range(len(self.token_questions)):
            q = self.token_questions[i]
            original_question = self.parser.questions[i]
            max_similarity = 0
            for j in range(len(self.token_sentences)):
                s = self.token_sentences[j]
                original_sentence = self.parser.answer_sentences[j]
                similarity = 0
                for w in q:
                    if w in s:
                        similarity = similarity + 1

                # Question matching max similarity with sentence will contain answer to it
                if similarity >= max_similarity:
                    self.qa_mapper[original_question] = (original_sentence, self.parser.get_answer_from_sentence(original_sentence))
                    max_similarity = similarity

        for q in self.qa_mapper:
            s,a = self.qa_mapper[q]
            print("Answer to Question %s is: %s" % (q,a))



if __name__ == '__main__':
    paragraph_file_name = "para"
    paragraph_file_name = "sachin_tendulkar_test_para"
    mapper = QAMapper(paragraph_file_name)
    mapper.find_answers()