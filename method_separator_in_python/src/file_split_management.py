from nltk.tokenize import word_tokenize
from method_separator_in_python.src.java_method import Method
from method_separator_in_python.src.treat_methods import TreatMethods
from method_separator_in_python.src.treat_class import TreatClass

class Split:
    def __init__(self):
        self.treat_methods = TreatMethods()
        self.treat_class = TreatClass()
        self.code_lines = list()
        self.all_methods = list()
        self.all_class = list()
        self.stack = list()

        self.class_name = None
        self.line = None
        self.method_name = None

    def work_in_file(self, file):
        with open(file, errors='ignore') as f:
            self.line = f.readline()

            while self.line:
                self.step_management()
                self.line = f.readline()
            f.close()
            return self.all_methods

    def step_management(self):
        tokens = word_tokenize(self.line)
        self.split_class(tokens)

        if self.class_name is not None:
            self.split_methods(tokens)

    def split_class(self, tokens):
        if self.treat_class.is_class_caller(tokens):
            name = self.treat_class.define_class_name(tokens)
            self.class_name = name

    def split_methods(self, tokens):
        for i in range(0, len(tokens)):
            if self.treat_methods.check_if_is_usable_method(tokens, self.class_name):
                self.method_name = self.treat_methods.define_method_name(tokens)
                self.code_lines.append(self.line)
                self.stack.append('{')
                break
            if len(self.stack) > 0:
                if i is len(tokens) - 1:
                    self.code_lines.append(self.line)
                if tokens[i] is '{':
                    self.stack.append('{')
                elif tokens[i] is '}':
                    self.stack.pop()
                    if len(self.stack) == 0:
                        self.create_new_method_object_and_clear_list()

    def create_new_method_object_and_clear_list(self):
        new_method = Method(self.method_name, self.code_lines.copy(), self.class_name)
        print(new_method)
        self.all_methods.append(new_method)
        self.code_lines.clear()


