import nltk
# Parser assumes below
# Line 1 contains all the paragraph sentences
# All lines after it except last one contains Questions
# Last line contains all answers separated by ';'
class Parser:
    def __init__(self, paragraph_file_name):
        try:
            self.input = open(paragraph_file_name, "r").readlines()
            self.parse_paragraph()
            self.parse_questions()
            self.parse_answers()
            self.get_para_lines_with_answers()
        except FileExistsError as e:
            print("Please add file name %s in current directory or change path" % paragraph_file_name)
            raise e
        except PermissionError as e:
            print("Unable to read file please check permissions")
            raise e

    def parse_paragraph(self):
        self.para = self.input[0]
        return self.para

    def parse_questions(self):
        self.questions = self.input[1:-1]
        self.questions = [q.strip().lower() for q in self.questions]
        return self.questions

    def parse_answers(self):
        self.answers = self.input[-1:][0].split(";")
        self.answers = [a.strip().lower() for a in self.answers]
        if len(self.answers) != len(self.questions):
            raise Exception("Input Mismatch: Number of Questions and Answers don't match")
        return self.answers

    def get_para_lines_with_answers(self):
        self.all_sentences = [s.replace("\n", " ").strip().lower() for s in nltk.sent_tokenize(self.para)]
        self.answer_sentences = []
        self.sentence_answer_mapping = {}

        for s in self.all_sentences:
            # Instead of tokenizing answers and sentences as answers are substrings of sentences
            # we are matching with length of answers to reduce ambiguity
            # This will still fail if answer of question from sentence has more than one similar length answers
            max_l = 0
            for a in self.answers:
                if a in s and len(a) > max_l:
                    max_l = len(a)
                    self.answer_sentences.append(s)
                    self.sentence_answer_mapping[s] = a

    def get_answer_from_sentence(self, sentence):
        return self.sentence_answer_mapping[sentence]

